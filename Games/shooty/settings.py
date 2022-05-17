# Settings
import os
import pygame as pg
import random

# Game title
TITLE = "Template"

# Screen size
WIDTH = 650
HEIGHT = 1000

# clock speed
FPS = 30

# Difficulty
diff = "Normal"

font_name = pg.font.match_font("Comic Sans MS")

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
cfBLUE = (100, 149, 237)

pow_list = ["shield", "gun", "life"]

game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")
music_folder = os.path.join(audio_Folder, "music")
ambiant_folder = os.path.join(audio_Folder, "ambiant")
fx_folder = os.path.join(audio_Folder, "fx")
