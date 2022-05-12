from settings import *


class Ghost(pg.sprite.Sprite):
    def __init__(self, game):
        super(Ghost, self).__init__()
        self.game = game
        self.image = pg.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.lives = 3
        self.speedx = 0
        self.speedy = 0
        self.speed = PLAYER_SPEED
        self.controlled = False

    def update(self):
        self.animations()
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

    def shuffle_ghost_control(self):
        # change the selected ghost sprite to the gray one, and make it player controlled.
        pass

    def die(self):
        # make ghost return to box
        # if game_mode == 2_player make it shuffle at the end / start
        pass

    def animations(self):
        if self.speedx > 0:
            pass  # turn ghostman into a ghost that spooks right
        if self.speedx < 0:
            pass  # turn ghostman into a ghost that spooks left
        if self.speedy > 0:
            pass  # turn ghostman into a ghost that spooks down
        if self.speedy < 0:
            pass  # turn ghostman into a ghost that spooks up
