from settings import *
vec = pg.math.Vector2

class Meteor(pg.sprite.Sprite):
    def __init__(self, game, color, size, x, y, dir):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image_store = random.choice(self.game.meteor_img_list[color][size])
        # self.image_store = pg.transform.scale(self.image_store, (35, 35))
        self.image_store.set_colorkey(BLACK)
        self.image = self.image_store
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.color = color
        self.splitted = False
        self.radius = (self.rect.width * .85) / 2
        yspeed = random.randint(-METEOR_SPEED, METEOR_SPEED)
        xspeed = random.randint(-METEOR_SPEED, METEOR_SPEED)
        if dir == "up":
            self.vel = vec(xspeed, -abs(yspeed))
        if dir == "right":
            self.vel = vec(abs(xspeed), yspeed)
        if dir == "left":
            self.vel = vec(-abs(xspeed), yspeed)
        if dir == "down":
            self.vel = vec(xspeed, abs(yspeed))

        self.sizes = ["big", "med", "small", "tiny"]
        for i in range(len(self.sizes)):
            if size == self.sizes[i]:
                self.size = i

        self.acc = vec(0, 0)
        self.rot = random.randint(-6, 6)

    def update(self):
        self.rotate()

        if self.rect.left > WIDTH:
            self.pos.x = 0
        if self.rect.right < 0:
            self.pos.x = WIDTH
        if self.rect.top > HEIGHT:
            self.pos.y = 0
        if self.rect.bottom < 0:
            self.pos.y = HEIGHT


        self.pos += self.vel

        self.rect.center = self.pos

    def rotate(self):
        self.rot = (self.rot) % 360
        newimg = pg.transform.rotate(self.image_store, self.rot)
        oldcenter = self.rect.center
        self.image = newimg
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def split(self, dir):
        self.size += 1
        if self.size < 4:
            for i in range(random.randint(2, 3)):
                meteor = Meteor(self.game, self.color, self.sizes[self.size], self.pos.x, self.pos.y, dir)
                self.game.all_sprites.add(meteor)
                self.game.meteorgroup.add(meteor)
