import os.path as path

from ...graphics.image import *
from ...datum.path import *

###############################################################################

def imgdb_setup(rootdir):
    global _imgdb_rootdir
    
    if rootdir:
        if not _imgdb_rootdir:
            _imgdb_rootdir = directory_path(path.normpath(path.abspath(rootdir)))

def imgdb_teardown():
    _costumes.clear()

def imgdb_ref(subpath):
    abs_path = _path_normalize(subpath)
    _, ext = path.splitext(subpath)
    surface = None

    if ext == ".png" or ext == ".svg":
        if abs_path in _costumes:
            surface = _costumes[abs_path]
        else:
            surface = _imgdb_load(abs_path)
            _costumes[abs_path] = surface
            
    return surface

def imgdb_remove(subpath):
    abs_path = _path_normalize(subpath)

    if abs_path in _costumes:
        del _costumes[abs_path]

def imgdb_build_path(subpath, filename, extension):
    abs_path = imgdb_absolute_path(subpath)

    return abs_path + filename + extension

def imgdb_absolute_path(subpath):
    return _path_normalize(subpath)

###############################################################################
_costumes = {}
_imgdb_rootdir = ""

def _path_normalize(str_path):
    if path.isabs(str_path):
        return str_path
    else:
        return _imgdb_rootdir + str_path

def _imgdb_load(abspath):
    return game_load_image(abspath)
