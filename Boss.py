from Wrap import  *
from Collide import *
from Missile import *
from Ship import *

class Missile(Wrap):
    image = games.load_image("icons/missile.bmp")
    sound = games.load_sound("sounds/missile.wav")
    LIFETIME = 70
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
        dx =  Missile.M_ACCELERATION * math.sin(angle)
        dy =  Missile.M_ACCELERATION * -math.cos(angle)

        super().__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy,
                                      angle = ship_angle)

        self.lifetime = Missile.LIFETIME

    def boss_missile(self, boss_x, boss_y, boss_angle, d_angle):

        angle = boss_angle * math.pi/ 180
        buffer_x = Missile.BUFFER+50* math.sin(angle + d_angle)
        buffer_y = Missile.BUFFER+50 * math.cos(angle + d_angle)
        x = boss_x + buffer_x
        y = boss_y + buffer_y
        new_missle = Missile(x,y,boss_angle)

        return new_missle


    def update(self):
        super(Missile,self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Asteroid):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
                self.die()
                if isinstance(sprite,Boss ):
                    self.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
                    Boss.HITS_TO_KILL += 1
                    print(Boss.HITS_TO_KILL)
                    if Boss.HITS_TO_KILL == 20:
                        sprite.die()
                if isinstance(sprite, Ship):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)




        self.lifetime -=1
        if self.lifetime == 0:
            self.destroy()


class Boss(Collide):

    VELOCITY_MAX = 7
    HITS_TO_KILL = 0
    MISSILE_WAIT = 30
    boss_image = games.load_image("icons/boss.png")
    SPEED = 1
    POINTS = 150

    def __init__(self, game, x,y):
        super().__init__(image=Boss.boss_image, x=x, y=y,
                         dx=random.choice([1,-1])* Boss.SPEED * random.random() ,
                         dy=random.choice([1,-1])* Boss.SPEED * random.random() )

        self.game = game
        self.missile_wait = 0

    def update(self):
        super(Boss,self).update()


        if self.missile_wait == 0:
            new_missle = Missile(self.x,self.y,self.angle)
            games.screen.add(new_missle)
            self.missile_wait = Boss.MISSILE_WAIT

        if self.missile_wait > 0:
            self.missile_wait -= 1




    def die(self):
        self.game.score.value += Boss.POINTS
        super().die()
        self.game.advance()
        Boss.HITS_TO_KILL = 0










