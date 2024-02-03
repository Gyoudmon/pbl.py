import pygame
import random

from ..imatter import *
from .movable import *

###################################################################################################
class ISprite(IMatter):
    def __init__(self):
        super(ISprite, self).__init__()
        self.__current_action_name = ""
        self.__frame_refs = []
        self.__animation_rest = 0
        self.__next_branch = -1
        self.__idle_time0 = 0

        self.__current_costume_idx = 0
        self.__canvas_width, self.__canvas_height = 0.0, 0.0
        self.__xscale, self.__yscale = 1.0, 1.0

    def construct(self):
        idx = self._get_initial_costume_index()

        if idx >= 0:
            self.switch_to_costume(idx)
        else:
            self.play_all()

    def get_extent(self, x, y):
        ow, oh = self.get_original_extent(x, y)
        w = ow * abs(self.__xscale)
        h = oh * abs(self.__yscale)

        return w, h

    def get_original_extent(self, x, y):
        if self.__current_costume_idx >= self.costume_count():
            return 0.0, 0.0
        elif self.__canvas_width > 0.0 and self.__canvas_height > 0.0:
            return self.__canvas_width, self.__canvas_height
        else:
            w, h = self._get_costume_extent(self.__current_costume_idx)

            if self.__canvas_width > 0.0:
                w = self.__canvas_width

            if self.__canvas_height > 0.0:
                h = self.__canvas_height

            return w, h
    
    def get_margin(self, x, y):
        t, r, b, l = self.get_original_margin(x, y)

        if self.__xscale >= 0.0:
            l, r = l * self.__xscale, r * self.__xscale
        else:
            l, r = -r * self.__xscale, -l * self.__xscale

        if self.__yscale >= 0.0:
            t, b = t * self.__yscale, b * self.__yscale
        else:
            t, b = -b * self.__yscale, -t * self.__yscale

        return t, r, b, l

    def get_original_margin(self, x, y):
        return 0.0, 0.0, 0.0, 0.0

    def on_resize(self, width, height, old_width, old_height):
        if self.__current_costume_idx < self.costume_count():
            cwidth, cheight = self._get_costume_extent(self.__current_costume_idx)

            if cwidth > 0.0 and cheight > 0.0:
                self.__xscale = width / cwidth
                self.__yscale = height / cheight

    def draw(self, renderer, x, y, Width, Height):
        if self.__current_costume_idx < self.costume_count():
            argv = { 'dst': pygame.Rect(x, y, Width, Height) }

            if self.__canvas_width <= 0.0 and self.__canvas_height <= 0.0:
                self._draw_costume(renderer, self.__current_costume_idx, None, argv)
            else:
                sx = abs(self.__xscale)
                sy = abs(self.__yscale)
                cwidth = self.__canvas_width
                cheight = self.__canvas_height
                width, height = self._get_costume_extent(self.__current_costume_idx)

                if cwidth <= 0.0:
                    cwidth = width

                if cheight <= 0.0:
                    cheight = height

                xoff = (cwidth - width) * 0.5 * sx
                yoff = (cheight - height) * 0.5 * sy

                if xoff > 0.0:
                    argv['dst'].left += xoff
                    argv['dst'].width -= (xoff * 2.0)

                if yoff > 0.0:
                    argv['dst'].top += yoff
                    argv['dst'].height -= (yoff * 2.0)

                if xoff >= 0.0 and yoff >= 0.0:
                    self._draw_costume(renderer, self.__current_costume_idx, None, argv)
                else:
                    src = pygame.Rect(0.0, 0.0, width, height)

                    if xoff < 0.0:
                        src.left -= xoff / sx
                        src.width -= src.left * 2.0

                    if yoff < 0.0:
                        src.top -= yoff / sy
                        src.height -= src.top * 2.0

                    self._draw_costume(renderer, self.__current_costume_idx, src, argv)

    def update(self, count, interval, uptime):
        frame_size = len(self.__frame_refs)
        duration = 0

        if frame_size > 0:
            if self.__animation_rest != 0:
                frame_idx = count % frame_size

                if frame_idx == 0:
                    if self.__next_branch >= 0:
                        self.__next_branch = self._update_action_frames(self.__frame_refs, self.__next_branch)
                        
                        if self.__frame_refs:
                            self.notify_timeline_restart(1)
                    else:
                        if self.__animation_rest > 0:
                            self.__animation_rest -= 1

                        if self.__animation_rest == 0:
                            self.__idle_time0 = uptime
                            self.stop()
                        else:
                            self.__next_branch = self._submit_action_frames(self.__frame_refs, self.__current_action_name)

                            if self.__frame_refs:
                                self.notify_timeline_restart(1)

                    if self.__frame_refs:
                        self.switch_to_costume(self.__frame_refs[0][0])
                        duration = self.__frame_refs[0][1]
                else:
                    self.switch_to_costume(self.__frame_refs[frame_idx][0])
                    duration = self.__frame_refs[frame_idx][1]
            else:
                self.__idle_time0 = uptime
                self.stop()
        elif frame_size == 0:
            idle_interval = self._preferred_idle_duration()

            if idle_interval > 0:
                if self.__idle_time0 == 0:
                    self.__idle_time0 = uptime

                if idle_interval <= (uptime - self.__idle_time0):
                    times = 1

                    self.__next_branch, times = self._submit_idle_frames(self.__frame_refs, times)

                    if self.__frame_refs:
                        self.switch_to_costume(self.__frame_refs[0][0])
                        duration = self.__frame_refs[0][1]
                        
                        if times < 1:
                            self.__animation_rest = 1
                        else:
                            self.__animation_rest = times

                        self.notify_timeline_restart(1)


        return duration

