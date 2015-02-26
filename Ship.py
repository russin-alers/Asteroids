import math

from Missile import *
from Asteroid import *
from Explosion import *


class Ship(Wrap):
    """Spaceship"""
    SHIP_SPEED = 1
    SHIP_ROTATION_STEP = 2
    ACCELERTATION = .03
    MISSILE_DELAY = 20
    VELOCITY_MAX = 3
    ship_image = games.load_image("icons/ship.bmp")
    move_sound = games.load_sound("sounds/thrust.wav")

    def __init__(self,game,x,y):
        super().__init__(image=Ship.ship_image, x=x,y=y)
        self.game = game
        self.missile_wait = 0

    def update(self):
        super(Ship,self).update()
        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 1
            Ship.move_sound.play()
            angle = self.angle * math.pi / 180
            self.dx += Ship.ACCELERTATION * math.sin(angle)
            self.dy += Ship.ACCELERTATION * -math.cos(angle)

            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.SHIP_ROTATION_STEP
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.SHIP_ROTATION_STEP
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile =  Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

        if self.missile_wait > 0:
            self.missile_wait -= 1

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Asteroid):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)

            self.game.end()
            self.die()
        """if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Missile):
                    sprite.die()"""

