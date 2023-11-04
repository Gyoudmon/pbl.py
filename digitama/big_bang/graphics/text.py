import pygame               # PyGame 函数

import sys
import enum

from .font import *
from .colorspace import *
from .geometry import *

###################################################################################################
class TextRenderMode(enum.Enum):
    Solid = 0x44215fc76574b744
    Shaded = 0x457cf9960addbe59
    LCD = 0x4873c4e96fb8ba72
    Blender = 0x470c7b0ea6e5d96f

###################################################################################################
def game_text_size(font: pygame.font.Font, text):
    if not font: 
        font = GameFont.DEFAULT

    return font.size(text)

###################################################################################################
def game_text_surface(text, font: pygame.font.Font, mode, fgc, bgc, wrap):
    if not font:
        font = GameFont.DEFAULT
    
    if bgc:
        bg = rgba(bgc)
    else:
        bg = None

    return font.render(text, True, rgba(fgc), bg)

###################################################################################################
def game_draw_solid_text(font, renderer, rgb, x, y, text):
    message = game_text_surface(text, font, TextRenderMode.Solid, rgb, None, 0)
    _safe_render_text_surface(renderer, message, x, y)

def game_draw_shaded_text(font, renderer, fgc, bgc, x, y, text):
    message = game_text_surface(text, font, TextRenderMode.Shaded, fgc, bgc, 0)
    _safe_render_text_surface(renderer, message, x, y)

def game_draw_lcd_text(font, renderer, fgc, bgc, x, y, text):
    message = game_text_surface(text, font, TextRenderMode.LCD, fgc, bgc, 0)
    _safe_render_text_surface(renderer, message, x, y)

def game_draw_blended_text(font, renderer, rgb, x, y, text):
    message = game_text_surface(text, font, TextRenderMode.Blender, rgb, None, 0)
    _safe_render_text_surface(renderer, message, x, y)

###################################################################################################
def _safe_render_text_surface(target, message, x, y):
    if message:
        game_render_surface(target, message, [x, y])
        del message
