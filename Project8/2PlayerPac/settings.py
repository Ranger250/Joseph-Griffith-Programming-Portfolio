# imports

import random
import pygame as pg
import os

# settings
TILESIZE = 24
TITLE = "Paccy"
WIDTH = TILESIZE * 28
HEIGHT = TILESIZE * 36
FPS = 30
FONT_NAME = pg.font.match_font("Comic Sans MS")
PLAYER_SPEED = 3
GHOST_SPEED = 2


# file and file names
file_name = os.path.dirname(__file__)
asset_folder = os.path.join(file_name, "assets")
img_folder = os.path.join(asset_folder, "imgs")
sound_folder = os.path.join(asset_folder, "sounds")


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
LIGHTBLUE = (0, 155, 155)
cfBLUE = (100, 149, 237)
BGCOLOR = BLACK