import pygame
import math
import typing

from .virtualization.iscreen import *
from .graphics.colorspace import *

from .misc import *
from .imatter import *
from .matter.movable import *

from .physics.mathematics import *

###############################################################################
class IPlaneInfo(object):
    def __init__(self, master: IScreen):
        super(IPlaneInfo, self).__init__()
        self.master = master

class _GlidingMotion(object):
    def __init__(self, x, y, absolute, sec = 0.0, sec_delta = 0.0):
        self.tx = x
        self.ty = y
        self.second = sec
        self.sec_delta = sec_delta
        self.absolute = absolute

class _MatterInfo(IMatterInfo):
    def __init__(self, master):
        super(_MatterInfo, self).__init__(master)
        
        self.x, self.y = 0.0, 0.0
        self.selected = False

        self.local_frame_delta = 0
        self.local_frame_count = 0
        self.local_elapse = 0
        self.duration = 0

        # for queued motions
        self.gliding = False
        self.gliding_tx = 0.0
        self.gliding_ty = 0.0
        self.motion_queues: list[_GlidingMotion] = []
        
        self.current_step = 1.0
        self.progress_total = 1.0

        self.iasync = None
        self.next, self.prev = None, None

###############################################################################
class Plane(object):
    def __init__(self, name):
        super(Plane, self).__init__()
        self.info: typing.Optional(IPlaneInfo) = None
        self.__caption = name
        self.__background, self.__bg_alpha = 0, 0.0
        self.__mleft, self.__mtop, self.__mright, self.__mbottom = 0.0, 0.0, 0.0, 0.0
        self.__head_matter: typing.Optional(IMatter) = None
        self.__focused_matter: typing.Optional(IMatter) = None
        self.__hovering_matter: typing.Optional(IMatter) = None
        self.__hovering_mlx, self.__hovering_mly = 0.0, 0.0
        self.__hovering_mgx, self.__hovering_mgy = 0.0, 0.0
        self.__local_frame_delta, self.__local_frame_count, self.__local_elapse = 0, 1, 0
        self.__translate_x, self.__translate_y = 0.0, 0.0
        self.__scale_x, self.__scale_y = 1.0, 1.0
        self.__mission_done = False
        self.__tooltip: typing.Optional(IMatter) = None
        self.__tooltip_dx, self.__tooltip_dy = 0.0, 0.0
        self.size_cache_invalid()

    def __del__(self):
        self.erase()
        self.info = None

# public
    def name(self):
        return self.__caption

# public
    def construct(self, Width, Height): pass
    def load(self, Width, Height): pass
    def reflow(self, width, height): pass
    def update(self, count, interval, uptime): pass

    def draw(self, renderer: pygame.Surface, X, Y, Width, Height):
        dsX, dsY = max(0.0, X), max(0.0, Y)
        dsWidth, dsHeight = X + Width, Y + Height

        if self.__bg_alpha > 0.0:
            game_fill_rect(renderer, dsX, dsY, dsWidth, dsHeight, self.__background, self.__bg_alpha)

        if self.__head_matter:
            clip = pygame.Rect(0, 0, 0, 0)
            child = self.__head_matter

            while True:
                info = child.info

                if child.visible():
                    mwidth, mheight = child.get_extent(info.x, info.y)

                    mx = (info.x + self.__translate_x) * self.__scale_x + X
                    my = (info.y + self.__translate_y) * self.__scale_y + Y

                    if rectangle_overlay(mx, my, mx + mwidth, my + mheight, dsX, dsY, dsWidth, dsHeight):
                        clip.x = int(math.floor(mx))
                        clip.y = int(math.floor(my))
                        clip.w = int(math.ceil(mwidth))
                        clip.h = int(math.ceil(mheight))

                        renderer.set_clip(clip)
                        child.draw(renderer, mx, my, mwidth, mheight)

                        if info.selected:
                            renderer.set_clip(None)
                            self.draw_visible_selection(renderer, mx, my, mwidth, mheight)

                child = info.next
                if child == self.__head_matter:
                    break
            
            renderer.set_clip(None)

    def draw_visible_selection(self, renderer, x, y, width, height):
        game_draw_rect(renderer, x, y, width, height, 0x00FFFF)
    
