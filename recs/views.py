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
    set_1_description = None
    set_2_description = None
    set_3_description = None
    set_1 = None
    set_2 = None
    set_3 = None
    set_1_community = None
    set_2_community = None
    set_3_community = None
    if GameGenrePosition.objects.filter(genre=genre, game__price__gt=30.00).exists():
        set_1_description = "Under $15"
        set_2_description = "$15-$30"
        set_3_description = "Over $30"
        set_1 = GameGenrePosition.objects.filter(genre=genre, game__price__lt=15.00, position__gt=0).order_by("position")
        set_2 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=15.00, game__price__lt=30.00, position__gt=0).order_by("position")
        set_3 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=30.00, position__gt=0).order_by("position")
        set_1_community = GameGenrePosition.objects.filter(genre=genre, game__price__lt=15.00, position=-1).order_by("game__name")
        set_2_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=15.00, game__price__lt=30.00, position=-1).order_by("game__name")
        set_3_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=30.00, position=-1).order_by("game__name")
    else:
        set_1_description = "Under $10"
        set_2_description = "$10-$20"
        set_3_description = "Over $20"
        set_1 = GameGenrePosition.objects.filter(genre=genre, game__price__lt=10.00, position__gt=0).order_by("position")
        set_2 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=10.00, game__price__lt=20.00, position__gt=0).order_by("position")
        set_3 = GameGenrePosition.objects.filter(genre=genre, game__price__gte=20.00, position__gt=0).order_by("position")
        set_1_community = GameGenrePosition.objects.filter(genre=genre, game__price__lt=10.00, position=-1).order_by("game__name")
        set_2_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=10.00, game__price__lt=20.00, position=-1).order_by("game__name")
        set_3_community = GameGenrePosition.objects.filter(genre=genre, game__price__gte=20.00, position=-1).order_by("game__name")

    return render(request, "recs/genre.html", {
        'genre': genre,
        'set_1': set_1,
        'set_2': set_2,
        'set_3': set_3,
        'set_1_community': set_1_community,
        'set_2_community': set_2_community,
        'set_3_community': set_3_community,
        'set_1_description': set_1_description,
        'set_2_description': set_2_description,
        'set_3_description': set_3_description
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

class GameAToZ:
    def __init__(self, steamid, name, submitter, url, price, thoughts, description):
        self.steamid = steamid
        self.name = name
        self.genres = []
        self.submitter = submitter
        self.url = url
        self.price = price
        self.thoughts = thoughts
        self.description = description

    def was_third_party_submission(self):
        return self.submitter is not None and self.submitter != ""

def atoz(request):
    data = GameGenrePosition.objects.order_by("game__name").distinct()

    games = dict()
    for game_pos in data:
        if game_pos.game.name in games:
            games[game_pos.game.name].genres.append(game_pos.genre.name)
        else:
            game = GameAToZ(game_pos.game.steamid, game_pos.game.name, game_pos.game.submitter, game_pos.game.url, game_pos.game.price, game_pos.game.thoughts, game_pos.game.description)
            game.genres.append(game_pos.genre.name)
            games[game_pos.game.name] = game

    return render(request, "recs/atoz.html", {"games": games.values()})


