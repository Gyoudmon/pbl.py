from .universe import *
from .plane import *

from .virtualization.screen.onionskin import *

import typing

###############################################################################
class _LinkedPlaneInfo(IPlaneInfo):
    def __init__(self, master):
        super(_LinkedPlaneInfo, self).__init__(master)
        self.next = None
        self.prev = None

###############################################################################
class Cosmos(Universe):
    def __init__(self, fps = 60, fgc = 0x000000, bgc = 0xFFFFFF):
        super(Cosmos, self).__init__(fps, fgc, bgc)
        
        self.__screen = OnionSkin(self)
        self.__head_plane: typing.Optional(Plane) = None
        self.__recent_plane: typing.Optional(Plane) = None

    def __del__(self):
        self.__collapse()
        self.__screen = None

# public
    def reflow(self, width, height):
        if width > 0.0 and height > 0.0:
            if self.__head_plane:
                child = self.__head_plane

                while True:
                    info = child.info
                    _reflow_plane(child, width, height)
                    child = info.next

                    if child == self.__head_plane:
                        break
    
    def update(self, count, interval, uptime):
        pass
    
    def draw(self, renderer, x, y, width, height):
        if self.__recent_plane:
            _draw_plane(renderer, self.__recent_plane, x, y, width, height)
    
    def can_exit(self):
        return self.__recent_plane and self.__recent_plane.can_exit()
    
# public
    def has_current_mission_completed(self):
        return (not self.__recent_plane) and (self.__recent_plane.has_mission_completed())
    
    def can_exit(self):
        return self.has_current_mission_completed() and self.__recent_plane is self.__recent_plane.info.next
    
    def notify_transfer(self, from_plane, to_plane):
        if from_plane:
            from_plane.on_leave(to_plane)

        if to_plane:
            to_plane.on_enter(from_plane)

# protected
    def _on_mouse_button_event(self, m, pressed):
        if self.__recent_plane:
            self.begin_update_sequence()
            x, y = m.pos
            
            if pressed:
                self.__recent_plane.on_pointer_pressed(m.button, x, y, 1)
            else:
                self.__recent_plane.on_pointer_released(m.button, x, y, 1)

            self.end_update_sequence()

    def _on_mouse_move(self, state, x, y, dx, dy):
        if self.__recent_plane:
            self.begin_update_sequence()
            self.__recent_plane.on_pointer_move(state, x, y, dx, dy)
            self.end_update_sequence()

    def _on_scroll(self, horizon, vertical, hprecise, vprecise):
        if self.__recent_plane:
            self.begin_update_sequence()
            self.__recent_plane.on_scroll(horizon, vertical, hprecise, vprecise)
            self.end_update_sequence()

    def _on_char(self, key, modifiers, repeats, pressed):
        if self.__recent_plane:
            self.begin_update_sequence()
            self.__recent_plane.on_char(key, modifiers, repeats, pressed)
            self.end_update_sequence()

# protected
    def _on_big_bang(self, width, height):
        if self.__head_plane:
            child = self.__head_plane

            while True:
                info = child.info
                _construct_plane(child, width, height)
                child = info.next

                if child == self.__head_plane:
                    break

            self.set_window_title(self.__recent_plane.name())

    def _on_game_start(self):
        if self.__recent_plane and (self.__recent_plane is self.__head_plane):
            self.notify_transfer(None, self.__recent_plane)

    def _on_elapse(self, count, interval, uptime):
        self.begin_update_sequence()

        if self.__head_plane:
            child = self.__recent_plane.info.next

            self.__recent_plane.begin_update_sequence()
            self.__recent_plane.on_elapse(count, interval, uptime)
            self.__recent_plane.end_update_sequence()

            while child != self.__recent_plane:
                child.on_elapse(count, interval, uptime)
                child = child.info.next

        self.update(count, interval, uptime)

        self.end_update_sequence()

# protected
    def _push_plane(self, plane):
        if plane.info is None:
            info = _bind_plane_owership(self.__screen, plane)

            if not self.__head_plane:
                self.__head_plane = plane
                self.__recent_plane = plane
                info.prev = self.__head_plane
            else:
                head_info = self.__head_plane.info
                prev_info = head_info.prev

                info.prev = head_info.prev
                prev_info.next = plane
                head_info.prev = plane
            
            info.next = self.__head_plane

# private
    def __collapse(self):
        self.__head_plane = None
        self.__recent_plane = None

###################################################################################################
def _bind_plane_owership(master, plane):
    plane.info = _LinkedPlaneInfo(master)
    
    return plane.info

def _construct_plane(plane, flwidth, flheight):
    plane.begin_update_sequence()

    plane.construct(flwidth, flheight)
    plane.load(flwidth, flheight)

    plane.end_update_sequence()

def _reflow_plane(plane, width, height):
    plane.reflow(width, height)

def _draw_plane(renderer, plane, x, y, width, height):
    plane.draw(renderer, x, y, width, height)
