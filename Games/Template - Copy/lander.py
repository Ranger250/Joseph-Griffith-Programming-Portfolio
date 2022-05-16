from settings import *
vec = pg.math.Vector2

class Lander(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image_store = self.game.spritesheet.get_image(52, 244, 48, 48)
        self.image_store = pg.transform.scale(self.image_store, (35, 35))
        self.image_store.set_colorkey(BLACK)
        self.image = self.image_store
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.last_shot = 0
        self.shoot_delay = 100

    def update(self):
        self.rotate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot += PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.rot -= PLAYER_ROT_SPEED
        if keys[pg.K_UP]:
            self.acc = vec(0, -PLAYER_ACC).rotate(-self.rot)


        # apply friction
        # self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

    def move_angle(self):
        dir = self.rot // 90
        rot = self.rot % 90
        if rot == 0:
            if dir == 1:
                self.acc.x = -PLAYER_ACC
                self.acc.y = 0
            elif dir == 2:
                self.acc.x = 0
                self.acc.y = PLAYER_ACC
            elif dir == 3:
                self.acc.x = PLAYER_ACC
                self.acc.y = 0
            elif dir == 0:
                self.acc.x = 0
                self.acc.y = -PLAYER_ACC
        else:

            num1 = 90 / (rot)
            num2 = 90 / (90 - (rot))
            if dir == 0:
                self.acc.x = -PLAYER_ACC * num2
                self.acc.y = -PLAYER_ACC * num1
            elif dir == 1:
                self.acc.x = -PLAYER_ACC * num1
                self.acc.y = PLAYER_ACC * num2
            elif dir == 2:
                self.acc.x = PLAYER_ACC * num2
                self.acc.y = PLAYER_ACC * num1
            elif dir == 3:
                self.acc.x = PLAYER_ACC * num1
                self.acc.y = -PLAYER_ACC * num2

            len = self.acc.x **2 + self.acc.y **2


    def rotate(self):
        self.rot = (self.rot) % 360
        newimg = pg.transform.rotate(self.image_store, self.rot)
        oldcenter = self.rect.center
        self.image = newimg
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def shoot(self, all_sprites, bullet_group, sprite, shoot_snd):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            shoot_snd.play()
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, sprite, all_sprites, bullet_group, self.rot)


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

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, all_sprites, bullet_group, rot):
        super(Bullet, self).__init__()
        # Make a player that is a green square 50x50
        self.image = sprite
        self.image = pg.transform.scale(self.image, (10, 20))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(5, 5)
        self.acc = vec(0, 0)
        self.rot = rot
        all_sprites.add(self)
        bullet_group.add(self)
        self.vel = vec(0, -5).rotate(-self.rot)
        self.rotate()

    def update(self):
        if self.rect.centerx < 0 or self.rect.centerx > WIDTH or self.rect.centery < 0 or self.rect.centery > HEIGHT:
            self.kill()
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

    def rotate(self):
        self.rot = (self.rot) % 360
        newimg = pg.transform.rotate(self.image, self.rot)
        oldcenter = self.rect.center
        self.image = newimg
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter