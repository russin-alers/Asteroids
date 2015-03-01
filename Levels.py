import random
from Wrap import *
from Boss import *
from Game import *


class Levels(object):
    level = 0

    def __init__(self, game):
        self.game = game

    def position(self, buffer):
        self.buffer = buffer
        x_min = random.randrange(self.buffer)
        y_min = self.buffer - x_min

        x_distance = random.randrange(x_min, games.screen.width - x_min)
        y_distance = random.randrange(y_min, games.screen.height - y_min)

        x = self.game.ship.x + x_distance
        y = self.game.ship.y + y_distance

        x %= games.screen.width
        y %= games.screen.height
        return x,y


    def asteroid_level(self):
        Levels.level += 1

        BUFFER = 150

        for i in range(Levels.level):

            x,y = self.position(BUFFER)

            new_asteroid = Asteroid (game = self.game,
                                    x=x, y=y,
                                    size=Asteroid.SIZE_LARGE)
            games.screen.add(new_asteroid)



    def boss_level(self):
        Levels.level += 1

        BUFFER = 150

        x,y = self.position(BUFFER)

        #if i !=2:
        new_boss = Boss (game = self.game,
                                x=x, y=y)

        games.screen.add(new_boss)

