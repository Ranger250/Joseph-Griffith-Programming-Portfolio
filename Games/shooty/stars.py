import pygame as pg
from settings import *
import random

class Star(pg.sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        # Make a player that is a green square 50x50
        self.image = pg.Surface((2, 2))
        self.image.fill(WHITE)
        # Making a "hitbox" for our player
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * .85) / 2
        # Centering in the middle of our screen
        self.rect.center = (random.randint(0, WIDTH), random.randint(0,HEIGHT))
        self.moveSpeed = 30
        self.speedx = 0
        self.speedy = self.moveSpeed
    def update(self):
        self.speedx = 0



        if self.rect.bottom > HEIGHT:
            self.rect.bottom = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        keystates = pg.key.get_pressed()
        if keystates[pg.K_a] or keystates[pg.K_LEFT]:
            self.speedx = 10
        if keystates[pg.K_d] or keystates[pg.K_RIGHT]:
            self.speedx = -10

        if keystates[pg.K_w] or keystates[pg.K_UP]:
            self.rect.centery += self.speedy
            self.rect.centerx += self.speedx