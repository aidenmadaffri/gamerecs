from django.db import models
from django.db.models import F

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200, unique=True)
    genres = models.ManyToManyField(Genre, through='GameGenrePosition', verbose_name="genres")
    submitter = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField("steam store page")
    price = models.FloatField()
    ttb = models.FloatField("TTB")
    thoughts = models.TextField(max_length=1000)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

    def was_third_party_submission(self):
        return self.submitter is not None

class GameGenrePosition(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    position = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.game.was_third_party_submission():
            self.position = -1
        elif self.position == 0:
            last_position = GameGenrePosition.objects.filter(genre=self.genre).order_by("-position")[0].position
            self.position = last_position + 1
        else:
            GameGenrePosition.objects.filter(position__gte=self.position).update(position=F('position') + 1)
        super().save(*args, **kwargs)
