# Imports
import pygame as pg
from settings import *
import random

# Create player class inherited from sprite
class Player(pg.sprite.Sprite):
    # Constructor
    def __init__(self, sprite, bullet_img, all_sprites, bullet_group, shoot_snd):
        super(Player, self).__init__()
        # Make a player that is a green square 50x50
        self.image = sprite
        self.image = pg.transform.scale(self.image, (50, 40))
        self.image.set_colorkey(BLACK)
        # Making a "hitbox" for our player
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * .85)/2
        # Centering in the middle of our screen
        self.rect.center = (WIDTH/2, HEIGHT - HEIGHT/20)
        self.speedx = 0
        self.speedy = 0
        self.moveSpeed = 11
        self.shield = 100
        self.ammo = 500
        self.shoot_delay = 0
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power_level = 1
        self.all_sprites = all_sprites
        self.bullet_group = bullet_group
        self.bullet_img = bullet_img
        self.shoot_snd = shoot_snd
        self.last_speed_drop = pg.time.get_ticks()
        self.speed_drop_delay = 100
        self.shooting = False
        self.cool_down_timer = 0
        self.cooldownDelay = 4000

    def update(self):
        if self.hidden and pg.time.get_ticks()-self.hide_timer > 1500:
            self.hidden = False
            self.rect.center = (WIDTH/2, HEIGHT - HEIGHT/20)
        if not self.shooting:
            self.shoot_delay -= 5
            if self.shoot_delay < 0:
                self.shoot_delay = 0
        if self.shoot_delay > 700 and self.power_level > 1:
            self.power_level -= 1
            if self.power_level < 1:
                self.power_level = 1
            self.shoot_delay = 0

        self.speedx = 0
        keystates = pg.key.get_pressed()
        if keystates[pg.K_a] or keystates[pg.K_LEFT]:
            self.speedx = -self.moveSpeed
        if keystates[pg.K_d] or keystates[pg.K_RIGHT]:
            self.speedx = self.moveSpeed
        if keystates[pg.K_SPACE]:
            if self.ammo > 0:
                self.shoot(self.all_sprites, self.bullet_group, self.bullet_img, self.shoot_snd)
                self.shooting = True

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.centerx += self.speedx

        now = pg.time.get_ticks()

        # if now - self.last_speed_drop > self.speed_drop_delay:
        #     self.last_speed_drop = now
        #     self.shoot_delay += 10

    def cool_down(self):
        self.shoot_delay = 0


    def shoot(self, all_sprites, bullet_group, sprite, shoot_snd):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            shoot_snd.play()
            self.last_shot = now
            if self.power_level == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top-1, sprite, all_sprites, bullet_group)
            elif self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top - 1, sprite, all_sprites, bullet_group)
                self.speed_drop_delay = 200
            elif self.power_level == 2:
                bullet = Bullet(self.rect.right, self.rect.top - 1, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.left, self.rect.top - 1, sprite, all_sprites, bullet_group)
            elif self.power_level == 3:
                bullet = Bullet(self.rect.right, self.rect.top - 1, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.left, self.rect.top - 1, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.centerx, self.rect.top - 1, sprite, all_sprites, bullet_group)
            elif self.power_level == 4:
                bullet = Bullet(self.rect.right, self.rect.top - 1, sprite, all_sprites, bullet_group, 1)
                bullet = Bullet(self.rect.left, self.rect.top - 1, sprite, all_sprites, bullet_group, -1)
                bullet = Bullet(self.rect.centerx, self.rect.top - 1, sprite, all_sprites, bullet_group)
            elif self.power_level == 5:
                bullet = Bullet(self.rect.right, self.rect.top - 1, sprite, all_sprites, bullet_group, 1)
                bullet = Bullet(self.rect.left, self.rect.top - 1, sprite, all_sprites, bullet_group, -1)
                bullet = Bullet(self.rect.right - 5, self.rect.top - 1, sprite, all_sprites, bullet_group, 3)
                bullet = Bullet(self.rect.left + 5 , self.rect.top - 1, sprite, all_sprites, bullet_group, -3)
                bullet = Bullet(self.rect.centerx, self.rect.top - 1, sprite, all_sprites, bullet_group)
            self.ammo -= 1
            self.shoot_delay += 20

    def gun_up(self):
        self.power_level += 1
        if self.power_level > 5:
            self.power_level = 5



    def die(self):
        self.loseLife()
        self.hide()
        self.shield = 100
        self.ammo = 500
        self.shoot_delay = 0


    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 1000)

    def takeDamage(self, hit):
        self.shield -= hit.radius

    def loseLife(self):
        self.lives -=1

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

    def add_shield(self, num):
        self.shield += 100
        if self.shield > 100:
            self.shield = 100

    def add_life(self):
        self.lives += 1




class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, all_sprites, bullet_group, speed_x=0):
        super(Bullet, self).__init__()
        # Make a player that is a green square 50x50
        self.image = sprite
        self.image = pg.transform.scale(self.image, (10, 20))
        self.image.set_colorkey(BLACK)
        # Making a "hitbox" for our player
        self.rect = self.image.get_rect()
        # Centering in the middle of our screen
        self.rect.centerx = x
        self.rect.centery = y
        self.moveSpeed = 20
        self.speedy = -self.moveSpeed
        all_sprites.add(self)
        bullet_group.add(self)
        self.speed_x = speed_x

    def update(self):
        self.rect.centery += self.speedy
        self.rect.centerx += self.speed_x
        if self.rect.bottom < -5:
            self.kill()

