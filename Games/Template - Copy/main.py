# Tile Based Game
from settings import *
from gameFunctions import *
from lander import *
from star import *
from meteor import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        # pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.colors = ["grey", "brown"]
        self.sizes = ["big", "med", "small", "tiny"]

    def load_data(self):
        self.dir = path.dirname(__file__)
        assets_dir = path.join(self.dir, 'assets')
        img_dir = path.join(assets_dir, 'imgs')
        audio_dir = path.join(assets_dir, "audio")
        fx_dir = path.join(audio_dir, "fx")
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        self.meteor_img_list = {}
        self.meteor_img_list["brown"] = {}
        self.meteor_img_list["grey"] = {}
        self.meteor_img_list["brown"]["big"] = []
        self.meteor_img_list["brown"]["med"] = []
        self.meteor_img_list["brown"]["small"] = []
        self.meteor_img_list["brown"]["tiny"] = []
        self.meteor_img_list["grey"]["big"] = []
        self.meteor_img_list["grey"]["med"] = []
        self.meteor_img_list["grey"]["small"] = []
        self.meteor_img_list["grey"]["tiny"] = []

        meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png",
                       "meteorBrown_med1.png", "meteorBrown_med3.png",
                       "meteorBrown_small1.png", "meteorBrown_small2.png",
                       "meteorBrown_tiny1.png","meteorBrown_tiny2.png",
                       "meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png",
                       "meteorGrey_med1.png", "meteorGrey_med2.png",
                       "meteorGrey_small1.png", "meteorGrey_small2.png",
                       "meteorGrey_tiny1.png", "meteorGrey_tiny1.png"]
        counter = 1
        for img in meteor_list:
            if counter < 5:
                self.meteor_img_list["brown"]["big"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 7:
                self.meteor_img_list["brown"]["med"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 9:
                self.meteor_img_list["brown"]["small"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 11:
                self.meteor_img_list["brown"]["tiny"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 15:
                self.meteor_img_list["grey"]["big"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 17:
                self.meteor_img_list["grey"]["med"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 19:
                self.meteor_img_list["grey"]["small"].append(pg.image.load(path.join(img_dir, img)).convert())
            elif counter < 21:
                self.meteor_img_list["grey"]["tiny"].append(pg.image.load(path.join(img_dir, img)).convert())
            counter += 1

        self.shoot_snd = pg.mixer.Sound(path.join(fx_dir, "pew.wav"))
        self.bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Lander(self)
        self.all_sprites.add(self.player)
        self.bulletgroup = pg.sprite.Group()
        self.meteorgroup = pg.sprite.Group()

        for i in range(NUMSTARS):
            self.all_sprites.add(Star(self, random.randint(0, WIDTH), random.randint(0, HEIGHT)))

        for i in range(NUMMETEORS):
            self.meteor = Meteor(self, random.choice(self.colors), random.choice(self.sizes), random.randint(0, WIDTH), 0, "down")
            self.all_sprites.add(self.meteor)
            self.meteorgroup.add(self.meteor)
        self.num_meteors = NUMMETEORS
        self.start = pg.time.get_ticks()

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key ==  pg.K_SPACE:
                    self.player.shoot(self.all_sprites, self.bulletgroup, self.bullet_img, self.shoot_snd)
        hits = pg.sprite.groupcollide(self.meteorgroup, self.bulletgroup, True, True)
        if hits:
            self.player.add_score()
            # random.choice(expsnd).play()
            for hit in hits:
                if hit.split == False:
                    hit.split()
            hits = pg.sprite.groupcollide(self.meteorgroup, self.bulletgroup, True, True)



        hits = pg.sprite.spritecollide(self.player, self.meteorgroup, False, pg.sprite.collide_circle)
        if hits:
            self.playing = False

    def update(self):
        print(self.num_meteors)
        # Game Loop - Update
        self.all_sprites.update()
        now = pg.time.get_ticks()
        if now - self.start > METEOR_DELAY:
            self.num_meteors += 1
            self.start = now
        if len(self.meteorgroup) < self.num_meteors:
            self.meteor = Meteor(self, random.choice(self.colors), random.choice(self.sizes), random.randint(0, WIDTH), 0, "down")
            self.all_sprites.add(self.meteor)
            self.meteorgroup.add(self.meteor)


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Instructions", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        draw_text(self.screen, "GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Score: " + str(self.player.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        time.sleep(1)
        self.wait_for_key()

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

