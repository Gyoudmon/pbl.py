import enum

from .citizen import *

###############################################################################
class BracerMode(enum.Enum):
    Walk = 0x4b46627b14e9ee18
    Run = 0x43255e877b479922
    Win = 0x452bcb91e546f954
    Lose = 0x496bf1e3c24d7940

###############################################################################
class Bracer(Citizen):
    def __init__(self, name):
        super(Bracer, self).__init__(digimon_mascot_path(name, '', "trail/Bracers"))
        self.__mode = None

# public
    def switch_mode(self, mode, repeat = -1, anchor = MatterAnchor.CC):
        if self.__mode != mode:
            self.__mode = mode

            self.moor(anchor)
            cwidth, cheight = self._get_canvas_size(mode)
            self.set_virtual_canvas(cwidth, cheight)
            self.clear_moor()
        
        if mode == BracerMode.Walk:
            self._on_walk_mode(repeat)
        elif mode == BracerMode.Run:
            self._on_run_mode(repeat)
        elif mode == BracerMode.Win:
            self._on_win_mode(repeat)
        elif mode == BracerMode.Lose:
            self._on_lose_mode(repeat)

        self.clear_moor()

    def current_mode(self):
        return self.__mode

# protected
    def _on_costumes_load(self, costumes):
        super(Bracer, self)._on_costumes_load(costumes)
        self.switch_mode(BracerMode.Walk)
    
    def _on_eward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_e_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_e")
        else:
            self.play("walk_e_")

    def _on_wward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_w_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_w")
        else:
            self.play("walk_w_")

    def _on_sward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_s_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_s")
        else:
            self.play("walk_s_")

    def _on_nward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_n_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_n")
        else:
            self.play("walk_n_")

    def _on_esward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_es_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_es")
        else:
            self.play("walk_es_")

    def _on_enward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_en_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_en")
        else:
            self.play("walk_en_")

    def _on_wsward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_ws_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_ws")
        else:
            self.play("walk_ws_")

    def _on_wnward(self, theta_rad, vx, vy):
        if self.__mode == BracerMode.Run:
            self.play("run_wn_")
        elif self.__mode == BracerMode.Lose:
            self.switch_to_costume("lose_wn")
        else:
            self.play("walk_wn_")

# protected
    def _get_canvas_size(self, mode):
        if mode == BracerMode.Walk:
            return (36.0, 72.0)
        elif mode == BracerMode.Run:
            return (48.0, 72.0)
        elif mode == BracerMode.Win:
            return (90.0, 90.0)
        elif mode == BracerMode.Lose:
            return (90.0, 90.0)

    def _on_walk_mode(self, repeat):
        self._retrigger_heading_change_event()

    def _on_run_mode(self, repeat):
        self._retrigger_heading_change_event()

    def _on_win_mode(self, repeat):
        self.play("win_", repeat)

    def _on_lose_mode(self, repeat):
        self.stop()
        self._retrigger_heading_change_event()

# protected
    def _retrigger_heading_change_event(self):
        vx = self.x_speed()
        vy = self.y_speed()
        vr = self.get_velocity_direction()

        self._dispatch_heading_event(vr, vx, vy, vr)

###############################################################################
class Estelle(Bracer):
    def __init__(self):
        super(Estelle, self).__init__("Estelle")

    def _get_canvas_size(self, mode):
        return super()._get_canvas_size(mode)

class Joshua(Bracer):
    def __init__(self):
        super(Joshua, self).__init__("Joshua")

class Scherazard(Bracer):
    def __init__(self):
        super(Scherazard, self).__init__("Scherazard")

class Olivier(Bracer):
    def __init__(self):
        super(Olivier, self).__init__("Olivier")

class Klose(Bracer):
    def __init__(self):
        super(Klose, self).__init__("Klose")

class Agate(Bracer):
    def __init__(self):
        super(Agate, self).__init__("Agate")

class Tita(Bracer):
    def __init__(self):
        super(Tita, self).__init__("Tita")

    def _get_canvas_size(self, mode):
        if mode == BracerMode.Walk:
            return (48.0, 72.0)
        elif mode == BracerMode.Run:
            return (50.0, 72.0)
        else:
            return super()._get_canvas_size(mode)
    
class Zin(Bracer):
    def __init__(self):
        super(Zin, self).__init__("Zin")

    def _get_canvas_size(self, mode):
        if mode == BracerMode.Walk or mode == BracerMode.Run:
            return (64.0, 96.0)
        else:
            return super()._get_canvas_size(mode)
