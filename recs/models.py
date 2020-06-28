from django.db import models
from django.db.models import F

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Game(models.Model):
    steamid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    genres = models.ManyToManyField(Genre, through='GameGenrePosition', verbose_name="genres")
    submitter = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField("steam store page")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    thoughts = models.TextField(max_length=1000)
    description = models.TextField(max_length=1000)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def was_third_party_submission(self):
        return self.submitter is not None and self.submitter != ""
    was_third_party_submission.admin_order_field = 'name'
    was_third_party_submission.boolean = True
    was_third_party_submission.short_description = 'Was third party submission?'

class GameGenrePosition(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    position = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.game.was_third_party_submission():
            self.position = -1
        elif self.position == 0:
            if GameGenrePosition.objects.all().filter(genre=self.genre).count() > 0:
                last_position = GameGenrePosition.objects.filter(genre=self.genre).exclude(position=-1).order_by("-position")[0].position
                self.position = last_position + 1
            else:
                self.position = 1
        else:
            GameGenrePosition.objects.filter(position__gte=self.position).update(position=F('position') + 1)
        super().save(*args, **kwargs)
