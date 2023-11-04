import os
import os.path as path

from ..isprite import *

from ...datum.path import *
from ...graphics.geometry import *
from ...virtualization.filesystem.imgdb import *

###############################################################################
class Sprite(ISprite):
    def __init__(self, pathname):
        super().__init__()

        self.__pathname = pathname
        self.__current_decorate = ""
        self.__costumes = []
        self.__decorates = {}

        self.enable_resize(True)

    def name(self):
        return file_name_from_path(self.__pathname)

    def construct(self):
        target = imgdb_absolute_path(self.__pathname)

        if path.exists(target):
            if path.isdir(target):
                for fname in os.listdir(target):
                    entry = path.join(target, fname)
                    
                    if path.isfile(entry):
                        self.__load_costume(entry)
                    elif path.isdir(entry):
                        decorate_name = fname

                        for dname in os.listdir(entry):
                            subentry = path.join(entry, dname)

                            if path.isfile(subentry):
                                self.__load_decorate(decorate_name, subentry)
                self.__costumes.sort(key = lambda c: c[0])
            else:
                self.__load_costume(self.__pathname)

            self._on_costumes_load(self.__costumes)
            super().construct()

# public
    def wear(self, name):
        if name in self.__decorates:
            self.__current_decorate = name
            self.notify_updated()

    def is_wearing(self):
        return len(self.__current_decorate) > 0
    
    def decorate_name(self):
        return self.__current_decorate

    def take_off(self):
        if not self.__current_decorate:
            self.__current_decorate = ''
            self.notify_updated()

    def costume_count(self):
        return len(self.__costumes)

# protected
    def _get_costume_extent(self, idx):
        return self.__costumes[idx][1].get_size()
    
    def _costume_index_to_name(self, idx):
        return self.__costumes[idx][0]
    
    def _draw_costume(self, renderer, idx, src, argv):
        dst = argv['dst']
        options = 0

        game_render_surface(renderer, self.__costumes[idx][1], dst, src, options)

        if self.__current_decorate:
            c_name = self.__costumes[idx][0]
            decorate = self.__decorates[self.__current_decorate]

            if c_name in decorate:
                game_render_surface(renderer, decorate[c_name], dst, src, options)
    
# protected
    def _on_costumes_load(self, costumes): pass

# private
    def __load_costume(self, png):
        costume = imgdb_ref(png)

        if costume:
            name = file_basename_from_path(png)
            self.__costumes.append((name, costume))

    def __load_decorate(self, d_name, png):
        deco_costume = imgdb_ref(png)

        if deco_costume:
            c_name = file_basename_from_path(png)
            self.__decorates[d_name][c_name] = deco_costume
