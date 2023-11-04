import pygame

import math   # 数学函数
import enum   # 枚举类型

from ..physics.mathematics import *

###############################################################################
class ColorMixture(enum.Enum):
    Ignore = 0
    Add = pygame.BLEND_RGB_ADD

    # Subtractive Mixture by multiplication has problem
    #  on pairs of non-primary colors,
    #  and there is no easy way to solve it
    Subtract = pygame.BLEND_RGB_SUB
    Multiple = pygame.BLEND_RGB_MULT
    
    Alpha = pygame.BLEND_ALPHA_SDL2

def color_mixture_to_blend_mode(mixture: ColorMixture):
    return mixture.value

def blend_mode_to_color_mixture(mode: int):
    return ColorMixture(mode)

###############################################################################
def rgba(cs, alpha = 0xFF):
    if isinstance(cs, int):
        c = RGBA_From_Hexadecimal_With_Alpha(cs, alpha) 
    elif isinstance(cs, float):
        c = RGBA_From_HSB_With_Alpha(cs, 1.0, 1.0, alpha)
    else:
        c = RGBA_From_HSB_With_Alpha(cs[0], cs[1], cs[2], alpha)

    return c

###############################################################################
def RGBA_From_Hexadecimal_With_Alpha(hex, alpha = 0xFF):
    r, g, b = RGB_FromHexadecimal(hex)
    a = alpha

    if isinstance(a, float):
        a = _UCHAR(a)

    return r, g, b, a

def RGBA_From_HSB_With_Alpha(hue, saturation, value, alpha = 0xFF):
    chroma = saturation * value
    m = value - chroma

    return _rgba_from_hue(hue, chroma, m, alpha)

def RGBA_From_HSV_With_Alpha(hue, saturation, value, alpha = 0xFF):
    chroma = saturation * value
    m = value - chroma

    return _rgba_from_hue(hue, chroma, m, alpha)

def RGBA_From_HSL_With_Alpha(hue, saturation, lightness, alpha = 0xFF):
    chroma = saturation * (1.0 - math.fabs(lightness * 2.0 - 1.0))
    m = lightness - chroma * 0.5
    
    return _rgba_from_hue(hue, chroma, m, alpha)

def RGBA_From_HSI_With_Alpha(hue, saturation, intensity, alpha = 0xFF):
    if (saturation == 0.0) or math.isnan(hue):
        return _color_rgba(intensity, intensity, intensity, alpha)
    elif (hue < 120.0):
        return _rgba_from_hsi_sector(hue, saturation, intensity, _R, alpha)
    elif (hue < 240.0):
        return _rgba_from_hsi_sector(hue - 120.0, saturation, intensity, _G, alpha)
    else:
        return _rgba_from_hsi_sector(hue - 240.0, saturation, intensity, _B, alpha)

###############################################################################
def Hexadecimal_From_RGB(red, green, blue):
    return (red << 16) | (green << 8) | blue

def RGB_FromHexadecimal(hex):
    return (hex >> 16) & 0xFF, (hex >> 8) & 0xFF, hex & 0xFF

def RGBA_FromHexadecimal(hex):
    return (hex >> 24) & 0xFF, (hex >> 16) & 0xFF, (hex >> 8) & 0xFF, hex & 0xFF

def RGB_Add(hex1, hex2):
    r1, g1, b1 = RGB_FromHexadecimal(hex1)
    r2, g2, b2 = RGB_FromHexadecimal(hex2)

    r = min(r1 + r2, 255)
    g = min(g1 + g2, 255)
    b = min(b1 + b2, 255)

    return Hexadecimal_From_RGB(r, g, b)

def Hue_FromRGB(c):
    if isinstance(c, int):
        red, green, blue = RGB_FromHexadecimal(c)
    else:
        red, green, blue = c[0], c[1], c[2]
        
    M = max(red, green, blue)
    m = min(red, green, blue)
    chroma = float(M) - float(m)
    
    if chroma == 0.0:
        return math.nan
    elif M == green:
        return 60.0 * ((float(blue) - float(red)) / chroma + 2.0)
    elif M == blue:
        return 60.0 * ((float(red) - float(green)) / chroma + 4.0)
    elif green < blue:
        return 60.0 * ((float(green) - float(blue)) / chroma + 6.0)
    else:
        return 60.0 * ((float(green) - float(blue)) / chroma)

###############################################################################
_R = 1
_G = 2
_B = 3

def _UCHAR(v):
    return max(0, min(round(v * 255.0), 0xFF))

def _color_rgba(r, g, b, a):
    if isinstance(a, float):
        a = _UCHAR(a)
    
    return _UCHAR(r), _UCHAR(g), _UCHAR(b), a

def _rgba_from_hue(hue, chroma, m, a):
    r = m
    g = m
    b = m

    hue = degrees_normalize(hue)
    
    if not math.isnan(hue):
        hue_60 = hue / 60.0
        flhue = math.floor(hue_60)
        fxhue = int(flhue)
        x = chroma * (1.0 - math.fabs(float(fxhue % 2) - (flhue - hue_60) - 1.0))
        
        if fxhue == 0:
            r += chroma
            g += x
        elif fxhue == 1:
            r += x
            g += chroma
        elif fxhue == 2:
            g += chroma
            b += x
        elif fxhue == 3:
            g += x
            b += chroma
        elif fxhue == 4:
            r += x
            b += chroma
        elif fxhue == 5:
            r += chroma
            b += x

    return _color_rgba(r, g, b, a)

def _rgba_from_hsi_sector(hue, saturation, intensity, color_component, alpha):
    cosH_60H = 2.0  # if hue == 0.0 or hue == 120.0

    if (hue != 0.0) and (hue != 120.0):
        H = hue * (math.pi / 180.0)
        cosH_60H = math.cos(H) / math.cos(math.pi / 3.0 - H)

    major = intensity * (1.0 + saturation * cosH_60H)
    midor = intensity * (1.0 - saturation)
    minor = (intensity * 3.0) - (major + midor)

    if color_component == _R:
        return _color_rgba(major, minor, midor, alpha)
    elif color_component == _G:
        return _color_rgba(midor, major, minor, alpha)
    else:
        return _color_rgba(minor, midor, major, alpha)
