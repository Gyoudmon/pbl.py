import math

from ..igraphlet import *
from ..movable import *

from ...graphics.image import *
from ...graphics.colorspace import *

###################################################################################################
class IShapelet(IGraphlet):
    def __init__(self, color = -1, border_color = -1):
        super(IShapelet, self).__init__()

        self.enable_resize(True)
        self.__geometry = None
        self.__mixture = ColorMixture.Alpha
        self.__color = _shape_color(color)
        self.__border_color = _shape_color(border_color)
        self.__alpha = 0xFF
        
    def __del__(self):
        self._invalidate_geometry()

# public
    def draw(self, renderer, flx, fly, flWidth, flHeight):
        width = round(flWidth)
        height = round(flHeight)
        
        if not self.__geometry:
            self.__geometry = game_blank_image(width + 1, height + 1)

            if self.__color >= 0:
                r, g, b = RGB_FromHexadecimal(self.__color)
                self._fill_shape(self.__geometry, width, height, r, g, b, self.__alpha)

            if self.__border_color >= 0:
                r, g, b = RGB_FromHexadecimal(self.__border_color)
                self._draw_shape(self.__geometry, width, height, r, g, b, self.__alpha)
                
        if self.__geometry:
            game_render_surface(renderer, self.__geometry, (flx, fly, flWidth, flHeight), None, self.__mixture.value)

# public
    def set_color(self, color):
        c = _shape_color(color)

        if self.__color != c:
            self.__color = c
            self._invalidate_geometry()
            self.notify_updated()

    def get_color(self):
        return self.__color

    def set_border_color(self, color):
        c = _shape_color(color)

        if self.__border_color != c:
            self.__border_color = c
            self._invalidate_geometry()
            self.notify_updated()
    
    def get_border_color(self):
        return self.__border_color
    
    def set_alpha(self, a):
        if isinstance(a, float):
            if a >= 1.0:
                a = 0xFF
            elif a <= 0.0:
                a = 0
            else:
                a = round(a * 255.0)

        if self.__alpha != a:
            self.__alpha = a
            self._invalidate_geometry()
            self.notify_updated()

    def set_color_mixture(self, mixture):
        if self.__mixture != mixture:
            self.__mixture = mixture
            self._invalidate_geometry()
            self.notify_updated()

    def get_color_hue(self):
        return Hue_FromRGB(self.__color)

# protected
    def _draw_shape(self, renderer: pygame.Surface, width, height, r, g, b, a): pass
    def _fill_shape(self, renderer: pygame.Surface, width, height, r, g, b, a): pass

# protected
    def _invalidate_geometry(self):
        if self.__geometry:
            del self.__geometry
            self.__geometry = None

###################################################################################################
class Linelet(IShapelet):
    def __init__(self, ex, ey, color):
        super(Linelet, self).__init__(color, -1)
        self.__epx = ex
        self.__epy = ey
        
    def get_extent(self, x, y):
        return abs(self.__epx), abs(self.__epy)

    def _on_resize(self, w, h, width, height):
        self.__epx *= w / width
        self.__epy *= h / height
        self._invalidate_geometry()

    def _fill_shape(self, renderer, width, height, r, g, b, a):
        x, y = 0, 0
        xn, yn = round(self.__epx), round(self.__epy)

        if xn < 0:
            x = x - xn
        
        if yn < 0:
            y = y - yn

        pygame.draw.aaline(renderer, (r, g, b, a), (x, y), (x + xn, y + yn), 1)

class HLinelet(Linelet):
    def __init__(self, width, color):
        super(HLinelet, self).__init__(width, 0.0, color)

class VLinelet(Linelet):
    def __init__(self, height, color):
        super(VLinelet, self).__init__(0.0, height, color)

