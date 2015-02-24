from  livewires import games
import random

games.init(screen_height= 480,
           screen_width=640,
           fps=50)

class Asteroid(games.Sprite):
    """Asteroid"""
    ASTEROID_SIZE_SMALL = 1
    ASTEROID_SIZE_MEDIUM = 2
    ASTEROID_SIZE_LARGE = 3
    images = {ASTEROID_SIZE_SMALL: games.load_image("icons/asteroid_small.bmp"),
              ASTEROID_SIZE_MEDIUM: games.load_image("icons/asteroid_med.bmp"),
              ASTEROID_SIZE_LARGE: games.load_image("icons/asteroid_big.bmp")}
    SPEED = 2

    def __init__(self,x,y,size):
        super().__init__(
            image=Asteroid.images[size],
            x = x, y = y,
            dx=random.choice([1,-1])* Asteroid.SPEED * random.random()/size,
            dy=random.choice([1,-1])* Asteroid.SPEED * random.random()/size)
        self.size = size

    def update(self):

        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width



class Ship(games.Sprite):
    """Spaceship"""

    ship_image = games.load_image("icons/ship.bmp")
    SHIP_SPEED = 1
    SHIP_ROTATION_STEP = 2
    move_sound = games.load_sound("icons/thrust.wav")

    def update(self):
        """Moves and rotation"""
        if games.keyboard.is_pressed(games.K_w):
            self.y -= Ship.SHIP_SPEED
        if games.keyboard.is_pressed(games.K_s):
            self.y += Ship.SHIP_SPEED
        if games.keyboard.is_pressed(games.K_a):
            self.x -= Ship.SHIP_SPEED
        if games.keyboard.is_pressed(games.K_d):
            self.x += Ship.SHIP_SPEED

        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.SHIP_ROTATION_STEP
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.SHIP_ROTATION_STEP




def main():
    background = games.load_image("icons/background.jpg", transparent=False)
    games.screen.background = background

    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.ASTEROID_SIZE_SMALL,Asteroid.ASTEROID_SIZE_MEDIUM,Asteroid.ASTEROID_SIZE_LARGE])
        new_asteroid = Asteroid(x = x,y = y,size = size)
        games.screen.add(new_asteroid)

    the_ship = Ship(image=Ship.ship_image,
                    x = games.screen.width/2,
                    y = games.screen.height/2)

    games.screen.add(the_ship)
    games.screen.mainloop()

main()
