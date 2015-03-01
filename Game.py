from  livewires import  color

from Ship import *
from Asteroid import *
from Levels import *

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