###################################################################################################
class Trianglet(IShapelet):
    def __init__(self, x2, y2, x3, y3, color, border_color = -1):
        super(Trianglet, self).__init__(color, border_color)

        self.__x2, self.__y2 = x2, y2
        self.__x3, self.__y3 = x3, y3

    def get_extent(self, x, y):
        xmin = min(0.0, min(self.__x2, self.__x3))
        ymin = min(0.0, min(self.__y2, self.__y3))
        xmax = max(0.0, max(self.__x2, self.__x3))
        ymax = max(0.0, max(self.__y2, self.__y3))

        return xmax - xmin + 1.0, ymax - ymin + 1.0
    
    def _on_resize(self, w, h, width, height):
        xratio = w / width
        yratio = h / height

        self.__x2 *= xratio
        self.__y2 *= yratio
        self.__x3 *= xratio
        self.__y3 *= yratio
        self._invalidate_geometry()

    def _draw_shape(self, renderer: pygame.Surface, width, height, r, g, b, a):
        x = -min(0.0, min(self.__x2, self.__x3))
        y = -min(0.0, min(self.__y2, self.__y3))
        pts = [(x, y), (self.__x2 + x, self.__y2 + y), (self.__x3 + x, self.__y3 + y)]

        pygame.draw.polygon(renderer, (r, g, b, a), pts, 1)

    def _draw_shape(self, renderer: pygame.Surface, width, height, r, g, b, a):
        x = -min(0.0, min(self.__x2, self.__x3))
        y = -min(0.0, min(self.__y2, self.__y3))
        pts = [(x, y), (self.__x2 + x, self.__y2 + y), (self.__x3 + x, self.__y3 + y)]
        c = (r, g, b, a)
        
        pygame.draw.polygon(renderer, c, pts, 0)
        pygame.draw.polygon(renderer, c, pts, 1)

###################################################################################################
class Rectanglet(IShapelet):
    def __init__(self, width, height, color, border_color = -1):
        super(Rectanglet, self).__init__(color, border_color)
        self.__width, self.__height = width, height

    def get_extent(self, x, y):
        return self.__width, self.__height

    def _on_resize(self, w, h, width, height):
        self.__width = w
        self.__height = h
        self._invalidate_geometry()
    
    def _draw_shape(self, renderer, width, height, r, g, b, a):
        pygame.draw.rect(renderer, (r, g, b, a), pygame.Rect(0, 0, width, height), 1)

    def _fill_shape(self, renderer, width, height, r, g, b, a):
        pygame.draw.rect(renderer, (r, g, b, a), pygame.Rect(0, 0, width, height), 0)

class Squarelet(Rectanglet):
    def __init__(self, edge_size, color, border_color = -1):
        super(Squarelet, self).__init__(edge_size, edge_size, color, border_color)

class RoundedRectanglet(IShapelet):
    def __init__(self, width, height, radius, color, border_color = -1):
        super(RoundedRectanglet, self).__init__(color, border_color)
        self.__width, self.__height = width, height
        self.__radius = radius

    def get_extent(self, x, y):
        return self.__width, self.__height

    def _on_resize(self, w, h, width, height):
        self.__width = w
        self.__height = h
        self._invalidate_geometry()
    
    def _draw_shape(self, renderer, width, height, r, g, b, a):
        rad = self.__radius

        if rad < 0.0:
            rad = -min(self.__width, self.__height) * rad

        pygame.draw.rect(renderer, (r, g, b, a), pygame.Rect(0, 0, width, height), 1, round(rad))

    def _fill_shape(self, renderer, width, height, r, g, b, a):
        rad = self.__radius

        if rad < 0.0:
            rad = -min(self.__width, self.__height) * rad

        pygame.draw.rect(renderer, (r, g, b, a), pygame.Rect(0, 0, width, height), 0, round(rad))

class RoundedSquarelet(RoundedRectanglet):
    def __init__(self, edge_size, radius, color, border_color = -1):
        super(RoundedSquarelet, self).__init__(edge_size, edge_size, radius, color, border_color)

