# Main Game File

# Installations_______________________
# install pygame with 'pip install pygame'

# Imports
from settings import *
import pygame as pg
from player import *


# Setup pygame
pg.init()
pg.mixer.init()

# Setup main function
def main():
    running = True
    # Create game objects________________________
    # Set up screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    # Create clock
    clock = pg.time.Clock()

    # Create sprite groups_____________
    all_sprites = pg.sprite.Group()
    player_group = pg.sprite.Group()

    # Create player object
    player = Player()

    # Add to sprite groups
    all_sprites.add(player)
    player_group.add(player)



    # Setup Game loop____________________________
    while running:
        # Update clock_________________
        clock.tick(FPS)

        # Process events_______________
        for event in pg.event.get():
            # Key down events
            if event.type == pg.KEYDOWN:
                # If esc is pressed, close the program
                if event.key == pg.K_ESCAPE:
                    running = False

            # If the red X was clicked, close the program
            if event.type == pg.QUIT:
                running = False

        # Update_______________________
        all_sprites.update()

        # Draw_________________________
        # Things that are drawn first are the farthest back

        # Background color
        screen.fill(cfBLUE)

        # Draw all sprites
        all_sprites.draw(screen)

        # Must be the last thing called in the draw section
        pg.display.flip()


# Run main loop
main()

