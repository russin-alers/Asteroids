from livewires import  games,color
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
        """ Check for overlapping sprites. """
        super(Collide, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Asteroid):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
                    self.die()
                else:
                    self.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
                    Boss.HITS_TO_KILL += 1
                    print(Boss.HITS_TO_KILL)
                    if Boss.HITS_TO_KILL == 20:
                        sprite.die()


    def die(self):
        """ Destroy self and leave explosion behind. """
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()

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


class Ship(Collide):
    """Spaceship"""
    SHIP_SPEED = 1
    SHIP_ROTATION_STEP = 2
    ACCELERATION = .03
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
            self.dx += Ship.ACCELERATION * math.sin(angle)
            self.dy += Ship.ACCELERATION * -math.cos(angle)

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

    def die(self):

        super(Ship, self).die()
        self.game.end()




class Missile(Collide):
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

class Game(object):

    def __init__(self):
        self.levels = Levels(self)
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

        """if Levels.level == 0:
            self.levels.asteroid_level()"""
        if Levels.level % 3 == 0:
            self.levels.boss_level()
        else:
            self.levels.asteroid_level()

        level_message = games.Message(value= "Level" + str(Levels.level),
                                      size= 40,
                                      color=color.yellow,
                                      x=games.screen.width/2,
                                      y=games.screen.height/10,
                                      lifetime= 3 * games.screen.fps,
                                      is_collideable=False)
        games.screen.add(level_message)
        if Levels.level > 1:
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
