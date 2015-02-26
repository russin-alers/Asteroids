from  livewires import  color

from src.Ship import *
from src.Asteroid import *

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

                #if i !=2:
                new_asteroid = Asteroid(game = self,
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