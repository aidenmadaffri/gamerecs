from django.core.management.base import BaseCommand, CommandError
import time
from recs.models import Game
from recs import steam

class Command(BaseCommand):
    help = 'Updates the prices for all the games'

    def handle(self, *args, **options):
        self.stdout.write("Started updating prices.")
        counter = 0
        for game in Game.objects.all():
            time.sleep(1)
            #Don't over request steam api
            if counter > 150:
                time.sleep(300)
                counter = 0
            steam_info = steam.get_game_info(game.steamid)
            game.price = steam_info['price']
            game.save()
            counter += 1
            self.stdout.write(game.name + " updated.")
        self.stdout.write("Finished updating prices")
