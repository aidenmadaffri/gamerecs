from django.contrib import admin

from .models import Game
from .models import Genre
from .models import GameGenrePosition

class PositionInline(admin.TabularInline):
    model = GameGenrePosition
    extra = 1

class GameAdmin(admin.ModelAdmin):
    inlines = (PositionInline,)

# Register your models here.
admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
