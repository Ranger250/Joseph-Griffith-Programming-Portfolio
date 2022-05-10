# Tile Based Game
from settings import *
from gameFunctions import *
from lander import *

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

    def load_data(self):
        self.dir = path.dirname(__file__)
        assets_dir = path.join(self.dir, 'assets')
        img_dir = path.join(assets_dir, 'imgs')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Lander(self)
        self.all_sprites.add(self.player)
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

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

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
        draw_text(self.screen, "Score ", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

