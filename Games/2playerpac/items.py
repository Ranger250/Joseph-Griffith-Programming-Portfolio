from settings import *

class Pellet(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pellets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.groups = game.all_sprites
        self.image = pg.Surface((int(TILESIZE*.15625), int(TILESIZE*.15625)))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = (x * TILESIZE) + int(TILESIZE/2)
        self.rect.centery = (y * TILESIZE) + int(TILESIZE/2)

class Pow_pellet(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((int(TILESIZE*.46875), int(TILESIZE*.46875)))
        self.rect = self.image.get_rect()
        self.rect.centerx = (x * TILESIZE) + int(TILESIZE/2)
        self.rect.centery = (y * TILESIZE) + int(TILESIZE/2)
        self.pows = ['score', 'flip', 'switch']
        self.chose_new_pow()

    def chose_new_pow(self):
        self.pow = random.choice(self.pows)
        if self.pow == 'score':
            self.image.fill(YELLOW)
        if self.pow == 'flip':
            self.image.fill(RED)
        if self.pow == 'switch':
            self.image.fill(GREEN)
