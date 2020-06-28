from django.contrib import admin

from .models import Game
from .models import Genre
from .models import GameGenrePosition

class PositionInline(admin.TabularInline):
    model = GameGenrePosition
    extra = 1

class WasThirdPartySubmissionFilter(admin.SimpleListFilter):
    title = 'third party submission'
    parameter_name = 'was_third_party_submission'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.exclude(submitter__exact="")
        elif value == 'No':
            return queryset.filter(submitter__exact="")
        return queryset

class GameAdmin(admin.ModelAdmin):
    inlines = (PositionInline,)
    list_display = ('name', 'price', 'was_third_party_submission', 'public')
    list_filter = ['genres', WasThirdPartySubmissionFilter, 'public']
    search_fields = ['name']

# Register your models here.
admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
