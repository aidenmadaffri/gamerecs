from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /123456/
    path("<int:steamid>/", views.detail, name='detail'),
    # ex: /submit;
    path("submit/", views.submit, name='submit')
]
