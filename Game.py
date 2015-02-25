from  livewires import games
import random, math

games.init(screen_height= 768,
           screen_width=1024,
           fps=50)

class Wrap(games.Sprite):

    def update(self):

        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        self.destroy()

class Collide(Wrap):

    def update(self):
        super(Collide,self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        new_explosion = Explosion(x=self.x,y=self.y)
        games.screen.add(new_explosion)
        self.destroy()


class Explosion(games.Animation):
    sound = games.load_sound("sounds/explosion.wav")
    exp_images = ["icons/exp-1.bmp",
                  "icons/exp-1_1.bmp",
                  "icons/exp-2.bmp",
                  "icons/exp-3.bmp",
                  "icons/exp-4.bmp",
                  "icons/exp-5.bmp",
                  "icons/exp-6.bmp",
                  "icons/exp-7.bmp",
                  "icons/exp-7_1.bmp",
                  "icons/exp-8.bmp",
                  "icons/exp-10.bmp",
                  "icons/exp-11.bmp"]

    def __init__(self, x,y):
        super().__init__(images=Explosion.exp_images,
                         x=x, y=y,
                         repeat_interval=4,
                         n_repeats=1,
                         is_collideable=False)
        Explosion.sound.play()



class Asteroid(Wrap):
    """Asteroid"""
    SIZE_SMALL = 1
    SIZE_MEDIUM = 2
    SIZE_LARGE = 3
    SPAWN = 2

    images = {SIZE_SMALL: games.load_image("icons/asteroid_small.bmp"),
              SIZE_MEDIUM: games.load_image("icons/asteroid_med.bmp"),
              SIZE_LARGE: games.load_image("icons/asteroid_big.bmp")}
    SPEED = 2

    def __init__(self,x,y,size):
        super().__init__(
            image=Asteroid.images[size],
            x = x, y = y,
            dx=random.choice([1,-1])* Asteroid.SPEED * random.random()/size,
            dy=random.choice([1,-1])* Asteroid.SPEED * random.random()/size)
        self.size = size

    def die(self):
        super().die()
        if self.size != Asteroid.SIZE_SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x,
                                        y=self.y,
                                        size=self.size-1)
                games.screen.add(new_asteroid)
        self.destroy()

class Missile(Collide):
    image = games.load_image("icons/missile.bmp")
    sound = games.load_sound("sounds/missile.wav")
    LIFETIME = 20
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

        self.lifetime -=1
        if self.lifetime == 0:
            self.destroy()

class Ship(Collide):
    """Spaceship"""
    SHIP_SPEED = 1
    SHIP_ROTATION_STEP = 2
    ACCELERTATION = .03
    MISSILE_DELAY = 20
    ship_image = games.load_image("icons/ship.bmp")
    move_sound = games.load_sound("sounds/thrust.wav")

    def __init__(self,x,y):
        super().__init__(image=Ship.ship_image, x=x,y=y)
        self.missile_wait = 0

    def update(self):
        super(Ship,self).update()
        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 1
            Ship.move_sound.play()
            angle = self.angle * math.pi / 180
            self.dx += Ship.ACCELERTATION * math.sin(angle)
            self.dy += Ship.ACCELERTATION * -math.cos(angle)
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

def main():
    background = games.load_image("icons/background.jpg", transparent=False)
    games.screen.background = background

    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SIZE_SMALL,Asteroid.SIZE_MEDIUM,Asteroid.SIZE_LARGE])
        new_asteroid = Asteroid(x = x,y = y,size = size)
        games.screen.add(new_asteroid)

    the_ship = Ship(x = games.screen.width/2,
                    y = games.screen.height/2)

    games.screen.add(the_ship)
    games.screen.mainloop()

main()
