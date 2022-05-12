# thanks for the sprites kenny!

# Main Game File

# Installations_______________________
# install pygame with 'pip install pygame'

# Imports
from settings import *
import pygame as pg
from player import *
from enemy import *
from stars import *
from animations import *
from hudFunctions import *
from power_ups import *

def show_gameOver_screen(screen, background, background_rect, clock):
    global running
    screen.blit(background, background_rect)
    draw_Text(screen, TITLE, 64, RED, WIDTH/2, HEIGHT /4)
    draw_Text(screen, "Arrows to Move, Space to Shoot", 30, WHITE, WIDTH/2, HEIGHT/ 2)
    draw_Text(screen, "Press any Key to start", 30, RED, WIDTH/2, HEIGHT*3/4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


# Setup pygame
pg.init()
pg.mixer.init()
running = True

# Setup main function
def main():
    global running
    game_over = True


    score = 0

    cooldownUpdate = pg.time.get_ticks()

    # Create game objects________________________
    # Set up screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    # Create clock
    clock = pg.time.Clock()

    # load assets
    background = pg.image.load(os.path.join(img_Folder, "starfield.png")).convert()
    background = pg.transform.scale(background, (WIDTH, HEIGHT))
    bg_rect = background.get_rect()

    meteor_img_list = []
    meteor_list = ["meteorBrown_big1.png", "meteorBrown_med1.png", "meteorBrown_small1.png", "meteorBrown_tiny1.png",
                   "meteorBrown_big2.png", "meteorBrown_med3.png", "meteorBrown_small2.png", "meteorBrown_tiny2.png",
                   "meteorBrown_big3.png", "meteorBrown_big4.png", "meteorGrey_big1.png", "meteorGrey_big2.png",
                   "meteorGrey_big3.png", "meteorGrey_big4.png", "meteorGrey_med1.png", "meteorGrey_med2.png",
                   "meteorGrey_small1.png", "meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny1.png"]

    for img in meteor_list:
        meteor_img_list.append(pg.image.load(os.path.join(img_Folder, img)).convert())

    explosion_anim = {}
    explosion_anim["lg"] = []
    explosion_anim["sm"] = []
    explosion_anim["playerExp"] = []
    for i in range(9):
        filename = "regularExplosion0{}.png".format(i)
        img = pg.image.load(os.path.join(img_Folder, filename)).convert()
        img.set_colorkey(BLACK)
        lg_img = pg.transform.scale(img, (75, 75))
        explosion_anim["lg"].append(lg_img)
        sm_img = pg.transform.scale(img, (30, 30))
        explosion_anim["sm"].append(sm_img)
        filename = "sonicExplosion0{}.png".format(i)
        img = pg.image.load(os.path.join(img_Folder, filename)).convert()
        img.set_colorkey(BLACK)
        explosion_anim["playerExp"].append(img)



    player_img = pg.image.load(os.path.join(img_Folder, "playerShip1_orange.png")).convert()
    player_mini_img = pg.transform.scale(player_img, (40, 30))
    player_mini_img.set_colorkey(BLACK)

    pow_img = {}
    pow_img[pow_list[0]] = pg.image.load(os.path.join(img_Folder, "shield_gold.png")).convert()
    pow_img[pow_list[1]] = pg.image.load(os.path.join(img_Folder, "bolt_gold.png")).convert()
    pow_img[pow_list[2]] = pg.transform.scale(player_mini_img, (20, 20))

    bullet_img = pg.image.load(os.path.join(img_Folder, "laserRed16.png")).convert()

    # load sounds
    shoot_snd = pg.mixer.Sound(os.path.join(fx_folder, "pew.wav"))
    exp_name = ["expl3.wav", "expl6.wav"]
    expsnd = []
    for snd in exp_name:
        expsnd.append(pg.mixer.Sound(os.path.join(fx_folder, snd)))

    pow_snd = pg.mixer.Sound(os.path.join(fx_folder, "Upgrade1.wav"))

    music = pg.mixer.music.load(os.path.join(music_folder, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
    pg.mixer.music.set_volume(0.5)



    pg.mixer.music.play(loops=-1)

    # Setup Game loop____________________________
    while running:
        if game_over:
            show_gameOver_screen(screen, background, bg_rect, clock)
            game_over = False
            # Create sprite groups
            all_sprites = pg.sprite.Group()
            player_group = pg.sprite.Group()
            enemy_group = pg.sprite.Group()
            bullet_group = pg.sprite.Group()
            pow_group = pg.sprite.Group()
            # create objects and add to groups
            for i in range(150):
                star = Star()
                all_sprites.add(star)
            player = Player(player_img, bullet_img, all_sprites, bullet_group, shoot_snd)
            all_sprites.add(player)
            player_group.add(player)
            for i in range(20):
                enemy = Mob(random.choice(meteor_img_list))
                all_sprites.add(enemy)
                enemy_group.add(enemy)
        # Update clock_________________
        clock.tick(FPS)

        # Process events_______________
        for event in pg.event.get():
            # Key down events
            if event.type == pg.KEYDOWN:

                # If esc is pressed, close the program
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    player.shooting = False




            # If the red X was clicked, close the program
            if event.type == pg.QUIT:
                running = False
        # collision between player sprite and enemy group
        hits = pg.sprite.spritecollide(player, enemy_group, True, pg.sprite.collide_circle)
        if hits:
            for hit in hits:

                random.choice(expsnd).play()
                player.takeDamage(hit)
                size = "lg"
                if hit.radius < 25:
                    size = "sm"

                expl = Explosion(hit.rect.center, size, explosion_anim)
                all_sprites.add(expl)

                enemy = Mob(random.choice(meteor_img_list))
                all_sprites.add(enemy)
                enemy_group.add(enemy)

            if player.shield <= 0:
                expl = Explosion(player.rect.center, "playerExp", explosion_anim)
                all_sprites.add(expl)
                player.die()

        if player.lives <= 0 and not expl.alive():
            game_over = True
              # take damage
            # play sound
            # play animation
        # collision between bullet group and enemy group
        hits = pg.sprite.groupcollide(enemy_group, bullet_group, True, True)
        if hits:
            random.choice(expsnd).play()
            for hit in hits:
                score += int(100 - hit.radius)
                size = "lg"
                if hit.radius < 25:
                    size = "sm"

                expl = Explosion(hit.rect.center, size, explosion_anim)
                all_sprites.add(expl)
                if random.random() > 0.95:
                    pow = Pow(hit.rect.center, pow_img)
                    pow_group.add(pow)
                    all_sprites.add(pow)
                enemy = Mob(random.choice(meteor_img_list))
                all_sprites.add(enemy)
                enemy_group.add(enemy)

        # if player hit pow
        hits = pg.sprite.spritecollide(player, pow_group, True)
        if hits:
            for hit in hits:
                if hit.type == pow_list[0]:
                    # play sound
                    # add to player shield
                    pow_snd.play()
                    player.add_shield(random.randint(25, 75))
                if hit.type == pow_list[1]:
                    pow_snd.play()
                    player.gun_up()
                if hit.type == pow_list[2]:
                    pow_snd.play()
                    player.add_life()

        # Update_______________________
        all_sprites.update()

        # Draw_________________________
        # Things that are drawn first are the farthest back

        # Background color
        screen.fill(cfBLUE)
        screen.blit(background, bg_rect)

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw HUD
        draw_Text(screen, str(score), 25, WHITE,WIDTH/2, 25)
        draw_bar(screen, 5, 30, player.shield, GREEN, "Health")
        draw_bar(screen, 5, HEIGHT-HEIGHT/30, player.ammo/5, BLUE, "Ammo")
        draw_bar(screen, 5, 60, player.shoot_delay/7, RED, "Heat")
        draw_life_img(screen, WIDTH-250, 30, player.lives, player_mini_img)


        # Must be the last thing called in the draw section
        pg.display.flip()


# Run main loop
main()

