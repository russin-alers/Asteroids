from Wrap import  *
from Ship import *
from Missile import *
from Ship import *

class Boss(Wrap):

    ACCELERTATION = .03
    VELOCITY_MAX = 7
    HITS_TO_KILL = 0
    boss_image = games.load_image("icons/boss.png")
    SPEED = 1
    POINTS = 150

    def __init__(self, game, x,y):
        super().__init__(image=Boss.boss_image, x=x, y=y,
                         dx=random.choice([1,-1])* Boss.SPEED * random.random() ,
                         dy=random.choice([1,-1])* Boss.SPEED * random.random() )

        self.game = game

    def update(self):
        super().update()



    def die(self):
        self.game.score.value += Boss.POINTS
        super().die()
        self.game.advance()
        Boss.HITS_TO_KILL = 0










