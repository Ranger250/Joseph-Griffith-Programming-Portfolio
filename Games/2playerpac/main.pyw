# main

# imports
import pacMan
from settings import *
from pacMan import *
from wall import *
from items import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.colors = ["blue", "orange", "pink", "red", "possessed", "vulnerable"]
        self.directions = ["right", "left", "up", "down"]
        #
        self.ghost_images = {}
        self.pac_images = []

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        pg.init()
        pg.mixer.init()

        self.pellet_snd_1 = pg.mixer.Sound(os.path.join(sound_folder, "munch_1.wav"))
        self.pellet_snd_2 = pg.mixer.Sound(os.path.join(sound_folder, "munch_2.wav"))
        self.pow_pel_snd = pg.mixer.Sound(os.path.join(sound_folder, "power_pellet.wav"))
        self.death_snd_1 = pg.mixer.Sound(os.path.join(sound_folder, "death_1.wav"))
        self.death_snd_2 = pg.mixer.Sound(os.path.join(sound_folder, "death_2.wav"))
        music = pg.mixer.music.load(os.path.join(sound_folder, "Enguarde [Donkey Kong 64].ogg"))

        self.wall_corner_img = pg.image.load(path.join(img_folder, 'wall_corner.png')).convert()
        self.wall_img = pg.image.load(path.join(img_folder, 'wall.png')).convert()


        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_down.png.png')).convert())
        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_up.png.png')).convert())
        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_right_open.png.png')).convert())
        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_right_closed.png.png')).convert())
        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_left_open.png.png')).convert())
        self.pac_images.append(pg.image.load(path.join(img_folder, 'pacman_left_closed.png.png')).convert())



        for color in self.colors:
            self.ghost_images[color] = []
            for dir in self.directions:
                self.ghost_images[color].append(pg.image.load(path.join(img_folder, '{}_ghost_{}.png.png'.format(color, dir))).convert())

    def new(self):
        self.start_screen()
        self.pows = pg.sprite.Group()
        self.pac1 = Player(self, 2, 2)
        self.pac2 = Player(self, 27, 35)
        self.pacs = pg.sprite.Group()
        self.pacs.add(self.pac1)
        self.pacs.add(self.pac2)
        self.pac1s = pg.sprite.Group()
        self.pac1s.add(self.pac1)
        self.pac2s = pg.sprite.Group()
        self.pac2s.add(self.pac2)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.pac1)
        self.all_sprites.add(self.pac2)
        self.ghosts = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pellets = pg.sprite.Group()
        self.switched = True
        self.last_switch = 0
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    x = random.randint(1, 100)
                    if x == 1:
                        Pow_pellet(self, col, row)
                    else:
                        Pellet(self, col, row)
                if tile == '1':
                    Wall(self, self.wall_corner_img, col, row, move_x=TILESIZE/2)
                if tile == '2':
                    Wall(self, self.wall_corner_img, col, row, flip_x=True)
                if tile == '3':
                    Wall(self, self.wall_corner_img, col, row, move_y=int(TILESIZE/2), rot=180)
                if tile == '4':
                    Wall(self, self.wall_corner_img, col, row, move_y=int(TILESIZE/2), move_x=int(TILESIZE/2), flip_y=True)
                if tile == '5':
                    Wall(self, self.wall_img, col, row, move_y=int(TILESIZE*.4375), stretch_x=True)
                if tile == '6':
                    Wall(self, self.wall_img, col, row, move_y=int(TILESIZE/32), stretch_x=True, flip_y=True)
                if tile == '7':
                    Wall(self, self.wall_img, col, row, flip_y=True, stretch_y=True, rot=90)
                if tile == '8':
                    Wall(self, self.wall_img, col, row, move_x=int(TILESIZE*.46875), stretch_y=True, rot=90)
                if tile == 'a':
                    Wall(self, self.wall_img, col, row, stretch_x=True, flip_y=True, move_y=int(TILESIZE/32))
                    Wall(self, self.wall_img, col, row, move_x=int(TILESIZE*.46875), move_y=int(TILESIZE*.375), stretch_y=True, rot=90)
                    Wall(self, self.wall_corner_img, col, row, move_x=int(TILESIZE*.53125), move_y=int(TILESIZE/32), rot=180)
                if tile == 'b':
                    Wall(self, self.wall_img, col, row, stretch_x=True, flip_y=True, move_y=int(TILESIZE/32), move_x=int(TILESIZE*.375))
                    Wall(self, self.wall_img, col, row, move_y=int(TILESIZE*.375), stretch_y=True, flip_y=True, rot=90)
                    Wall(self, self.wall_corner_img, col, row, flip_y=True, move_y=int(TILESIZE/32), move_x=-int(TILESIZE/32))
                if tile == 'c':
                    Wall(self, self.wall_img, col, row, move_y=int(TILESIZE*.4375), move_x=int(TILESIZE*.375), stretch_x=True)
                    Wall(self, self.wall_img, col, row, flip_y=True, stretch_y=True, rot=90, move_y=-int(TILESIZE*.375))
                    Wall(self, self.wall_corner_img, col, row, move_y=int(TILESIZE*.46875), move_x=-int(TILESIZE/32))
                if tile == 'd':
                    Wall(self, self.wall_img, col, row, move_y=int(TILESIZE*.4375), move_x=-int(TILESIZE*.15625), stretch_x=True)
                    Wall(self, self.wall_img, col, row, move_x=int(TILESIZE*.46875), move_y=-int(TILESIZE/2), stretch_y=True, rot=90)
                    Wall(self, self.wall_corner_img, col, row, move_y=int(TILESIZE*.46875), move_x=int(TILESIZE*.5625), flip_x=True)

        self.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                # Pacmans movement
                if not self.switched:
                    if event.key == pg.K_w:
                         self.pac2.speedx = 0
                         self.pac2.speedy = -1
                    if event.key == pg.K_a:
                         self.pac2.speedy = 0
                         self.pac2.speedx = -1
                    if event.key == pg.K_d:
                         self.pac2.speedy = 0
                         self.pac2.speedx = 1
                    if event.key == pg.K_s:
                         self.pac2.speedx = 0
                         self.pac2.speedy = 1
                    if event.key == pg.K_UP:
                         self.pac1.speedx = 0
                         self.pac1.speedy = -1
                    if event.key == pg.K_LEFT:
                         self.pac1.speedy = 0
                         self.pac1.speedx = -1
                    if event.key == pg.K_RIGHT:
                         self.pac1.speedy = 0
                         self.pac1.speedx = 1
                    if event.key == pg.K_DOWN:
                         self.pac1.speedx = 0
                         self.pac1.speedy = 1
                else:
                    if event.key == pg.K_w:
                        self.pac1.speedx = 0
                        self.pac1.speedy = -1
                    if event.key == pg.K_a:
                        self.pac1.speedy = 0
                        self.pac1.speedx = -1
                    if event.key == pg.K_d:
                        self.pac1.speedy = 0
                        self.pac1.speedx = 1
                    if event.key == pg.K_s:
                        self.pac1.speedx = 0
                        self.pac1.speedy = 1
                    if event.key == pg.K_UP:
                        self.pac2.speedx = 0
                        self.pac2.speedy = -1
                    if event.key == pg.K_LEFT:
                        self.pac2.speedy = 0
                        self.pac2.speedx = -1
                    if event.key == pg.K_RIGHT:
                        self.pac2.speedy = 0
                        self.pac2.speedx = 1
                    if event.key == pg.K_DOWN:
                        self.pac2.speedx = 0
                        self.pac2.speedy = 1



                # ghost movement
                if event.key == pg.K_UP:
                    pass
                if event.key == pg.K_LEFT:
                    pass
                if event.key == pg.K_RIGHT:
                    pass
                if event.key == pg.K_DOWN:
                    pass

    def update(self):
        self.all_sprites.update()
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self.pac1, self.pows, True)
        if hits:
            self.pow_pel_snd.play()
            for hit in hits:
                if hit.pow == "score":
                    self.pac1.score_pow()
                elif hit.pow == "flip":
                    self.pac2.flip_pow()
                elif hit.pow == "switch":
                    self.switched = not self.switched
                    self.last_switch = now
        hits = pg.sprite.spritecollide(self.pac2, self.pows, True)
        if hits:
            self.pow_pel_snd.play()
            for hit in hits:
                if hit.pow == "score":
                    self.pac2.score_pow()
                elif hit.pow == "flip":
                    self.pac1.flip_pow()
                elif hit.pow == "switch":
                    self.switched = not self.switched
                    self.last_switch = now

        if self.pac1.speed + self.pac2.speed >= int(TILESIZE*.34375):

            if self.pac1.score > self.pac2.score:
                self.pac1.speed = int(TILESIZE*.1875)
                self.pac2.speed = int(TILESIZE*.15625)
            elif self.pac2.score > self.pac1.score:
                self.pac2.speed = int(TILESIZE*.1875)
                self.pac1.speed = int(TILESIZE*.15625)
            else:
                self.pac2.speed = int(TILESIZE*.1875)
                self.pac1.speed = int(TILESIZE*.1875)
        if self.pac1.score > self.pac2.score:
            self.pac1.big = True
            self.pac2.big = False
        elif self.pac1.score < self.pac2.score:
            self.pac1.big = False
            self.pac2.big = True
        else:
            self.pac1.big = False
            self.pac2.big = False

        hits = pg.sprite.spritecollide(self.pac1, self.pac2s, False)
        if hits:
            if self.pac1.score > self.pac2.score:
                self.pac2.kill()
                self.death_snd_1.play()
            elif self.pac1.score < self.pac2.score:
                self.pac1.kill()
                self.death_snd_1.play()
            self.game_over_screen()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTBLUE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTBLUE, (0, y), (WIDTH, y))

    def draw(self):
        now = pg.time.get_ticks()
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.pacs.draw(self.screen)
        self.draw_text(str(self.pac1.score), int(TILESIZE*.625), RED, int(WIDTH/3), int(HEIGHT*.61))
        self.draw_text(str(self.pac2.score), int(TILESIZE*.625), RED, int(WIDTH*2/3), int(HEIGHT*.61))
        if now - self.last_switch < 2000 and self.last_switch != 0:
            self.draw_text("SWITCH!", int(TILESIZE*1.5625), RED, WIDTH/2, HEIGHT/2)

        # last
        pg.display.flip()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def start_screen(self):
        if not self.running:
            return
        print("test")
        self.screen.fill(BLACK)
        self.draw_text("2 Player Pac", int(TILESIZE*1.5), WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play", int(TILESIZE*.625), WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Arrow keys and wasd to control. Big eats little. Player with higher score is big", int(TILESIZE*.5625), WHITE, WIDTH / 2, (HEIGHT / 2 -30))
        self.draw_text("Powerups: Red = Inverts opponent controls  Yellow = 100 points  Green = Players switch controls", int(TILESIZE*.5625), WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Have fun!", int(TILESIZE*.5625), WHITE, WIDTH / 2, (HEIGHT / 2)+30)
        pg.display.flip()
        self.wfk()

    def game_over_screen(self):

        if not self.running:
            return
        self.screen.fill(BLACK)
        if self.pac1.score > self.pac2.score:
            winner = "Player 1 wins"
        else:
            winner = "Player 2 wins"
        self.draw_text(winner, int(TILESIZE*1.5), WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play", int(TILESIZE*.625), WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wfk()
        self.new()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



    def wfk(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
while g.running:
    g.new()

pg.quit()