# public
    def find_matter(self, x, y):
        found = None

        if self.__head_matter:
            head_info = self.__head_matter.info
            child = head_info.prev

            while True:
                info = child.info

                if not child.concealled():
                    sx, sy, sw, sh = _unsafe_get_matter_bound(child, info)

                    sx += (self.__translate_x * self.__scale_x)
                    sy += (self.__translate_y * self.__scale_y)

                    if flin(sx, x, sx + sw) and flin(sy, y, sy + sh):
                        if child.is_colliding_with_mouse(x - sx, y - sy):
                            found = child
                            break

                child = info.prev

                if child == head_info.prev:
                    break

        return found

    def get_matter_location(self, matter, anchor):
        info = _plane_matter_info(self, matter)
        x, y = False, 0.0

        if info:
            sx, sy, sw, sh = _unsafe_get_matter_bound(matter, info)

            if isinstance(anchor, MatterAnchor):
                fx, fy = matter_anchor_fraction(anchor)
            else:
                fx, fy = anchor

            x = sx + sw * fx
            y = sy + sh * fy

        return x, y

    def get_matter_boundary(self, matter):
        info = _plane_matter_info(self, matter)
        x, y, width, height = False, 0.0, 0.0, 0.0
        
        if info:
            x, y, width, height = _unsafe_get_matter_bound(matter, info)

        return x, y, width, height

    def get_matters_boundary(self):
        self.__recalculate_matters_extent_when_invalid()

        w = self.__mright - self.__mleft
        h = self.__mbottom - self.__mtop

        return self.__mleft, self.__mtop, w, h
    
    def bring_to_front(self, m, target = None):
        tinfo = _plane_matter_info(self, target)

        if not tinfo:
            if not self.__head_matter:
                self.bring_to_front(m, self.__head_matter.info.prev)
        else:
            sinfo = _plane_matter_info(self, m)
        
            if sinfo and (m != target):
                if tinfo.next != m:
                    sinfo.prev.info.next = sinfo.next
                    sinfo.next.info.prev = sinfo.prev
                    tinfo.next.info.prev = m
                    sinfo.prev = target
                    sinfo.next = tinfo.next
                    tinfo.next = m

                if self.head_matter == m:
                    self.head_matter = sinfo.next
            
                self.notify_updated()

    def bring_forward(self, m, n = 1):
        sinfo = _plane_matter_info(self, m)
    
        if sinfo:
            sentry = self.__head_matter.info.prev
            target = m

            while (target != sentry) and (n > 0):
                n = n - 1
                target = target.info.next

            self.bring_to_front(m, target)

    def send_to_back(self, m, target = None):
        tinfo = _plane_matter_info(self, target)

        if not tinfo:
            if not self.__head_matter:
                self.send_to_back(m, self.__head_matter)
        else:
            sinfo = _plane_matter_info(self, m)
        
            if sinfo and (m != target):
                if tinfo.prev != m:
                    sinfo.prev.info.next = sinfo.next
                    sinfo.next.info.prev = sinfo.prev
                    tinfo.prev.info.next = m
                    sinfo.next = target
                    sinfo.prev = tinfo.prev
                    tinfo.prev = m

                if self.__head_matter == target:
                    self.__head_matter = m

                self.notify_updated()

    def send_backward(self, m, n = 1):
        sinfo = _plane_matter_info(self, m)
    
        if sinfo:
            target = m

            while (target != self.__head_matter) and (n > 0):
                n = n - 1
                target = target.info.prev

            self.send_to_back(m, target)

    def insert(self, matter: IMatter, x = 0.0, y = 0.0, anchor: MatterAnchor = MatterAnchor.LT, dx = 0.0, dy = 0.0):
        if matter.info is None:
            fx, fy = matter_anchor_fraction(anchor)
            
            info = _bind_matter_owership(self, matter)
            if not self.__head_matter:
                self.__head_matter = matter
                info.prev = self.__head_matter
            else:
                head_info = self.__head_matter.info
                prev_info = head_info.prev.info

                info.prev = head_info.prev
                prev_info.next = matter
                head_info.prev = matter
            info.next = self.__head_matter

            self.begin_update_sequence()
            matter.construct()
            self.__move_matter_to_target_via_info(matter, info, x, y, fx, fy, dx, dy)
            
            if matter.ready():
                if self.__scale_x != 1.0 or self.__scale_y != 1.0:
                    self.__do_resize(matter, info, fx, fy, self.__scale_x, self.__scale_y)

                self.notify_updated()
                self.on_matter_ready(matter)
            else:
                self.notify_updated()
            
            self.end_update_sequence()

        return matter

    def move(self, matter: IMatter, x, y, ignore_gliding = False):
        if matter:
            info = _plane_matter_info(self, matter)

            if info:
                if self.__move_matter_via_info(matter, info, x, y, False, ignore_gliding):
                    self.notify_updated()
        elif self.__head_matter:
            child = self.__head_matter

            while True:
                info = child.info

                if info.selected:
                    self.__move_matter_via_info(child, info, x, y, False, ignore_gliding)

                child = info.next
                if child == self.__head_matter:
                    break
            
            self.notify_update()
    
    def glide(self, sec, matter: IMatter, x, y):
        info = _plane_matter_info(self, matter)

        if info:
            if self.__glide_matter_via_info(matter, info, sec, x, y, False):
                self.notify_updated()
        elif self.__head_matter:
            child = self.__head_matter

            while True:
                info = child.info

                if info.selected:
                    self.__glide_matter_via_info(child, info, sec, x, y, False)

                child = info.next
                if child == self.__head_matter:
                    break
            
            self.notify_update()

    def move_to(self, matter: IMatter, target, anchor: MatterAnchor = MatterAnchor.LT, dx = 0.0, dy = 0.0):
        info = _plane_matter_info(self, matter)
        
        if info:
            pos = self.__extract_moving_target_info(target)
            
            if isinstance(pos, tuple):
                fx, fy = matter_anchor_fraction(anchor)
            
                if self.__move_matter_to_target_via_info(matter, info, pos[0], pos[1], fx, fy, dx, dy):
                    self.notify_updated()

    def glide_to(self, sec, matter: IMatter, target, anchor: MatterAnchor = MatterAnchor.LT, dx = 0.0, dy = 0.0):
        info = _plane_matter_info(self, matter)
        
        if info:
            pos = self.__extract_moving_target_info(target)
            
            if isinstance(pos, tuple):
                fx, fy = matter_anchor_fraction(anchor)
            
                if self.__glide_matter_to_target_via_info(matter, info, sec, pos[0], pos[1], fx, fy, dx, dy):
                    self.notify_updated()

    def glide_to_mouse(self, sec, matter: IMatter, anchor: MatterAnchor = MatterAnchor.CC, dx = 1.0, dy = 1.0):
        mx, my = get_current_mouse_location()
        self.glide_to(sec, matter, (mx, my), anchor, dx, dy)
    
    def remove(self, matter: IMatter):
        info = _plane_matter_info(self, matter)

        if info:
            prev_info = info.prev
            next_info = info.next

            prev_info.next = info.next
            next_info.prev = info.prev

            if self.__head_matter == matter:
                if self.__head_matter == info.next:
                    self.__head_matter = None
                else:
                    self.__head_matter = info.next

            if self.__hovering_matter == matter:
                self.__hovering_matter = None
            
            self.notify_updated()
            self.size_cache_invalid()
    
    def erase(self):
        self.__head_matter = None
        self.size_cache_invalid()

    def size_cache_invalid(self):
        self.__mright = self.__mleft - 1.0

    def is_colliding(self, matter: IMatter, target):
        '''
        the target can be shaped as one of
                target_matter
                (target_matter, target_anchor)
                (target_matter, target_x_fraction, target_y_fraction)
        '''

        okay = False

        slx, sty, sw, sh = self.get_matter_boundary(matter)

        if slx is not False:
            if isinstance(target, IMatter):
                tlx, tty, tw, th = self.get_matter_boundary(target)

                if tlx is not False:
                    srx, sby = slx + sw, sty + sh
                    trx, tby = tlx + tw, tty + th

                    okay = rectangle_overlay(slx, sty, srx, sby, tlx, tty, trx, tby)
            else:
                if len(target) == 2:
                    tx, ty = self.get_matter_location(target[0], target[1])
                elif len(target) == 3:
                    tx, ty = self.get_matter_location(target[0], (target[1], target[2]))

                if tx is not False:
                    okay = rectangle_contain(slx, sty, slx + sw, sty + sh, tx, ty)

        return okay

