import random

from src.Wrap import *


class Asteroid(Wrap):
    """Asteroid"""
    SIZE_SMALL = 1
    SIZE_MEDIUM = 2
    SIZE_LARGE = 3
    SPAWN = 2
    POINTS = 30
    total = 0

    images = {SIZE_SMALL: games.load_image("icons/asteroid_small.bmp"),
              SIZE_MEDIUM: games.load_image("icons/asteroid_med.bmp"),
              SIZE_LARGE: games.load_image("icons/asteroid_big.bmp")}
    SPEED = 2

    def __init__(self,game,x,y,size):
        super().__init__(
            image=Asteroid.images[size],
            x = x, y = y,
            dx=random.choice([1,-1])* Asteroid.SPEED * random.random()/size,
            dy=random.choice([1,-1])* Asteroid.SPEED * random.random()/size)
        self.game = game
        self.size = size
        Asteroid.total += 1


    def die(self):
        Asteroid.total -= 1
        self.game.score.value += int(Asteroid.POINTS / self.size)
        self.game.score.right = games.screen.width - 10

        if self.size != Asteroid.SIZE_SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game=self.game,
                                        x=self.x,
                                        y=self.y,
                                        size=self.size-1)
                games.screen.add(new_asteroid)

        if Asteroid.total == 0:
            self.game.advance()

        #self.destroy()
        super().die()
