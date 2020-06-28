import re
from recs import steam

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from .models import Game, Genre, GameGenrePosition
from .forms import SubmitForm

def index(request):
    genres = Genre.objects.all().order_by('name')
    return render(request, "recs/index.html", {"genres": genres})

def top(request):
    return render(request, "recs/top.html")

def genre(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    price_under_15 = GameGenrePosition.objects.filter(genre=genre, game__price__lt=15.00, position__gt=0).order_by("position")
    price_15_to_30 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=15.00, game__price__lt=30.00, position__gt=0).order_by("position")
    price_over_30 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=30.00).order_by("position")
    price_under_15_community = GameGenrePosition.objects.filter(genre=genre, game__price__lt=15.00, position=-1).order_by("game__name")
    price_15_to_30_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=15.00, game__price__lt=30.00, position=-1).order_by("game__name")
    price_over_30_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=30.00, position=-1).order_by("game__name")
    return render(request, "recs/genre.html", {
        'genre': genre,
        'price_under_15': price_under_15,
        'price_15_to_30': price_15_to_30,
        'price_over_30': price_over_30,
        'price_under_15_community': price_under_15_community,
        'price_15_to_30_community': price_15_to_30_community,
        'price_over_30_community': price_over_30_community
    })

def game(request, steamid):
    game = get_object_or_404(Game, steamid=steamid)
    return render(request, "recs/game.html", {"game": game})

def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            url_search = re.search('^(https://)?store\.steampowered\.com/app/(\d+).*$', url, re.IGNORECASE)
            steamid = url_search.group(2)
            steam_info = steam.get_game_info(steamid)

            if steam_info is None:
                return render(request, "recs/submit.html", {
                    'form': form,
                    'error_message': "The game you provided does not exist on Steam."
                })
            elif Game.objects.filter(steamid=steamid).exists():
                return render(request, "recs/submit.html", {
                    'form': form,
                    'error_message': "The game you provided is already on the list."
                })

            new_game = Game(steamid=steamid, name=steam_info['name'], submitter=form.cleaned_data['submitter'], url=url, price=steam_info['price'], thoughts=form.cleaned_data['thoughts'], description=steam_info['description'], public=True)
            new_game.save()

            for genre_id in form.cleaned_data['genres']:
                game_genre_position = GameGenrePosition(game=new_game, genre=Genre.objects.get(pk=genre_id), position=0)
                game_genre_position.save()

            if 'done-submitting' in request.POST:
                return HttpResponseRedirect("/game/" + new_game.steamid)
            return HttpResponseRedirect("/submit/")

    else:
        form = SubmitForm()

    return render(request, "recs/submit.html", {'form': form})