# public
    def find_next_selected_matter(self, start = None):
        found = None

        if start:
            if self.__head_matter:
                found = _do_search_selected_matter(self.__head_matter, self.__mode, self.__head_matter)
        else:
            info = _plane_matter_info(self, start)

            if info:
                found = _do_search_selected_matter(info.next, self.__mode, self.__head_matter)

        return found

    def add_selected(self, m):
        if self.can_select_multiple():
            info = _plane_matter_info(self, m)

            if info and not info.selected:
                if self.can_select(m):
                    _unsafe_add_selected(self, m, info)
    
    def set_selected(self, m):
        info = _plane_matter_info(self, m)

        if info and not info.selected:
            if self.can_select(m):
                _unsafe_set_selected(self, m, info)
    
    def no_selected(self):
        if self.__head_matter:
            child = self.__head_matter

            self.begin_update_sequence()

            while True:
                info = child.info

                if info.selected:
                    self.before_select(child, False)
                    info.selected = False
                    self.after_select(child, False)
                    self.notify_updated()

                child = info.next
                if child == self.__head_matter:
                    break

            self.end_update_sequence()
    
    def count_selected(self):
        n = 0

        if self.__head_matter:
            child = self.__head_matter

            while True:
                info = child.info

                if info.selected:
                    n += 1

                child = info.next
                if child == self.__head_matter:
                    break

        return n
    
    def is_selected(self, m):
        info = _plane_matter_info(self, m)
        selected = False

        if info:
            selected = info.selected

        return selected

    def set_background(self, c_hex, a = 1.0):
        self.__background = c_hex
        self.__bg_alpha = a

