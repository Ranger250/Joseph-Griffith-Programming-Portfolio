from settings import *
import pygame as pg

def draw_Text(surf, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surf, text_rect)


def draw_bar(surf, x, y, pct, color, text="", size=20, txtColor=WHITE):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 25
    fill = (pct/100)*BAR_LENGTH
    outlinerect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillrect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, color, fillrect)
    pg.draw.rect(surf, WHITE, outlinerect, 2)
    draw_Text(surf, text, size, txtColor, x+BAR_LENGTH/2, y)

def draw_life_img(surf, x, y, count, img):
    if count > 5:
        count = 5
    for i in range(count):
        img_rect = img.get_rect()
        img_rect.x = x + (img.get_width() + 5)*i
        img_rect.y = y
        surf.blit(img, img_rect)