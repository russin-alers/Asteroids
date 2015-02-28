import random
from Wrap import *
from Boss import *
from Game import *


class Levels(object):
    level = 0

    def __init__(self, game):
        self.game = game

    def asteroid_level(self):
        Levels.level += 1

        BUFFER = 150

        for i in range(Levels.level):

            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)

            x = self.game.ship.x + x_distance
            y = self.game.ship.y + y_distance

            x %= games.screen.width
            y %= games.screen.height

            #if i !=2:
            """new_asteroid = Asteroid(game = self,
                                    x=x, y=y,
                                    size=Asteroid.SIZE_LARGE)
            games.screen.add(new_asteroid)"""
            new_asteroid = Asteroid (game = self.game,
                                    x=x, y=y,
                                    size=Asteroid.SIZE_LARGE)
            games.screen.add(new_asteroid)
            #else:
            #    new_ship = Ship(game=self,
            #                    x=x,y=y)
            #    games.screen.add(new_ship)



        level_message = games.Message(value= "Level" + str(self.level),
                                      size= 40,
                                      color=color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/10,
                                      lifetime= 3 * games.screen.fps,
                                      is_collideable=False)
        games.screen.add(level_message)
        if self.level > 1:
            self.game.sound.play()