from livewires import games

games.init(screen_width=640,
           screen_height=480,
           fps=50)

explosions = ["icons/exp-1.bmp",
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
              "icons/exp-11.bmp",]

explosion = games.Animation(images=explosions,
                            x=games.screen.width/2,
                            y=games.screen.height/2,
                            n_repeats=0,
                            repeat_interval = 5)
games.screen.add(explosion)
games.screen.mainloop()

