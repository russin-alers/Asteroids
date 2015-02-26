from livewires import games

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
