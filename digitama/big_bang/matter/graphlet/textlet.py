from ..igraphlet import *

from ...forward import *
from ...graphics.colorspace import *
from ...graphics.named_colors import *
from ...graphics.font import *
from ...graphics.text import *

###################################################################################################
def make_label_for_tooltip(font, fg_color = BLACK, bg_color = SNOW, bd_color = GOLD):
    tooltip = Labellet("", font, fg_color)

    tooltip.set_background_color(bg_color)
    tooltip.set_border_color(bd_color)

    return tooltip

###################################################################################################
class ITextlet(IGraphlet):
    def __init__(self):
        super(ITextlet, self).__init__()
        self.__raw = ""
        self._text_color = SILVER
        self._alpha = 1.0
        self.__background_color = WHITE
        self.__background_alpha = 0.0
        self.__border_color = CYAN
        self.__border_alpha = 0.0
        self._text_font = None
        self._text_surface = None
        self.set_text_color()

    def __def__(self):
        if self._text_surface:
            del self._text_surface
            self._text_surface = None

# public
    def set_text_color(self, color_hex = SILVER, alpha = 1.0):
        if self._text_color != color_hex or self._alpha != alpha:
            self._text_color = color_hex
            self._alpha = alpha
            self.__update_text_surface()
            self.notify_updated()

    def get_text_color(self):
        return self._text_color

    def set_background_color(self, bg_hex, alpha = 1.0):
        if self.__background_color != bg_hex or self.__background_alpha != alpha:
            self.__background_color = bg_hex
            self.__background_alpha = alpha
            self.notify_updated()

    def set_border_color(self, bd_hex, alpha = 1.0):
        if self.__border_color != bd_hex or self.__border_alpha != alpha:
            self.__border_color = bd_hex
            self.__border_alpha = alpha
            self.notify_updated()

    def set_font(self, font, anchor = MatterAnchor.LT):
        self.moor(anchor)

        if font:
            self._text_font = font
        else:
            self._text_font = GameFont.DEFAULT

        self._on_font_changed()
        self.notify_updated()

    def set_text(self, content, anchor = MatterAnchor.LT):
        self.__raw = content
        self.moor(anchor)

        if self._text_font:
            self.__update_text_surface()
        else:
            self.set_font(None, anchor)

        self.notify_updated()

# public
    def get_extent(self, x, y):
        w, h = 0.0, 0.0

        if self._text_surface:
            w, h = self._text_surface.get_size()
        else:
            w, h = super(ITextlet, self).get_extent(x, y)

        return w, h

    def draw(self, renderer, x, y, Width, Height):
        if self._text_surface:
            if self.__background_alpha > 0.0:
                game_fill_rect(renderer, x, y, Width, Height, self.__background_color, self.__background_alpha)
            
            if self.__border_alpha > 0.0:
                game_draw_rect(renderer, x + 0.5, y + 0.5, Width - 1.0, Height - 1.0, self.__border_color, self.__border_alpha)

            game_render_surface(renderer, self._text_surface, (x, y))

# protected
    def _on_font_changed(self): pass

# private
    def __update_text_surface(self):
        if self._text_surface:
            del self._text_surface

        if self.__raw:
            self._text_surface = game_text_surface(self.__raw, self._text_font,
                TextRenderMode.Blender, self._text_color, None, 0)
        else:
            self._text_surface = None            

###################################################################################################
class Labellet(ITextlet):
    def __init__(self, caption, font, color_hex = -1, alpha = 1.0):
        super(Labellet, self).__init__()

        if font:
            self.set_font(font)
        
        if color_hex >= 0:
            self.set_text_color(color_hex, alpha)

        self.set_text(caption)
