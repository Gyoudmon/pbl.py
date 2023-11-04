import pygame                           # PyGame 函数

from .colorspace import *               # 色彩空间相关函数, 前面那个点指代相对本文件的路径
from ..physics.mathematics import *     # 图形学、线性代数相关函数

###############################################################################
def game_draw_grid(surface, row, col, cell_width, cell_height, xoff, yoff, cs, alpha = 0xFF):
    xend = xoff + col * cell_width
    yend = yoff + row * cell_height

    for c in range(0, col + 1):
        x = xoff + c * cell_width

        for r in range(0, row + 1):
            y = yoff + r * cell_height
            game_draw_line(surface, xoff, y, xend, y, cs, alpha)

        game_draw_line(surface, x, yoff, x, yend, cs, alpha)

def game_fill_grid(surface, grids, row, col, cell_width, cell_height, xoff, yoff, cs, alpha = 0xFF):
    for c in range(col):
        for r in range(row):
            if (grids[r][c] > 0):
                x = xoff + c * cell_width
                y = yoff + r * cell_height
                game_fill_rect(surface, x, y, cell_width, cell_height, cs, alpha)

###############################################################################
def game_draw_line(surface, x1, y1, x2, y2, cs, alpha = 0xFF):
    pygame.draw.line(surface, rgba(cs, alpha), (x1, y1), (x2, y2), 1)

def game_draw_rect(surface, x, y, width, height, cs, alpha = 0xFF):
    box = pygame.Rect(round(x), round(y), round(width), round(height))
    pygame.draw.rect(surface, rgba(cs, alpha), box, 1)

def game_fill_rect(surface: pygame.Surface, x, y, width, height, cs, alpha = 0xFF):
    box = pygame.Rect(round(x), round(y), round(width), round(height))
    surface.fill(rgba(cs, alpha), box)

def game_draw_square(surface, cx, cy, apothem, cs, alpha = 0xFF):
    game_draw_rect(surface, cx - apothem, cy - apothem, apothem * 2, apothem * 2, cs, alpha)

def game_fill_square(surface, cx, cy, apothem, cs, alpha = 0xFF):
    game_fill_rect(surface, cx - apothem, cy - apothem, apothem * 2, apothem * 2, cs, alpha)

def game_draw_circle(surface, cx, cy, radius, cs, alpha = 0xFF):
    pygame.draw.circle(surface, rgba(cs, alpha), (cx, cy), radius, 1)

def game_fill_circle(surface, cx, cy, radius, cs, alpha = 0xFF):
    pygame.draw.circle(surface, rgba(cs, alpha), (cx, cy), radius, 0)

def game_draw_ellipse(surface, cx, cy, aradius, bradius, cs, alpha = 0xFF):
    box = pygame.Rect(cx - aradius, cy - bradius, aradius * 2, bradius * 2)
    pygame.draw.ellipse(surface, rgba(cs, alpha), box, 1)

def game_fill_ellipse(surface, cx, cy, aradius, bradius, cs, alpha = 0xFF):
    box = pygame.Rect(cx - aradius, cy - bradius, aradius * 2, bradius * 2)
    pygame.draw.ellipse(surface, rgba(cs, alpha), box, 0)

def game_draw_regular_polygon(surface, n, cx, cy, radius, rotation, cs, alpha = 0xFF):
    __draw_regular_polygon(surface, n, cx, cy, radius, rotation, rgba(cs, alpha), 1)

def game_fill_regular_polygon(surface, n, cx, cy, radius, rotation, cs, alpha = 0xFF):
    __draw_regular_polygon(surface, n, cx, cy, radius, rotation, rgba(cs, alpha), 0)

###############################################################################
def game_render_surface(target: pygame.Surface, source: pygame.Surface, dest, src_region = None, options = 0):
    target.blit(source, dest, src_region, options)

###############################################################################
def __draw_regular_polygon(surface, n, cx, cy, r, rotation, c, width):
    # for inscribed regular polygon, the radius should be `Rcos(pi/n)`
    start = math.radians(rotation)
    delta = d_pi / float(n)

    x0 = r * math.cos(start) + cx
    y0 = r * math.sin(start) + cy

    pts = [(x0, y0)]

    for idx in range(1, n):
        theta = start + delta * float(idx)
        sx = r * math.cos(theta) + cx
        sy = r * math.sin(theta) + cy

        pts.append((sx, sy))

    pygame.draw.polygon(surface, c, pts, width)
