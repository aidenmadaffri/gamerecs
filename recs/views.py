import re
from recs import steam

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from .models import Game, Genre, GameGenrePosition
from .forms import SubmitForm

def index(request):
    return HttpResponse("TODO")

def detail(request, steamid):
    game = get_object_or_404(Game, steamid=steamid)
    return render(request, "recs/detail.html", {"game": game})

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

            return HttpResponseRedirect("/")

    else:
        form = SubmitForm()

    return render(request, "recs/submit.html", {'form': form})
