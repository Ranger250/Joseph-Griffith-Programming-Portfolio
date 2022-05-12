import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Player, self).__init__()
        self.game = game
        # self.image = pg.Surface((15, 15))

        self.pac_images = []
        for image in game.pac_images:

            image.set_colorkey(BLACK)
            image = pg.transform.scale(image, (int(TILESIZE/1.6), int(TILESIZE/1.6)))
            self.pac_images.append(image)
        self.image = self.pac_images[0]
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.lives = 3

        self.rect.center = (x*TILESIZE-TILESIZE/2, y*TILESIZE-TILESIZE/2)
        self.speed = PLAYER_SPEED
        self.speedx = 0
        self.speedy = 0
        self.open = True
        self.last_update = 0
        self.score = -10
        self.big = False
        self.pbe = 0
        self.flipped = 1
        self.flip_time = 0

    def score_pow(self):
        self.score += 100

    def flip_pow(self):
        self.flipped = -1
        self.flip_time = pg.time.get_ticks()


    def collide_with_walls(self, dir):
        pass

    def update(self):
        now = pg.time.get_ticks()
        if self.flipped and now - self.flip_time > 5000:
            self.flipped = 1
        if self.score == -10:
            self.score = 0
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        if not self.big:
            self.pac_images = []
            for image in self.game.pac_images:
                image.set_colorkey(BLACK)
                image = pg.transform.scale(image, (int(TILESIZE/1.6), int(TILESIZE/1.6)))
                self.pac_images.append(image)
        else:
            self.pac_images = []
            for image in self.game.pac_images:
                image.set_colorkey(BLACK)
                image = pg.transform.scale(image, (int(TILESIZE*.9375), int(TILESIZE*.9375)))
                self.pac_images.append(image)

        self.rect.centerx += 3
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.centerx -= 3
        if hits:
            self.speedx = 0
            self.rect.centerx -= int(TILESIZE*.3125)

        self.rect.centerx -= 3
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.centerx += 3
        if hits:
            self.speedx = 0
            self.rect.centerx += int(TILESIZE*.3125)

        self.rect.centery += 3
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.centery -= 3
        if hits:
            self.speedy = 0
            self.rect.centery -= int(TILESIZE*.3125)

        self.rect.centery -= 3
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.centery += 3
        if hits:
            self.speedy = 0
            self.rect.centery += int(TILESIZE*.3125)

        pel_hits = pg.sprite.spritecollide(self, self.game.pellets, False)
        for hit in pel_hits:
            if self.pbe == 0:
                self.game.pellet_snd_1.play()
                self.pbe = 1
            elif self.pbe == 1:
                self.game.pellet_snd_2.play()
                self.pbe = 0
            self.score += 10
            hit.kill()
        self.animations()




        self.rect.centerx += self.speedx * self.flipped * self.speed
        self.rect.centery += self.speedy *self.flipped * self.speed

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

        self.speed = int(self.score // 15 * TILESIZE / 32)
        if self.speed == 0:
            self.speed = 1
        if self.speed > 6:
            self.speed = 6

    def die(self):
        if self.lives > 0:
            self.lives -= 1
        else:
            self.game.playing = False

    def animations(self):
        now = pg.time.get_ticks()
        if self.speedx > 0:
            if now - self.last_update > 200:
                self.last_update = now
                self.open = not self.open

                if self.open:
                    center = self.rect.center
                    self.image = self.pac_images[2]
                    self.rect.center = center
                else:
                    center = self.rect.center
                    self.image = self.pac_images[3]
                    self.rect.center = center
            # turn pacman into a pacman that pacs right
        if self.speedx < 0:
            if now - self.last_update > 200:
                self.last_update = now
                self.open = not self.open

                if self.open:
                    center = self.rect.center
                    self.image = self.pac_images[4]
                    self.rect.center = center
                else:
                    center = self.rect.center
                    self.image = self.pac_images[5]
                    self.rect.center = center
                    # turn pacman into a pacman that pacs left
        if self.speedy > 0:
            center = self.rect.center
            self.image = self.pac_images[0]
            self.rect.center = center
            # turn pacman into a pacman that pacs down
        if self.speedy < 0:
            center = self.rect.center
            self.image = self.pac_images[1]
            self.rect.center = center
            # turn pacman into a pacman that pacs up