# public
    def on_pointer_pressed(self, button, x, y, clicks):
        handled = False

        if button == 1:
            unmasked_matter = self.find_matter(x, y)

            if unmasked_matter:
                info = unmasked_matter.info

                if not info.selected:    
                    self.set_caret_owner(unmasked_matter)
                    self.no_selected()

                if unmasked_matter.low_level_events_allowed():
                    local_x = x - info.x
                    local_y = y - info.y
                    handled = unmasked_matter.on_pointer_pressed(button, local_x, local_y)
            else:
                self.set_caret_owner(unmasked_matter)
                self.no_selected()

        return handled

    def on_pointer_released(self, button, x, y, clicks):
        handled = False

        if button == 1:
            unmasked_matter = self.find_matter(x, y)

            if unmasked_matter:
                info = unmasked_matter.info
                local_x = x - info.x
                local_y = y - info.y
                    
                if unmasked_matter.events_allowed():
                    if clicks == 1:
                        unmasked_matter.on_tap(local_x, local_y)

                    if unmasked_matter.low_level_events_allowed():
                        unmasked_matter.on_pointer_released(button, local_x, local_y, clicks)

                if clicks == 1:
                    if info.selected:
                        self.on_tap_selected(unmasked_matter, local_x, local_y)
                    else:
                        self.on_tap(unmasked_matter, local_x, local_y)

                    handled = info.selected
                else:
                    # leave for the sentry 
                    pass

        return handled

    def on_pointer_move(self, state, x, y, dx, dy):
        handled = False

        if state == 0:
            unmasked_matter = self.find_matter(x, y)

            if (unmasked_matter is None) or (unmasked_matter is not self.__hovering_matter):
                if unmasked_matter and (not unmasked_matter.concealled()):
                    self.__say_goodbye_to_hover_matter(state, x, y, dx, dy)

                if self.__tooltip and self.__tooltip.visible() and self.__tooltip is not unmasked_matter:
                    self.__tooltip.show(False)

            if unmasked_matter:
                info = unmasked_matter.info
                local_x = x - info.x
                local_y = y - info.y
                
                if not unmasked_matter.concealled():
                    self.__hovering_matter = unmasked_matter
                    self.__hovering_mgx = x
                    self.__hovering_mgy = y
                    self.__hovering_mlx = local_x
                    self.__hovering_mly = local_y

                    if unmasked_matter.events_allowed():
                        unmasked_matter.on_havor(local_x, local_y)

                        if unmasked_matter.low_level_events_allowed():
                            unmasked_matter.on_pointer_move(state, local_x, local_y)
                
                    self.on_hover(self.__hovering_matter, local_x, local_y)
                    handled = True
            
                if self.__tooltip:
                    if self.update_tooltip(unmasked_matter, local_x, local_y, x, y):
                        if not self.__tooltip.visible():
                            self.__tooltip.show(True)

                        self.__place_tooltip(unmasked_matter)

        return handled

    def on_scroll(self, horizon, vertical, hprecise, vprecise):
        return False

