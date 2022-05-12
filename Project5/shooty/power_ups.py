from settings import *
import pygame as pg


class Pow(pg.sprite.Sprite):
    def __init__(self, center, pow_img):
        super(Pow, self).__init__()
        self.pow_img = pow_img
        self.type = random.choice(pow_list)
        self.image = self.pow_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        if self.type == "shield":
            self.speed_y = 3
        elif self.type == "gun":
            self.speed_y = 6
        elif self.type == "life":
            self.speed_y = 10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.kill()

