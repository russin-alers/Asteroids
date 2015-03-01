from Wrap import *
from Explosion import *
from Asteroid import *
from Ship import *
from Boss import *

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
                if isinstance(sprite,Boss ):
                    self.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)
                    Boss.HITS_TO_KILL += 1
                    print(Boss.HITS_TO_KILL)
                    if Boss.HITS_TO_KILL == 20:
                        sprite.die()
                if isinstance(sprite, Ship):
                    sprite.die()
                    new_explosion = Explosion(x=self.x,y=self.y)
                    games.screen.add(new_explosion)

    def die(self):
        """ Destroy self and leave explosion behind. """
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()