# public
    # do nothing by default
    def on_focus(self, m, on_off): pass
    def on_hover(self, m, local_x, local_y): pass
    def on_goodbye(self, m, local_x, local_y): pass
    def on_save(self): pass

    def on_char(self, key, modifiers, repeats, pressed):
        if self.__focused_matter:
            self.__focused_matter.on_char(key, modifiers, repeats, pressed)

    def on_tap(self, m, local_x, local_y):
        if m:
            info = m.info

            if not info.selected:
                if self.can_select(m):
                    _unsafe_set_selected(self, m, info)

                    if m.events_allowed():
                        self.set_caret_owner(m)

                    if self.__tooltip and self.__tooltip.visible():
                        self.update_tooltip(m, local_x, local_y, local_x + info.x, local_y + info.y)
                        self.__place_tooltip(m)
                else:
                    self.no_selected()

    def on_tap_selected(self, m, local_x, local_y): pass
    
    def on_elapse(self, count, interval, uptime):
        if self.__head_matter:
            child = self.__head_matter

            while True:
                dwidth, dheight = self.info.master.get_extent()
                info: _MatterInfo = child.info
                
                local_interval, local_elapse = _local_timeline_elapse(interval, info.local_frame_delta, info.local_elapse, info.duration)
                info.local_elapse = local_elapse

                if local_interval > 0:
                    info.duration = child.update(info.local_frame_count, local_interval, uptime)
                    info.local_frame_count += 1

                # Yes, do moving separately to make it more smooth
                self.__do_motion_moving(child, info, dwidth, dheight)
                    
                child = info.next

                if child == self.__head_matter:
                    break
        
        local_interval, local_elapse = _local_timeline_elapse(interval, self.__local_frame_delta, self.__local_elapse, 0)
        self.__local_elapse = local_elapse

        if local_interval > 0:
            self.update(self.__local_frame_count, local_interval, uptime)
            self.__local_frame_count += 1

            if self.__tooltip and self.__tooltip.visible():
                if self.__hovering_matter:
                    self.update_tooltip(self.__hovering_matter, self.__hovering_mlx, self.__hovering_mly, self.__hovering_mgx, self.__hovering_mgy)
                    self.__place_tooltip(self.__hovering_matter)
    
# public
    def on_enter(self, from_plane):
        width, height = self.info.master.get_client_extent()
        self.on_mission_start(width, height)

    def on_leave(self, to_plane):
        # the completion of mission doesn't imply leaving
        pass

    def has_mission_completed(self):
        return self.__mission_done

    def mission_complete(self):
        self.on_mission_complete()
        self.__mission_done = True

    def on_mission_start(self, width, height): pass
    def on_mission_complete(self): pass

    def on_motion_start(self, m, sec, x, y, xspd, yspd): pass
    def on_motion_step(self, m, x, y, xspd, yspd, percentage): pass
    def on_motion_complete(self, m, x, y, xspd, yspd): pass

# public
    def set_tooltip_matter(self, m, dx = 0.0, dy = 0.0):
        self.begin_update_sequence()

        self.__tooltip = m
        self.__tooltip.show(False)
        self.__tooltip_dx = dx
        self.__tooltip_dy = dy

        self.end_update_sequence()

    def update_tooltip(self, matter: IMatter, local_x, local_y, global_x, global_y):
        pass

# public, do nothing by default
    def can_interactive_move(self, m, local_x, local_y): return False
    def can_select(self, m): return False
    def can_select_multiple(self): return False
    def before_select(self, m, on_or_off): pass
    def after_select(self, m, on_or_off): pass
        
# public
    def get_focused_matter(self):
        if self.matter_unmasked(self.__focused_matter):
            m = self.__focused_matter
        else:
            m = None

        return m
    
    def set_caret_owner(self, m):
        if self.__focused_matter != m:
            if m and m.events_allowed():
                info = _plane_matter_info(self, m)

                if info:
                    if self.__focused_matter:
                        self.__focused_matter.own_caret(False)
                        self.on_focus(self.__focused_matter, False)
                    
                    self.__focused_matter = m
                    m.own_caret(True)
                    self.on_focus(m, True)
            elif self.__focused_matter:
                self.__focused_matter.own_caret(False)
                self.on_focus(self.__focused_matter, False)
                self.__focused_matter = None
        elif m:
            self.on_focus(m, True)

    def notify_matter_ready(self, m):
        info: _MatterInfo = _plane_matter_info(self, m)

        if info and info.iasync:
            self.size_cache_invalid()
            self.begin_update_sequence()

            self.__glide_matter_to_target_via_info(m, info,
                    info.iasync['second'],
                    info.iasync['x0'], info.iasync['y0'],
                    info.iasync['fx0'], info.iasync['fy0'],
                    info.iasync['dx0'], info.iasync['dy0'])
                
            if self.__scale_x != 1.0 or self.__scale_y != 1.0:
                self.__do_resize(m, info, 
                        info.iasync['fx0'], info.iasync['fy0'],
                        self.__scale_x, self.__scale_y)
                
            info.iasync = None

            self.notify_updated()
            self.on_matter_ready(m)
            self.end_update_sequence()

    def on_matter_ready(self, m): pass

