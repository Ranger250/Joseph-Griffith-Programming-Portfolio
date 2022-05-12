# Sprite classes for platform game
import pygame as pg
import pygame.time
import random

from settings import *
vec = pg.math.Vector2


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, steps):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.current_step = 0
        self.last_step = 0
        self.steps = steps
        self.last_step_time = pg.time.get_ticks()
        self.end = False
        self.record = 0
        self.height = 0
        self.record_time = 0
        self.score = 0
        self.id = 0

    def calculate_score(self):
        self.score = self.record - self.record_time/10000
        if self.record_time == 0:
            self.score = -1000000000000


    def do_step(self):
        now = pg.time.get_ticks()
        if now - self.last_step_time >= self.steps[self.current_step][1]:
            self.current_step += 1
            self.last_step_time = now
            if self.current_step > len(self.steps) - 1:
                self.current_step = len(self.steps) - 1
                self.end = True
            if self.end:
                self.vel.x = 0
                return

            self.last_step = self.current_step-1
            if self.last_step < 0:
                self.last_step = 0

            if self.steps[self.last_step][0] == "jump" or self.steps[self.last_step][0] == "jump_right" or self.steps[self.last_step][0] == "jump_left":
                self.jump_cut()
            else:
                self.acc.x = 0

            if self.steps[self.current_step][0] == "jump":
                self.jump()
                self.acc.x = 0
            elif self.steps[self.current_step][0] == "jump_right":
                self.jump()
                self.acc.x = PLAYER_ACC
            elif self.steps[self.current_step][0] == "jump_left":
                self.jump()
                self.acc.x = -PLAYER_ACC
            elif self.steps[self.current_step][0] == "right":
                self.acc.x = PLAYER_ACC
            elif self.steps[self.current_step][0] == "left":
                self.acc.x = -PLAYER_ACC
            else:
                self.acc.x = 0


    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()

        now = pg.time.get_ticks()
        if self.height > self.record:
            self.rect.x += 2
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 2
            if hits and not self.jumping:
                self.record = self.height
                self.record_time = now - self.game.gen_time_stamp


        self.acc = vec(0, PLAYER_GRAV)
        self.do_step()
        # keys = pg.key.get_pressed()
        # if keys[pg.K_LEFT]:
        #     self.acc.x = -PLAYER_ACC
        # if keys[pg.K_RIGHT]:
        #     self.acc.x = PLAYER_ACC

        if self.steps[self.current_step][0] == "jump_right" or self.steps[self.current_step][0] == "right":
            self.acc.x = PLAYER_ACC
        elif self.steps[self.current_step][0] == "jump_left" or self.steps[self.current_step][0] == "left":
            self.acc.x = -PLAYER_ACC
        else:
            self.acc.x = 0
        if self.end:
            self.acc.x = 0

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        # self.height = -self.pos.y
        self.height -= self.vel.y + 0.5 * self.acc.y

        self.rect.midbottom = self.pos


    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class Cloud(pg.sprite.Sprite):
    def __init__(self, game, y):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = random.randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = y

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < POW_SPAWN_PCT:
            # Pow(self.game, self)
            pass

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(556, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH
        self.rect.centery = y
        self.vx = random.randrange(1, 4)
        self.vx *= random.choice([1, -1])
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        # self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH:
            self.rect.centerx = 0
        if self.rect.right < 0:
            self.rect.centerx = WIDTH