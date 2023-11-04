import os.path as path

###############################################################################
def directory_path(p):
    if len(p) > 0:
        if p[-1] != path.sep:
            p += path.sep
    
    return p

def path_only(p):
    return path.dirname(p)

def file_name_from_path(p):
    return path.basename(p)

def file_basename_from_path(p):
    fn = file_name_from_path(p)
    bn, _ = path.splitext(fn)

    return bn

def file_extension_from_path(p):
    fn = file_name_from_path(p)
    _, ext = path.splitext(fn)

    return ext

###############################################################################
def enter_digimon_zone(process_path):
    global _zonedir
    
    process_path = path.realpath(process_path)

    if path.isdir(process_path):
        _zonedir = path.normpath(process_path)
    else:
        _zonedir, _ = path.split(path.normpath(process_path))

    _zonedir = directory_path(_zonedir)

def digimon_mascot_setup(shared_path):
    global _mascotdir

    if shared_path:
        folder = path.normpath(shared_path)

        if path.abspath(folder):
            _mascotdir = directory_path(folder)
        else:
            _mascotdir = digimon_subdir(folder)

def digimon_zonedir():
    return _zonedir

def digimon_subdir(dirpath):
    return digimon_zonedir() + directory_path(path.normpath(dirpath))

def digimon_mascot_rootdir():
    if _mascotdir:
        return _mascotdir
    else:
        return digimon_subdir("stone/mascot")
    
def digimon_mascot_subdir(dirpath):
    return digimon_mascot_rootdir() + directory_path(path.normpath(dirpath))

def digimon_path(file, ext = '', sub_rootdir = 'stone'):
    p = path.normpath(file)

    if ext:
        p += ext

    if sub_rootdir:
        p = directory_path(path.normpath(sub_rootdir)) + p

    return _zonedir + p

def digimon_mascot_path(file, ext = '.png', sub_rootdir = ''):
    p = path.normpath(file)

    if ext:
        p += ext

    if sub_rootdir:
        p = directory_path(path.normpath(sub_rootdir)) + p

    return digimon_mascot_rootdir() + p

###############################################################################
_zonedir = ""
_mascotdir = ""