# public
    def begin_update_sequence(self):
        if self.info:
            self.info.master.begin_update_sequence()

    def is_in_update_sequence(self):
        if self.info:
            self.info.master.is_in_update_sequence()
        
    def end_update_sequence(self):
        if self.info:
            self.info.master.end_update_sequence()
        
    def should_update(self):
        if self.info:
            self.info.master.should_update()
        
    def notify_updated(self):
        if self.info:
            self.info.master.notify_updated()

# public
    def set_matter_fps(self, m: IMatter, fps, restart = False):
        info = _plane_matter_info(self, m)

        if info:
            _unsafe_set_matter_fps(info, fps, restart)

    def set_local_fps(self, fps, restart = False):
        df, fc, e = _unsafe_set_local_fps(fps, restart, self.__local_frame_delta, self.__local_frame_count, self.__local_elapse)
        self.__local_frame_delta = df
        self.__local_frame_count = fc
        self.__local_elapse = e

    def notify_matter_timeline_restart(self, m: IMatter, count0, duration):
        info = _plane_matter_info(self, m)

        if info:
            info.duration = duration
            info.local_frame_count = count0
            info.local_elapse = 0  

# private
    def __do_resize(self, m: IMatter, info, fx, fy, scale_x, scale_y, prev_scale_x = 1.0, prev_scale_y = 1.0):
        if m.resizable():
            sx, sy, sw, sh = _unsafe_get_matter_bound(m, info)

            m.resize(sw / prev_scale_x * scale_x, sh / prev_scale_y * scale_y)
            nw, nh = m.get_extent(sx, sy)

            nx = sx + (sw - nw) * fx
            ny = sy + (sh - nh) * fy

            self.__do_moving_via_info(m, info, nx, ny, True)

    def __recalculate_matters_extent_when_invalid(self):
        if self.__mright < self.__mleft:
            if self.__head_matter:
                child = self.__head_matter
                self.__mleft, self.__mtop = math.inf, math.inf
                self.__mright, self.__mbottom = -math.inf, -math.inf

                while True:
                    info = child.info

                    x, y, w, h = _unsafe_get_matter_bound(child, info)
                    self.__mleft = min(self.__mleft, x)
                    self.__mright = max(self.__mright, x + w)
                    self.__mtop = min(self.__mtop, y)
                    self.__mbottom = max(self.__mbottom, y + h)

                    child = info.next
                    if child == self.__head_matter:
                        break
            else:
                self.__mleft, self.__mtop = 0.0, 0.0
                self.__mright, self.__mbottom = 0.0, 0.0

    def __say_goodbye_to_hover_matter(self, state, x, y, dx, dy):
        done = False

        if self.__hovering_matter:
            info = self.__hovering_matter.info
            local_x = x - info.x
            local_y = y - info.y

            if self.__hovering_matter.events_allowed():
                done |= self.__hovering_matter.on_goodbye(local_x, local_y)

                if self.__hovering_matter.low_level_events_allowed():
                    done |= self.__hovering_matter.on_pointer_move(state, local_x, local_y, dx, dy, True)

                self.on_goodbye(self.__hovering_matter, local_x, local_y)
                self.__hovering_matter = None

        return done
    
    def __extract_moving_target_info(self, target):
        '''
        the target position, which can be shaped as one of
                (x, y)
                (target_matter, target_anchor)
                (target_matter, target_x_fraction, target_y_fraction)
                (target_matter_for_x, x_fraction, target_matter_for_y, y_fraction)
        '''

        pos = False
        target_shape = len(target)
            
        if target_shape == 2:
            if isinstance(target[0], IMatter):
                tinfo = _plane_matter_info(self, target[0])

                if tinfo:
                    tx, ty, tw, th = _unsafe_get_matter_bound(target[0], tinfo)
                    tfx, tfy = matter_anchor_fraction(target[1])
                    pos = (tx + tw * tfx, ty + th * tfy)
            else:
                pos = target
        elif target_shape == 3:
            tinfo = _plane_matter_info(self, target[0])

            if tinfo:
                tx, ty, tw, th = _unsafe_get_matter_bound(target[0], tinfo)
                pos = (tx + tw * target[1], ty + th * target[2])
        else:
            xinfo = _plane_matter_info(self, target[0])
            yinfo = _plane_matter_info(self, target[2])

            if xinfo and yinfo:
                xtx, _, xtw, _ = _unsafe_get_matter_bound(target[0], xinfo)
                _, yty, _, yth = _unsafe_get_matter_bound(target[2], yinfo)
                pos = (xtx + xtw * target[1], yty + yth * target[2])

        return pos
    
    def __place_tooltip(self, target):
        self.move_to(self.__tooltip, (target, MatterAnchor.LB), MatterAnchor.LT, self.__tooltip_dx, self.__tooltip_dy)
        
        width, height = self.info.master.get_client_extent()
        ttx, tty = self.get_matter_location(self.__tooltip, MatterAnchor.LB)

        if tty > height:
            self.move_to(self.__tooltip, (target, MatterAnchor.LT), MatterAnchor.LB, self.__tooltip_dx, self.__tooltip_dy)

        if ttx < 0.0:
            self.move(self.__tooltip, -ttx, 0.0)
        else:
            ttx, tty = self.get_matter_location(self.__tooltip, MatterAnchor.RB)

            if ttx > width:
                self.move(self.__tooltip, width - ttx, 0.0)

