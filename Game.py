from  livewires import games, color
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

class Missile(Collide):
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
                sprite.die()
            self.die()


        self.lifetime -=1
        if self.lifetime == 0:
            self.destroy()

class Ship(Collide):
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
                sprite.die()
            self.game.end()
            self.die()
        """if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Missile):
                    sprite.die()"""


class Game(object):

    def __init__(self):
        self.level = 0

        self.sound = games.load_sound("sounds/level.wav")

        self.score =  games.Text(value=0,
                                 size=30,
                                 color=color.white,
                                 top=5,
                                 right=games.screen.width -10,
                                 is_collideable = False)

        games.screen.add(self.score)

        self.ship = Ship(game = self,
                         x=games.screen.width/2,
                         y=games.screen.height/2)
        games.screen.add(self.ship)

    def play(self):
        games.music.load("sounds/theme.mp3")
        games.music.play(-1)

        background = games.load_image("icons/background.jpg")
        games.screen.background = background

        self.advance()

        games.screen.mainloop()

    def advance(self):

        self.level += 1

        BUFFER = 150

        for i in range(self.level):

            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)

            x = self.ship.x + x_distance
            y = self.ship.y + y_distance

            x %= games.screen.width
            y %= games.screen.height

            new_asteroid = Asteroid(game = self,
                                    x=x, y=y,
                                    size=Asteroid.SIZE_LARGE)
            games.screen.add(new_asteroid)

        level_message = games.Message(value= "Level" + str(self.level),
                                      size= 40,
                                      color=color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/10,
                                      lifetime= 3 * games.screen.fps,
                                      is_collideable=False)
        games.screen.add(level_message)
        if self.level > 1:
            self.sound.play()


    def end(self):

        end_message  = games.Message(value="Game Over",
                                     size=90,
                                     color=color.red,
                                     x=games.screen.width/2,
                                     y=games.screen.height/2,
                                     lifetime=5 * games.screen.fps,
                                     after_death=games.screen.quit,
                                     is_collideable=False)

        games.screen.add(end_message)

def main():
    Asteroids = Game()
    Asteroids.play()

main()
