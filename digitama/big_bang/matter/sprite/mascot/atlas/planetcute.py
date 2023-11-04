from .....datum.path import *

from ....sprite.folder import *

###############################################################################
class GroundBlockType(enum.Enum):
    Soil = 0x45ebcaab7cadecdf
    Dirt = 0x464548c8ff4af8f3
    Grass = 0x4ec73c06758af68e
    Stone = 0x4512a993b921ff7e
    Water = 0x406319eac504dc11
    Wood = 0x416c47f3f52c75af

###############################################################################
class PlanetCuteTile(Sprite):
    def __init__(self, default_type):
        super(PlanetCuteTile, self).__init__(digimon_mascot_path("atlas/planetcute", ""))
        self.camouflage(True)

        self.__type = default_type

# public
    def get_original_margin(self, x, y):
        return 32.0, 0.0, 0.0, 0.0
    
    def get_thickness(self):
        return 25.0 * self._get_vertical_scale()
    
    def set_type(self, type):
        if self.__type != type:
            self.__type = type
            self.switch_to_costume(self.__type_to_name(self.__type))

# protected
    def _get_initial_costume_index(self):
        return self._costume_name_to_index(self.__type_to_name(self.__type))
    
# private
    def __type_to_name(self, type: GroundBlockType):
        return type.name.lower()
