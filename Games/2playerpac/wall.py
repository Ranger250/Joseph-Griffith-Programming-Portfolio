from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game, sprite, x, y, rot=0, move_x=0, move_y=0, flip_x=False, flip_y=False,
                 stretch_y=False, stretch_x=False):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = sprite
        self.image.set_colorkey(BLACK)
        height = self.image.get_height()
        width = self.image.get_width()
        self.image = pg.transform.scale(self.image, (int(width / 32 * TILESIZE), int(height / 32 * TILESIZE)))
        if stretch_x == True:
            self.image = pg.transform.scale(self.image, (TILESIZE, int(TILESIZE/1.6)))
        if stretch_y == True:
            self.image = pg.transform.scale(self.image, (TILESIZE, int(TILESIZE/1.6)))
        if flip_x == True:
            self.image = pg.transform.flip(self.image, flip_x, flip_y)
        if flip_y == True:
            self.image = pg.transform.flip(self.image, flip_x, flip_y)
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x * TILESIZE) + move_x
        self.rect.y = (y * TILESIZE) + move_y
