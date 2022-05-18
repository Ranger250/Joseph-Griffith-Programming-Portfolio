# imports
import pygame as pg
import random
from os import path

# game options/settings
TITLE = "My Game"
TILESIZE = 24
WIDTH = TILESIZE * 32
HEIGHT = TILESIZE * 24
FPS = 60
FONT_NAME = pg.font.match_font("ariel")

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
cfBLUE = (100, 149, 237)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BGCOLOR = DARKGREY


GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# Player setting
PLAYER_SPEED = WIDTH // 3