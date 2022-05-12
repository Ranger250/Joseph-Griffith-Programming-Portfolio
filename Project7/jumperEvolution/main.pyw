# Thanks for the sprites kenny!
# Happy tune by http://opengameart.org/users/syncopika
# Yippee by http://opengameart.org/userssnabisch

# Jumper platform game
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import copy

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.scroll_speed = 0
        self.list_of_steps = ["jump", "jump", "jump", "jump_right", "jump_right", "jump_right", "jump_right", "jump_left",  "jump_left", "jump_left", "jump_left","wait", "right", "left"]
        self.gen_timer = pg.time.get_ticks()
        self.new_gen_steps = []
        self.starting_pos = [40, HEIGHT - 100]
        self.top_plat = 0
        self.enemy_heights = []
        self.screen_displacment = 0
        self.gen_time_stamp = 0
        self.last_best = -1000
        self.no_change = 0
        self.top_score = -100000000000
        self.best_steps = []

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        assets_dir = path.join(self.dir, 'assets')
        img_dir = path.join(assets_dir, 'imgs')
        with open(path.join(self.dir, HS_FILE), "r") as f:
            try:
                self.highscore = int(f.readline())
                print(self.highscore)
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        self.audio_dir = path.join(assets_dir, 'audio')
        self.ambient_dir = path.join(self.audio_dir, 'ambient')
        self.fx_dir = path.join(self.audio_dir, 'fx')
        self.music_dir = path.join(self.audio_dir, 'music')
        self.jump_sound = pg.mixer.Sound(path.join(self.fx_dir, 'Jump33.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.fx_dir, 'Boost16.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.players = pg.sprite.Group()

        for i in range(STEP_NUM):
            self.best_steps.append([""])

        load_height = 0
        cloud_load_height = HEIGHT
        enemy_load_height = -300
        for i in range(GEN_NUM):

            steps = []
            for s in range(STEP_NUM):
                step = [random.choice(self.list_of_steps), random.randrange(100, 3000)]
                steps.append(step)
            player = Player(self, steps)
            player.id = i
            self.players.add(player)
        # create starting platforms
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        # temp
        # for i in range(40):
        #     Platform(self,i * 20 -50, HEIGHT - 60)
        # for i in range(40):
        #     Platform(self,i * 20 -50, HEIGHT - 30)


        for i in range(PLATFORM_NUM):
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), load_height)
            load_height -= random.randrange(10, 200)
        for i in range(PLATFORM_NUM*2):
            Cloud(self, cloud_load_height)
            cloud_load_height -= random.randrange(10, 150)
        for plat in self.platforms:
            if plat.rect.centery < self.top_plat:
                self.top_plat = plat.rect.centery
        while enemy_load_height > self.top_plat:
            self.enemy_heights.append(enemy_load_height)
            enemy_load_height -= random.randrange(500, 800)
        for height in self.enemy_heights:
            Mob(self, height)

        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.music_dir, 'Happy Tune.ogg'))

        self.run()

    def new_gen(self):

        # top_score = -1000000000000
        # for sprite in self.players:
        #     sprite.calculate_score()
        #     if sprite.score > top_score:
        #         top_score = sprite.score
        #
        # for sp in self.players:
        #     if sp.score == top_score:
        #         base_steps = sp.steps
        #
        # for i in range(len(self.players)):
        #     steps = base_steps[:]
        #     for step in steps:
        #         if random.randrange(1, 100) <= MUTATION_PER:
        #             step[0] = random.choice(self.list_of_steps)
        #         if random.randrange(1, 100) <= MUTATION_PER:
        #             step[1] = random.randrange(100, 3000)
        #     self.new_gen_steps.append(steps)
        # for player in self.players:
        #     player.kill()
        #
        # for steps in self.new_gen_steps:
        #     player = Player(self, steps)
        #     self.players.add(player)

        new_step = False

        self.last_best = self.top_score

        for sprite in self.players:
            sprite.calculate_score()

            if sprite.score > self.top_score:
                if sprite.score > self.top_score:
                    self.top_score = sprite.score
                    print("new score")
        base_steps = self.best_steps
        for sp in self.players:
            if sp.score == self.top_score:
                base_steps = sp.steps
                self.best_steps = base_steps


        if self.no_change > NEW_STEP:
            new_step = True
            self.no_change = 0
            print("up steps")
        print(len(base_steps))

        for pl in self.players:
            print(pl.record)
            steps = copy.deepcopy(base_steps)
            for step in steps:
                if pl.id > 0:
                    if len(self.best_steps) - STEP_NUM >= 1:
                        if len(steps) - steps.index(step) <= 500:
                            if random.randrange(1, 100) <= MUTATION_PER:
                                step[0] = random.choice(self.list_of_steps)
                            if random.randrange(1, 100) <= MUTATION_PER:
                                step[1] = random.randrange(100, 3000)
                    else:
                        if random.randrange(1, 100) <= MUTATION_PER:
                            step[0] = random.choice(self.list_of_steps)
                        if random.randrange(1, 100) <= MUTATION_PER:
                            step[1] = random.randrange(100, 3000)

            if new_step:
                steps.append([random.choice(self.list_of_steps), random.randrange(100, 3000)])

            pl.steps = steps[:]
            pl.pos = vec(*self.starting_pos)
            pl.rect.center = (self.starting_pos[0], self.starting_pos[1])
            pl.vel = vec(0, 0)
            pl.acc = vec(0, 0)
            pl.score = 0
            pl.record = 0
            pl.record_time = 0
            pl.height = 0
            pl.end = False
            pl.current_step = 0
            pl.last_step = 0
            pl.last_step_time = pg.time.get_ticks()
            pl.height -= self.screen_displacment
        if new_step:
            # steps.append([random.choice(self.list_of_steps), random.randrange(100, 3000)])
            self.best_steps.append([random.choice(self.list_of_steps), random.randrange(100, 3000)])
        # mob_counter = 0
        for mob in self.mobs:
            mob.rect.centerx = WIDTH
            # mob.rect.centery = self.enemy_heights[mob_counter]
            # mob_counter += 1
        self.gen_time_stamp = pg.time.get_ticks()

        if self.top_score <= self.last_best:
            self.no_change += 1
        else:
            self.no_change = 0
        print("changenum " + str(self.no_change))




    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.scroll_speed = -2
                if event.key == pg.K_DOWN:
                    self.scroll_speed = 2
                # if event.key == pg.K_SPACE:
                #     for player in self.players:
                #         player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    self.scroll_speed = 0

            #     if event.key == pg.K_SPACE:
            #         for player in self.players:
            #             player.jump_cut()
            # if event.type == pg.MOUSEWHEEL:
            #     self.scroll_speed = event.y
            # else:
            #     self.scroll_speed = 0


    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # new gen?
        now = pg.time.get_ticks()
        if now - self.gen_timer >= len(self.best_steps) / 1 * 1000:
            self.new_gen()
            self.gen_timer = now
            return
        # if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0 , 500, 1000]):
        #     self.mob_timer = now
        #     Mob(self)
        # hit mobs?
        hits = pg.sprite.groupcollide(self.players, self.mobs, False, False)
        if hits:
            for player in self.players:
                mob_hits = pg.sprite.spritecollide(player, self.mobs, False, pg.sprite.collide_mask)
                if mob_hits:
                    player.pos = vec(*self.starting_pos)
                    player.rect.center = (self.starting_pos[0], self.starting_pos[1])
                    player.vel = vec(0, 0)
                    player.acc = vec(0, 0)
            # if mob_hits:
            #     self.playing = False

        # move screen based on scroll wheel
        for sprite in self.all_sprites:
            sprite.rect.y += -(self.scroll_speed * 5)
        for player in self.players:
            player.rect.y += (self.scroll_speed * 5)
            player.pos.y += -(self.scroll_speed * 5)
        self.starting_pos[1] += -(self.scroll_speed * 5)
        for player in self.players:
            player.height += (self.scroll_speed * 5)
        self.screen_displacment += (self.scroll_speed * 5)

        # check if player hits a platform - only if falling
        for player in self.players:
            if player.vel.y > 0:
                hits = pg.sprite.spritecollide(player, self.platforms, False)
                if hits:
                    lowest = hits[0]
                    for hit in hits:
                        if hit.rect.bottom > lowest.rect.bottom:
                            lowest = hit
                    if player.pos.x < lowest.rect.right + 10 and player.pos.x > lowest.rect.left - 10:
                        if player.pos.y < lowest.rect.centery:
                            player.pos.y = lowest.rect.top
                            player.vel.y = 0
                            player.jumping = False
        # if player reaches top 1/4 of screen
        #     if player.rect.top <= HEIGHT / 4:
        #         if random.randrange(100) < 15:
        #             Cloud(self)

                # player.pos.y += max(abs(player.vel.y), 2)
                # for cloud in self.clouds:
                #     cloud.rect.y += max(abs(player.vel.y / 2), 2)
                # for mob in self.mobs:
                #     mob.rect.y += max(abs(player.vel.y), 2)
                # for plat in self.platforms:
                #     plat.rect.y += max(abs( player.vel.y), 2)
                    # Destroys platforms as they go off screen
                    # if plat.rect.top >= HEIGHT:
                    #     plat.kill()
                    #     self.score += 10
        # if player hits powerup
        # pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        # for pow in pow_hits:
        #     if pow.type == 'boost':
        #         self.boost_sound.play()
        #         self.player.vel.y = -BOOST_POWER
        #         self.player.jumping = False
        # Die!
        # if self.player.rect.bottom > HEIGHT:
        #     # drop and kill all platforms
        #     for sprite in self.all_sprites:
        #         sprite.rect.y -=max(self.player.vel.y, 10)
        #         if sprite.rect.bottom < 0:
        #             sprite.kill()
        # if len(self.platforms) == 0:
        #     self.playing = False

        # spawn new platforms to keep same average number
        # while len(self.platforms) < 8:
        #     width = random.randrange(50, 100)
        #     Platform(self, random.randrange(0, WIDTH-width),
        #             random.randrange(-75, -30))



    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.music_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Watch rabbits learn how to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.music_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2 ,HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

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

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