# private
    def __move_matter_via_info(self, m, info: _MatterInfo, x, y, absolute, ignore_gliding):
        moved = False

        if (not info.gliding) or (m is self.__tooltip) or ignore_gliding:
            moved = self.__do_moving_via_info(m, info, x, y, absolute)
        else:
            if len(info.motion_queues) == 0:
                info.motion_queues.append(_GlidingMotion(x, y, absolute))
            else:
                back = info.motion_queues[-1]

                if back.second == 0.0:
                    back.tx = x
                    back.ty = y
                    back.absolute = absolute
                else:
                    info.motion_queues.append(_GlidingMotion(x, y, absolute))

        return moved

    def __move_matter_to_target_via_info(self, m, info, x, y, fx, fy, dx, dy):
        self.__glide_matter_to_target_via_info(m, info, 0.0, x, y, fx, fy, dx, dy)

    def __glide_matter_via_info(self, m, info: _MatterInfo, sec, x, y, absolute):
        moved = False

        if sec <= 0.0:
            moved = self.__move_matter_via_info(m, info, x, y, absolute, False)
        else:
            sec_delta = 0.0
            if self.info:
                sec_delta = 1.0 / float(self.info.master.frame_rate())
            
            if (sec <= sec_delta) or (sec_delta == 0.0):
                moved = self.__move_matter_via_info(m, info, x, y, absolute, False)
            else:
                if m.motion_stopped():
                    info.motion_queues.clear()
                    moved = self.__do_gliding_via_info(m, info, x, y, sec, sec_delta, absolute)
                elif not info.gliding:
                    moved = self.__do_gliding_via_info(m, info, x, y, sec, sec_delta, absolute)
                else:
                    info.motion_queues.append(_GlidingMotion(x, y, absolute, sec, sec_delta))
        
        return moved

    def __glide_matter_to_target_via_info(self, m, info, sec, x, y, fx, fy, dx, dy):
        ax, ay = 0.0, 0.0

        if m.ready():
            _, _, sw, sh = _unsafe_get_matter_bound(m, info)
            ax = sw * fx
            ay = sh * fy
        else:
            info.iasync = {}
            info.iasync['second'] = sec
            info.iasync['x0'] = x
            info.iasync['y0'] = y
            info.iasync['fx0'] = fx
            info.iasync['fy0'] = fy
            info.iasync['dx0'] = dx
            info.iasync['dy0'] = dy

        return self.__glide_matter_via_info(m, info, sec, x - ax + dx, y - ay + dy, True)

    def __do_moving_via_info(self, m, info, x, y, absolute):
        moved = False

        if not absolute:
            x += info.x
            y += info.y

        if info.x != x or info.y != y:
            ox = info.x
            oy = info.y
            info.x = x
            info.y = y

            m.on_location_changed(info.x, info.y, ox, oy)
            self.size_cache_invalid()
            moved = True

        return moved

    def __do_gliding_via_info(self, m: IMatter, info: _MatterInfo, x, y, sec, sec_delta, absolute):
        moved = False

        if not absolute:
            x += info.x
            y += info.y
        
        if info.x != x or info.y != y:
            n = math.floor(sec / sec_delta)
            dx = x - info.x
            dy = y - info.y
            xspd = dx / n
            yspd = dy / n

            m.set_delta_speed(0.0, 0.0)
            m.set_speed(xspd, yspd)

            info.gliding = True
            info.gliding_tx = x
            info.gliding_ty = y
            info.current_step = 1.0
            info.progress_total = n

            self.on_motion_start(m, sec, info.x, info.y, xspd, yspd)
            info.x, info.y = m.step(info.x, info.y)
            self.on_motion_step(m, info.x, info.y, xspd, yspd, info.current_step / info.progress_total)
            m.on_location_changed(info.x, info.y, x - dx, y - dy)
            self.size_cache_invalid()
            moved = True
        
        return moved

    def __do_motion_moving(self, child: IMatter, info: _MatterInfo, dwidth, dheight):
        if not child.motion_stopped():
            ox, oy = info.x, info.y
            xspd, yspd = child.x_speed(), child.y_speed()
            info.x, info.y = child.step(ox, oy)
            
            if info.gliding:
                if _over_stepped(info.gliding_tx, info.x, xspd) or _over_stepped(info.gliding_ty, info.y, yspd):
                    info.x, info.y = info.gliding_tx, info.gliding_ty
                    self.on_motion_step(child, info.x, info.y, xspd, yspd, 1.0)
                    child.motion_stop()
                    info.gliding = False
                    self.on_motion_complete(child, info.x, info.y, xspd, yspd)
                else:
                    info.current_step += 1.0
                    self.on_motion_step(child, info.x, info.y, xspd, yspd, info.current_step / info.progress_total)

            cwidth, cheight = child.get_extent(info.x, info.y)
            hdist, vdist = 0.0, 0.0
            
            if info.x < 0:
                hdist = info.x
            elif info.x + cwidth > dwidth:
                hdist = info.x + cwidth - dwidth

            if info.y < 0:
                vdist = info.y
            elif info.y + cheight > dheight:
                vdist = info.y + cheight - dheight

            if hdist != 0.0 or vdist != 0.0:
                child.on_border(hdist, vdist)
                
                if child.x_stopped():
                    if info.x < 0.0:
                        info.x = 0.0
                    elif info.x + cwidth > dwidth:
                        info.x = dwidth - cwidth

                if child.y_stopped():
                    if info.y < 0.0:
                        info.y = 0.0
                    elif info.y + cheight > dheight:
                        info.y = dheight - cheight

            if info.gliding and child.motion_stopped():
                info.gliding = False

            if info.x != ox or info.y != oy:
                child.on_location_changed(info.x, info.y, ox, oy)
                self.size_cache_invalid()
                self.notify_updated()
        else:
            while len(info.motion_queues) > 0:
                gm = info.motion_queues.pop(0)

                if gm.second > 0.0:
                    if self.__do_gliding_via_info(child, info, gm.tx, gm.ty, gm.second, gm.sec_delta, gm.absolute):
                        self.notify_updated()
                        break
                elif self.__do_moving_via_info(child, info, gm.tx, gm.ty, gm.absolute):
                    self.notify_updated()

