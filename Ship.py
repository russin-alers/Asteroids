from livewires import games

games.init(screen_height= 480,
           screen_width=640,
           fps=50)


class Ship(games.Sprite):
    """Spaceship"""
    
    def update(self):
        """Moves and rotation"""
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1




def main():
    background = games.load_image("icons/background.jpg", transparent=False)
    games.screen.background = background
    ship_image = games.load_image("icons/ship.bmp")
    the_ship = Ship(image=ship_image,
                    x=games.screen.width/2,
                    y=games.screen.height/2)
    games.screen.add(the_ship)
    games.screen.mainloop()
main()

