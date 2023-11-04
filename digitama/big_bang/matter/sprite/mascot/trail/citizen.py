import os
import os.path as path
import random

from ...folder import *

from .....datum.path import *
from .....physics.motion.map2d import *

###############################################################################
class Citizen(Sprite, I8WayMotion):
    @staticmethod
    def list_special_names():
        return _list_citizen_names(_TRAIL_SPECIALS_PATH)
    
    @staticmethod
    def create_special(name):
        return Citizen(digimon_mascot_path(name, '', _TRAIL_SPECIALS_PATH))

# public
    def __init__(self, fullname):
        super(Citizen, self).__init__(fullname)
        self.set_virtual_canvas(36.0, 72.0)

# public
    def construct(self):
        super(Citizen, self).construct()
        self.play("walk_s")
    
    def preferred_loacal_fps(self):
        return 15
    
# protected
    def _on_heading_changed(self, theta_rad, vx, vy, prev_vr):
        self._dispatch_heading_event(theta_rad, vx, vy, prev_vr)

# protected
    def _on_eward(self, theta_rad, vx, vy):
        self.play("walk_e_")

    def _on_wward(self, theta_rad, vx, vy):
        self.play("walk_w_")

    def _on_sward(self, theta_rad, vx, vy):
        self.play("walk_s_")

    def _on_nward(self, theta_rad, vx, vy):
        self.play("walk_n_")

    def _on_esward(self, theta_rad, vx, vy):
        self.play("walk_es_")

    def _on_enward(self, theta_rad, vx, vy):
        self.play("walk_en_")

    def _on_wsward(self, theta_rad, vx, vy):
        self.play("walk_ws_")

    def _on_wnward(self, theta_rad, vx, vy):
        self.play("walk_wn_")

###############################################################################
class TrailKid(Citizen):
    @classmethod
    def list_names(cls):
        return _list_citizen_names(_TRAIL_KIDS_PATH)
    
    @classmethod
    def randomly_create(cls):
        names = TrailKid.list_names()
        kid = None
    
        if names:
            kid = TrailKid(names[random.randrange(len(names))])

        return kid

# public
    def __init__(self, name):
        super(TrailKid, self).__init__(digimon_mascot_path(name, '', _TRAIL_KIDS_PATH))
        self.set_virtual_canvas(32.0, 56.0)

class TrailStudent(Citizen):
    @classmethod
    def list_names(cls):
        return _list_citizen_names(_TRAIL_STUDENTS_PATH)
    
    @classmethod
    def randomly_create(cls):
        names = TrailStudent.list_names()
        student = None
    
        if names:
            student = TrailStudent(names[random.randrange(len(names))])

        return student

# public
    def __init__(self, name):
        super(TrailStudent, self).__init__(digimon_mascot_path(name, '', _TRAIL_STUDENTS_PATH))
        self.set_virtual_canvas(32.0, 68.0)

###############################################################################
_TRAIL_KIDS_PATH = "trail/Kids"
_TRAIL_STUDENTS_PATH = "trail/Students"
_TRAIL_SPECIALS_PATH = "trail/Specials"

def _list_citizen_names(subdir):
    rootdir = digimon_mascot_subdir(subdir)
    names = []

    for name in os.listdir(rootdir):
        entry = path.join(rootdir, name)

        if path.isdir(entry):
            names.append(name)

    return names
