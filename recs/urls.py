from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /game/123456/
    path("game/<int:steamid>/", views.game, name='game'),
    # ex: /submit/
    path("submit/", views.submit, name='submit'),
    # ex: /top/
    path("top/", views.top, name="top"),
    # ex: /genre/1/
    path("genre/<int:genre_id>/", views.genre, name="genre"),
    # ex: /atoz/
    path("atoz/", views.atoz, name="atoz")
]
