from livewires import  games

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
