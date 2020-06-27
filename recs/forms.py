from django import forms
from django.core import validators

from .models import Genre

class SubmitForm(forms.Form):
    choices = list()
    for genre in Genre.objects.all():
        choices.append((genre.pk, genre.name))

    url = forms.CharField(label="Game's Steam URL:", validators=[validators.RegexValidator(regex='^(https://)?store\.steampowered\.com/app/(\d+).*$', message='Please provide a valid store page link, e.x. https://store.steampowered.com/app/570/Dota_2/')])
    submitter = forms.CharField(max_length=50, required=False)
    genres = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)
    thoughts = forms.CharField(max_length=1000, widget=forms.Textarea)