class Ellipselet(IShapelet):
    def __init__(self, aradius, bradius, color, border_color = -1):
        super(Ellipselet, self).__init__(color, border_color)
        self.__aradius, self.__bradius = aradius, bradius

    def get_extent(self, x, y):
        return self.__aradius * 2.0, self.__bradius * 2.0

    def _on_resize(self, w, h, width, height):
        self.__aradius = w * 0.5
        self.__bradius = h * 0.5
        self._invalidate_geometry()
    
    def _draw_shape(self, renderer, width, height, r, g, b, a):
        rx = round(self.__aradius) - 1
        ry = round(self.__bradius) - 1
        c = (r, g, b, a)
        
        if rx == ry:
            cx = rx + 1
            cy = ry + 1
            pygame.draw.circle(renderer, c, (cx, cy), rx, 1)
        else:
            pygame.draw.ellipse(renderer, c, pygame.Rect(0, 0, width, height), 1)

    def _fill_shape(self, renderer, width, height, r, g, b, a):
        rx = round(self.__aradius) - 1
        ry = round(self.__bradius) - 1
        c = (r, g, b, a)
        
        if rx == ry:
            center = (rx + 1, ry + 1)
            pygame.draw.circle(renderer, c, center, rx, 0)
            pygame.draw.circle(renderer, c, center, rx, 1)
        else:
            box = pygame.Rect(0, 0, width, height)
            pygame.draw.ellipse(renderer, c, box, 0)
            pygame.draw.ellipse(renderer, c, box, 1)

class Circlet(Ellipselet):
    def __init__(self, radius, color, border_color = -1):
        super(Circlet, self).__init__(radius, radius, color, border_color)

###################################################################################################
class RegularPolygonlet(IShapelet):
    def __init__(self, n, radius, color, border_color = -1, rotation = 0.0):
        super(RegularPolygonlet, self).__init__(color, border_color)
        self.__n = n
        self.__aradius, self.__bradius = radius, radius
        self.__rotation = rotation
        self.__lx, self.__rx, self.__ty, self.__by = 0.0, 0.0, 0.0, 0.0
        self.__pts = [(0, 0)] * n
        self.__initialize_vertice()

    def get_extent(self, x, y):
        return self.__rx - self.__lx + 1, self.__by - self.__ty + 1
    
    def _on_resize(self, w, h, width, height):
        self.__aradius = w / width
        self.__bradius = h / height
        self.__initialize_vertice()
        self._invalidate_geometry()

    def _draw_shape(self, renderer, width, height, r, g, b, a):
        pygame.draw.polygon(renderer, (r, g, b, a), self.__pts, 1)
    
    def _fill_shape(self, renderer, width, height, r, g, b, a):
        c = (r, g, b, a)
        pygame.draw.polygon(renderer, c, self.__pts, 0)
        pygame.draw.polygon(renderer, c, self.__pts, 1)
    
    def __initialize_vertice(self):
        start = math.radians(self.__rotation)
        delta = 2.0 * math.pi / float(self.__n)

        self.__lx = self.__aradius
        self.__ty = self.__bradius
        self.__rx = -self.__lx
        self.__by = -self.__ty

        for idx in range(0, self.__n):
            theta = start + delta * float(idx)
            this_x = self.__aradius * math.cos(theta)
            this_y = self.__bradius * math.sin(theta)
            self.__pts[idx] = (this_x, this_y)

            if self.__rx < this_x:
                self.__rx = this_x
            elif self.__lx > this_x:
                self.__lx = this_x

            if self.__by < this_y:
                self.__by = this_y
            elif self.__ty > this_y:
                self.__ty = this_y

        for idx in range(0, self.__n):
            x, y = self.__pts[idx]
            self.__pts[idx] = (x - self.__lx, y - self.__ty)

###################################################################################################
def _shape_color(src):
    if isinstance(src, int):
        return src
    elif isinstance(src, float):
        return _shape_color([src, 1.0, 1.0])
    else:
        r, g, b, _ = RGBA_From_HSB_With_Alpha(src[0], src[1], src[2], 0xFF)
        return Hexadecimal_From_RGB(r, g, b)