###############################################################################
    def set_virtual_canvas(self, width, height):
        if self.__canvas_width != width or self.__canvas_height != height:
            self.__canvas_width = width
            self.__canvas_height = height
            self.notify_updated()

    def auto_virtual_canvas(self, action_name):
        cwidth, cheight = 0.0, 0.0

        for idx in range(0, self.costume_count()):
            if not action_name or self._costume_index_to_name(idx).startswith(action_name):
                cw, ch = self._get_costume_extent(idx)

                if cw > cwidth:
                    cwidth = cw

                if ch > cheight:
                    cheight = ch

        self.set_virtual_canvas(cwidth, cheight)

    def switch_to_costume(self, idx):
        if isinstance(idx, int):
            maxsize = self.costume_count()

            if maxsize > 0:
                actual_idx = idx

                if actual_idx >= maxsize:
                    actual_idx %= maxsize
                elif actual_idx < 0:
                    actual_idx = maxsize - ((-actual_idx) % maxsize)
            
                if actual_idx != self.__current_costume_idx:
                    self.__current_costume_idx = actual_idx
                    self.notify_updated()
        elif isinstance(idx, str):
            cidx = self._costume_name_to_index(idx)

            if cidx >= 0:
                self.switch_to_costume(cidx)

    def switch_to_random_costume(self, idx0, idxn):
        self.switch_to_costume(self, random.randint(idx0, idxn))

###############################################################################
    def preferred_local_fps(self):
        return 10
    
    def play(self, action, repetition = -1):
        if isinstance(action, str):
            self.__play_action(action, repetition)
        else:
            self.__play_sequence(action[0], action[1], repetition)

    def play_all(self, repetition = -1):
        self.__play_sequence(0, self.costume_count(), repetition)

    def in_playing(self):
        return self.__animation_rest != 0
    
    def stop(self, rest = 0):
        self.__animation_rest = max(rest, 0)
        
        if self.__animation_rest == 0:
            self.__current_action_name = ''
            self.__frame_refs.clear()

###############################################################################
    def flip(self, horizontal = True, vertical = False): pass

###############################################################################
    def costume_count(self):
        return 0

    def greetings(self, repeat = 1):
        pass

    def goodbye(self, repeat = 1):
        pass

    def _costume_name_to_index(self, name):
        cidx = -1

        for idx in range(0, self.costume_count()):
            if self._costume_index_to_name(idx) == name:
                cidx = idx
                break

        if cidx < 0:
            for idx in range(0, self.current_count()):
                if self._costume_index_to_name(idx).startswith(name):
                    cidx = idx
                    break

        return cidx
    
    def _get_initial_costume_index(self):
        return 0
    
###############################################################################
# abstract
    def _get_costume_extent(self, idx): pass
    def _costume_index_to_name(self, idx): pass
    def _draw_costume(self, renderer, idx, src, argv): pass
    
###############################################################################
    def _preferred_idle_duration(self):
        return random.randint(2000, 4000)

    def _submit_idle_frames(self, frame_refs, times):
        return self._submit_action_frames(frame_refs, "idle"), times

    def _submit_action_frames(self, frame_refs: list, action):
        for i in range(0, self.costume_count()):
            if self._costume_index_to_name(i).startswith(action):
                frame_refs.append((i, 0))

        return -1

    def _update_action_frames(self, frame_refs, next_branch):
        return -1
    
###############################################################################
    def _get_horizontal_scale(self):
        return abs(self.__xscale)

    def _get_vertical_scale(self):
        return abs(self.__yscale)

###############################################################################
    def __play_action(self, action, repetition):
        self.__current_action_name = action
        self.__animation_rest = repetition
        self.__frame_refs.clear()
        self.__next_branch = self._submit_action_frames(self.__frame_refs, self.__current_action_name)

        if self.__frame_refs:
            self.switch_to_costume(self.__frame_refs[0][0])
            self.notify_timeline_restart(1, self.__frame_refs[0][1])

        return len(self.__frame_refs)

    def __play_sequence(self, idx0, count, repetition):
        size = self.costume_count()

        self.__current_action_name = ""
        self.__animation_rest = repetition
        self.__frame_refs.clear()
        self.__next_branch = -1

        if count >= size:
            count = count % size + size
        
        for off in range(0, count):
            self.__frame_refs.append((idx0 + off, 0))

        return len(self.__frame_refs)
