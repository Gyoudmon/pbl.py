import pygame

import os
import sys
import enum

###################################################################################################
_default_fontsize = 18

_system_fonts = {}
_system_fontdirs = [
    "/System/Library/Fonts",
    "/Library/Fonts",
    "C:\\Windows\\Fonts",
    "/usr/share/fonts"
]

###################################################################################################
class FontSize(enum.Enum):
    xx_small = 0x1,
    x_small = 0x2,
    small = 0x3,
    medium = 0x4,
    large = 0x5,
    x_large = 0x6,
    xx_large = 0x7

class FontFamily(enum.Enum):
    sans_serif = 0x1,
    serif = 0x2,
    cursive = 0x3,
    fantasy = 0x4,
    math = 0x5,
    monospace = 0x6,
    fangsong = 0x7,
    _ = 0x0

class GameFont:
    DEFAULT: pygame.font.Font = None
    Title: pygame.font.Font = None
    Tooltip: pygame.font.Font = None

    sans_serif: pygame.font.Font = None
    serif: pygame.font.Font = None
    cursive: pygame.font.Font = None
    fantasy: pygame.font.Font = None
    monospace: pygame.font.Font = None
    math: pygame.font.Font = None
    fangsong: pygame.font.Font = None

###################################################################################################
def GameFonts_initialize(fontsize = _default_fontsize):
    for rootdir in _system_fontdirs:
        if os.path.isdir(rootdir):
            for parent, _subdirs, fontfiles in os.walk(rootdir):
                for fontfile in fontfiles:
                    _system_fonts[fontfile] = (parent + os.sep + fontfile).encode('utf-8')

    medium_size = generic_font_size(FontSize.medium, fontsize)
    title_size = generic_font_size(FontSize.xx_large, fontsize)

    GameFont.DEFAULT = game_create_font(generic_font_family_name_for_chinese(FontFamily.serif), medium_size)
    GameFont.Title = game_create_font(generic_font_family_name_for_chinese(FontFamily.sans_serif), title_size)
    GameFont.Tooltip = game_create_font(generic_font_family_name_for_chinese(FontFamily.serif), medium_size)
    
    GameFont.sans_serif = game_create_font(generic_font_family_name_for_chinese(FontFamily.sans_serif), medium_size)
    GameFont.serif = game_create_font(generic_font_family_name_for_chinese(FontFamily.serif), medium_size)
    GameFont.cursive = game_create_font(generic_font_family_name_for_chinese(FontFamily.cursive), medium_size)
    GameFont.fantasy = game_create_font(generic_font_family_name_for_chinese(FontFamily.fantasy), medium_size)
    GameFont.monospace = game_create_font(generic_font_family_name_for_chinese(FontFamily.monospace), medium_size)
    GameFont.math = game_create_font(generic_font_family_name_for_chinese(FontFamily.math), medium_size)
    GameFont.fangsong = game_create_font(generic_font_family_name_for_chinese(FontFamily.fangsong), medium_size)
    
def GameFonts_destroy():
    if GameFont.DEFAULT != None: GameFont.DEFAULT = None
    if GameFont.Title != None: GameFont.Title = None
    if GameFont.Tooltip != None: GameFont.Tooltip = None

    if GameFont.sans_serif != None: GameFont.sans_serif = None
    if GameFont.serif != None: GameFont.serif = None
    if GameFont.monospace != None: GameFont.monospace = None
    if GameFont.math != None: GameFont.math = None
    if GameFont.fangsong != None: GameFont.fangsong = None
    if GameFont.cursive != None: GameFont.cursive = None
    if GameFont.fantasy != None: GameFont.fantasy = None

###################################################################################################
def generic_font_size(size: FontSize, normal_size = _default_fontsize):
    if size is FontSize.xx_large:   return normal_size * 2
    elif size is FontSize.x_large:  return normal_size * 3 // 2
    elif size is FontSize.large:    return normal_size * 6 // 5
    elif size is FontSize.small:    return normal_size * 8 // 9
    elif size is FontSize.x_small:  return normal_size * 3 // 4
    elif size is FontSize.xx_small: return normal_size * 3 // 5
    else: return normal_size

def generic_font_family_name_for_ascii(family: FontFamily):
    if sys.platform == 'darwin':
        if family is FontFamily.sans_serif: return "LucidaGrande.ttc"
        elif family is FontFamily.serif: return "Times New Roman.ttf"
        elif family is FontFamily.monospace: return "Courier New Bold.ttf"
        elif family is FontFamily.math: return "STIXTwoText-Italic.ttf"
        elif family is FontFamily.cursive: return "Apple Chancery.ttf"
        elif family is FontFamily.fantasy: return "Comic Sans MS.ttf"
        elif family is FontFamily.fangsong: return "PingFang.ttc"
    elif sys.platform == 'win32':
        if family is FontFamily.sans_serif: return "msyh.ttc"
        elif family is FontFamily.serif: return "times.ttf"
        elif family is FontFamily.monospace: return "cour.ttf"
        elif family is FontFamily.math: return "BOD_R.TTF"
        elif family is FontFamily.cursive: return "Courier.ttc"
        elif family is FontFamily.fantasy: return "Bodoni 72.ttc"
        elif family is FontFamily.fangsong: return "msyh.ttc"
    else:
        if family is FontFamily.sans_serif: return "Nimbus Sans.ttc"
        elif family is FontFamily.serif: return "DejaVu Serif.ttc"
        elif family is FontFamily.monospace: return "Monospace.ttf"
        elif family is FontFamily.math: return "URW Bookman.ttf"
        elif family is FontFamily.fangsong: return "Arial Unicode.ttf"
        elif family is FontFamily.cursive: return "Chancery.ttf"
        elif family is FontFamily.fantasy: return "Helvetica.ttf"
    
    return ""

def generic_font_family_name_for_chinese(family: FontFamily):
    if sys.platform == 'darwin':
        if family is FontFamily.sans_serif: return "Hiragino Sans GB.ttc"
        elif family is FontFamily.serif: return "Songti.ttc"
        elif family is FontFamily.monospace: return "STHeiti Medium.ttc"
        elif family is FontFamily.fangsong: return "Arial Unicode.ttf"
    elif sys.platform == 'win32':
        if family is FontFamily.sans_serif: return "msyh.ttc"
        elif family is FontFamily.serif: return "simkai.ttf"
        elif family is FontFamily.monospace: return "simhei.ttf"
        elif family is FontFamily.cursive: return "FZSTK.TTF"
        elif family is FontFamily.fantasy: return "STHUPO.TTF"
        elif family is FontFamily.fangsong: return "simfang.ttf"

    return generic_font_family_name_for_ascii(family)

###################################################################################################
def game_create_font(face, fontsize = _default_fontsize):
    font = None

    try:
        if face in _system_fonts:
            font = pygame.font.Font(_system_fonts[face], fontsize)
        else:
            font = pygame.font.Font(face, fontsize)
    except FileNotFoundError:
        font = pygame.font.Font(_system_fonts[generic_font_family_name_for_chinese(FontFamily.sans_serif)], fontsize)

    return font

def game_font_destroy(font, usr_only = True):
    if font:
        if not usr_only: del font
        elif font == GameFont.DEFAULT: pass
        elif font == GameFont.Title: pass
        elif font == GameFont.Tooltip: pass
        elif font == GameFont.sans_serif: pass
        elif font == GameFont.serif: pass
        elif font == GameFont.monospace: pass
        elif font == GameFont.math: pass
        elif font == GameFont.cursive: pass
        elif font == GameFont.fangsong: pass
        elif font == GameFont.fantasy: pass
        else: del font