###################################################################################################
def _bind_matter_owership(master, m: IMatter):
    m.info = _MatterInfo(master)
    _unsafe_set_matter_fps(m.info, m.preferred_loacal_fps(), True)
    
    return m.info

def _plane_matter_info(master, m):
    info = None

    if m and m.info and m.info.master == master:
        info = m.info
    
    return info

def _unsafe_get_matter_bound(m: IMatter, info):
    width, height = m.get_extent(info.x, info.y)

    return info.x, info.y, width, height

def _unsafe_add_selected(master, m, info):
    master.before_select(m, True)
    info.selected = True
    master.after_select(m, True)
    master.notify_updated()

def _unsafe_set_selected(master, m, info):
    master.begin_update_sequence()
    master.no_selected()
    _unsafe_add_selected(master, m, info)
    master.end_update_sequence()

def _do_search_selected_matter(start: IMatter, terminator):
    found = None
    child = start

    while child != terminator:
        info = child.info

        if info.selected:
            found = child
            break

        child = info.next

    return found

def _over_stepped(tx, cx, spd):
    return flsign(tx - cx) != flsign(spd)

def _unsafe_set_local_fps(fps, restart, frame_delta, frame_count, elapse):
    frame_delta = 0

    if fps > 0:
        frame_delta = 1000 / fps

    if restart:
        frame_count = 0
        elapse = 0

    return frame_delta, frame_count, elapse

def _unsafe_set_matter_fps(info: _MatterInfo, fps, restart):
    df, fc, e = _unsafe_set_local_fps(fps, restart, info.local_frame_delta, info.local_frame_count, info.local_elapse)
    info.local_frame_delta = df
    info.local_frame_count = fc
    info.local_elapse = e

def _local_timeline_elapse(global_interval, local_frame_delta, local_elapse, duration):
    interval = 0

    if local_frame_delta > 0 or duration > 0:
        if duration > 0:
            e = duration
        else:
            e = local_frame_delta

        if local_elapse < e:
            local_elapse += global_interval
        else:
            interval = local_elapse
            local_elapse = 0
    else:
        interval = global_interval

    return interval, local_elapse
