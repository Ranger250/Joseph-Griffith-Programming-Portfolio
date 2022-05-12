import pygame as pg
from settings import *
import random

class Mob(pg.sprite.Sprite):
    def __init__(self, sprite):
        super(Mob, self).__init__()
        self.image_orig = sprite
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # self.image = pg.transform.scale(self.image, (50, 40))
        # Making a "hitbox" for our player
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * .85) / 2
        self.moving = False
        self.rect.center = (random.randint(20, WIDTH-20), random.randint(-100, -20))
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(4, 18)
        if self.moving:
            self.speedy *= 2
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pg.time.get_ticks()


    def update(self):
        self.rotate()
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if self.rect.left > WIDTH and self.rect.centery < HEIGHT*75:
            self.rect.right = 0
        if self.rect.right < 0  and self.rect.centery < HEIGHT*75:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT + random.randint(3, 20):
            self.rect.center = (random.randint(20, WIDTH - 20), random.randint(-100, -20))
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(4, 18)
            if self.moving:
                self.speedy *= 2






    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            newimg = pg.transform.rotate(self.image_orig, self.rot)
            oldcenter = self.rect.center
            self.image = newimg
            self.rect = self.image.get_rect()
            self.rect.center = oldcenter