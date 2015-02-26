from Asteroid import *
from Explosion import *
import math

class Missile(Wrap):
    image = games.load_image("icons/missile.bmp")
    sound = games.load_sound("sounds/missile.wav")
    LIFETIME = 100
    BUFFER = 90
    M_ACCELERATION = 7

    def __init__(self, ship_x, ship_y, ship_angle):

        Missile.sound.play()
        angle = ship_angle * math.pi / 180

        #missile's starting position depends on ship's x,y and angle
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y

        #missile's speed
        dx = Missile.M_ACCELERATION * math.sin(angle)
        dy = Missile.M_ACCELERATION * -math.cos(angle)

        super().__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy,
                                      angle = ship_angle)

        self.lifetime = Missile.LIFETIME

    def update(self):
        super(Missile,self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Asteroid):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
            self.die()


        self.lifetime -=1
        if self.lifetime == 0:
            self.destroy()
