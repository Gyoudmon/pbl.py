from ..isprite import *

from ...datum.path import *
from ...graphics.geometry import *
from ...virtualization.filesystem.imgdb import *

###############################################################################
class ISpriteSheet(ISprite):
    def __init__(self, pathname):
        super(ISpriteSheet, self).__init__()

        self.__pathname = pathname
        self.__sprite_sheet = None

        self.enable_resize(True)

    def name(self):
        return file_name_from_path(self.__pathname)

    def construct(self):
        self.__sprite_sheet = imgdb_ref(self.__pathname)

        if self.__sprite_sheet:
            self._on_sheet_load(self.__sprite_sheet)
            super().construct()

# protected
    def _get_costume_extent(self, idx):
        _, _, w, h = self._get_costume_region(idx)

        return (w, h)
        
    def _draw_costume(self, renderer, idx, src, argv):
        region = self._get_costume_region(idx)
        dst = argv['dst']
        options = 0

        if src:
            src.left += region.left
            src.top += region.top
        else:
            src = region

        game_render_surface(renderer, self.__sprite_sheet, dst, src, options)
    
# protected
    def _on_sheet_load(self, sheet): pass

# protected, abstract
    def _get_costume_region(self, idx): pass

###############################################################################
class SpriteGridSheet(ISpriteSheet):
    def __init__(self, pathname, row, col, xgap = 0, ygap = 0, inset = False):
        super().__init__(pathname)

        self._row = max(row, 1)
        self._col = max(col, 1)
        self.__cell_width, self.__cell_height = 0, 0
        self.__cell_xgap, self.__cell_ygap = xgap, ygap
        self.__cell_inset = inset

# public
    def costume_count(self):
        if self.__cell_width == 0:
            return 0
        else:
            return self._row * self._col

    def grid_cell_index(self, x, y):
        xoff, yoff = 0, 0
        cl, rw = 0, 0

        if self.__cell_inset:
            xoff = self.__cell_xgap
            yoff = self.__cell_ygap

        if self.__cell_width > 0 and self.__cell_height > 0:
            cl = (x - xoff) / (self.__cell_width  + self.__cell_xgap)
            rw = (y - yoff) / (self.__cell_height + self.__cell_ygap)

        idx = rw * self._col + cl

        return idx, rw, cl

# protected
    def _on_sheet_load(self, sheet: pygame.Surface):
        w, h = sheet.get_size()

        if self.__cell_inset:
            w -= self.__cell_xgap * 2
            h -= self.__cell_ygap * 2

        self.__cell_width  = (w - ((self._col - 1) * self.__cell_xgap)) / self._col
        self.__cell_height = (h - ((self._row - 1) * self.__cell_ygap)) / self._row

    def _get_costume_region(self, idx):
        r = int(idx) / self._col
        c = int(idx) % self._col
        xoff, yoff = 0, 0

        if self.__cell_inset:
            xoff = self.__cell_xgap
            yoff = self.__cell_ygap
        
        x = c * (self.__cell_width  + self.__cell_xgap) + xoff
        y = r * (self.__cell_height + self.__cell_ygap) + yoff

        return pygame.Rect(x, y, self.__cell_width, self.__cell_height)
    
    def _costume_index_to_name(self, idx):
        return str(idx)
