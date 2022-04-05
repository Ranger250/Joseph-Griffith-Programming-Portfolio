# Imports
import pygame as pg
from settings import *
import random

# Create player class inherited from sprite
class Player(pg.sprite.Sprite):
    # Constructor
    def __init__(self):
        super(Player, self).__init__()
        # Make a player that is a green square 50x50
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        # Making a "hitbox" for our player
        self.rect = self.image.get_rect()
        # Centering in the middle of our screen
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speedx = 17
        self.speedy = 9

    def update(self):
        self.bouncing()

    def screenwraping(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def teleporting(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.top = HEIGHT
            self.rect.centerx = WIDTH/2
            self.speedx = 0
            self.speedy = -2
        if self.rect.right < 0:
            self.rect.bottom = 0
            self.rect.centerx = WIDTH/2
            self.speedx = 0
            self.speedy = 2
        if self.rect.bottom < 0:
            self.rect.right = 0
            self.rect.centery = HEIGHT/2
            self.speedx = 2
            self.speedy = 0
        if self.rect.top > HEIGHT:
            self.rect.left = WIDTH
            self.rect.centery = HEIGHT / 2
            self.speedx = -2
            self.speedy = 0

    def bouncing(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx *= -1
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.speedy *= -1