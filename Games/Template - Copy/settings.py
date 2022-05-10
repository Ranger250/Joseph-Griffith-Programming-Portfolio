# imports
import pygame as pg
import random
from os import path

# game options/settings
TITLE = "My Game"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = pg.font.match_font("ariel")
SPRITESHEET = "simpleSpace_sheet.png"


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
cfBLUE = (100, 149, 237)
BGCOLOR = cfBLUE

#player settings
PLAYER_GRAV = 0.0
PLAYER_ACC = 0.05
PLAYER_ROT_SPEED = 5