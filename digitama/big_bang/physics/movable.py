from ..forward import *

from .mathematics import *

###############################################################################
class IMovable(object):
    def __init__(self):
        super(IMovable, self).__init__()
        
        self.__border_strategies = {}
        self.__bounce_acc = False
        self.__ar, self.__ax, self.__ay = math.nan, 0.0, 0.0
        self.__vr, self.__vx, self.__vy = math.nan, 0.0, 0.0
        self.__tvx, self.__tvy = math.inf, math.inf

        self.set_border_strategy([BorderStrategy.IGNORE])
        self.motion_stop(True, True)

# public
    def set_border_strategy(self, s):
        if isinstance(s, BorderEdge):
            self.set_border_strategy([s, s, s, s])
        else:
            size = len(s)

            if size == 1:
                self.set_border_strategy([s[0], s[0], s[0], s[0]])
            elif size == 2:
                self.set_border_strategy([s[0], s[1], s[0], s[1]])
            elif size == 4:
                self.__border_strategies[BorderEdge.TOP] = s[0]
                self.__border_strategies[BorderEdge.RIGHT] = s[1]
                self.__border_strategies[BorderEdge.BOTTOM] = s[2]
                self.__border_strategies[BorderEdge.LEFT] = s[3]
            else:
                pass

    def on_border(self, hoffset, voffset):
        hstrategy = BorderStrategy.IGNORE
        vstrategy = BorderStrategy.IGNORE

        if hoffset < 0.0:
            hstrategy = self.__border_strategies[BorderEdge.LEFT]
        elif hoffset > 0.0:
            hstrategy = self.__border_strategies[BorderEdge.RIGHT]

        if voffset < 0.0:
            vstrategy = self.__border_strategies[BorderEdge.TOP]
        elif voffset > 0.0:
            vstrategy = self.__border_strategies[BorderEdge.BOTTOM]

        if hstrategy == BorderStrategy.STOP or vstrategy == BorderStrategy.STOP:
            self.motion_stop(True, True) # if stopping, both direction should stop
        elif hstrategy == BorderStrategy.BOUNCE or vstrategy == BorderStrategy.BOUNCE:
            self.motion_bounce(hstrategy == BorderStrategy.BOUNCE, vstrategy == BorderStrategy.BOUNCE)

# public
    def set_acceleration(self, acc, direction, is_radian = False):
        ax, ay = orthogonal_decomposition(acc, direction, is_radian)
        self.set_delta_speed(ax, ay)

    def add_acceleration(self, acc, direction, is_radian = False):
        ax, ay = orthogonal_decomposition(acc, direction, is_radian)
        self.add_delta_speed(ax, ay)

    def get_acceleration(self):
        return vector_magnitude(self.__ax, self.__ay)

    def get_acceleration_direction(self, need_radian = True):
        rad = self.__ar

        if math.isnan(rad):
            rad = math.atan2(self.__ay, self.__ax)

        if not need_radian:
            rad = radians_to_degrees(rad)

        return rad

    def set_delta_speed(self, xacc, yacc):
        xchanged = (self.__ax != xacc)
        ychanged = (self.__ay != yacc)

        if xchanged: self.__ax = xacc
        if ychanged: self.__ay = yacc

        if xchanged or ychanged:
            self.__on_acceleration_changed()

    def add_delta_speed(self, xacc, yacc):
        self.set_delta_speed(self.__ax + xacc, self.__ay + yacc)

    def x_delta_speed(self):
        return self.__ax
    
    def y_delta_speed(self):
        return self.__ay

# public
    def set_velocity(self, spd, direction, is_radian = False):
        vx, vy = orthogonal_decomposition(spd, direction, is_radian)
        self.set_speed(vx, vy)

    def add_velocity(self, spd, direction, is_radian = False):
        vx, vy = orthogonal_decomposition(spd, direction, is_radian)
        self.add_speed(vx, vy)

    def get_velocity(self):
        return vector_magnitude(self._vx, self.__vy)
    
    def get_velocity_direction(self, need_radian = True):
        rad = self.__vr

        if math.isnan(rad):
            rad = math.atan2(self.__vy, self.__vx)

        if not need_radian:
            rad = radians_to_degrees(rad)

        return rad
        
    def set_speed(self, xspd, yspd):
        xspd = vector_clamp(xspd, self.__tvx)
        yspd = vector_clamp(yspd, self.__tvy)

        xchanged = self.__vx != xspd
        ychanged = self.__vy != yspd

        if xchanged: self.__vx = xspd
        if ychanged: self.__vy = yspd

        if xchanged or ychanged:
            self.__on_velocity_changed()

    def add_speed(self, xspd, yspd):
        self.set_speed(self.__vx + xspd, self.__vy + yspd)

    def x_speed(self):
        return self.__vx
    
    def y_speed(self):
        return self.__vy

# public
    def set_terminal_velocity(self, max_v, direction, is_radian = False):
        xv, vy = orthogonal_decomposition(max_v, direction, is_radian)
        self.set_terminal_speed(xv, vy)

    def set_terminal_speed(self, mxspd, myspd):
        changed = False

        self.__tvx = math.abs(mxspd)
        self.__tvy = math.abs(myspd)

        if flout(-self.__tvx, self.__vx, self.__tvx):
            self.__vx = vector_clamp(self.__vx, self.__tvx)
            changed = True

        if flout(-self.__tvy, self.__vy, self.__tvy):
            self.__vy = vector_clamp(self.__vy, self.__tvy)
            changed = True

        if changed:
            self.__on_velocity_changed()
    
    def set_heading(self, direction, is_radian = False):
        if not is_radian:
            direction = degrees_to_radians(direction)

        self.__check_heading_changing(direction)

    def get_heading(self, need_radian = True):
        return self.get_velocity_direction()
    
    def heading_rotate(self, theta, is_radian = False):
        if theta != 0.0:
            vector_rotate(self.__vx, self.__vy, theta, 0.0, 0.0, is_radian)
            self.__on_velocity_changed()

# public
    def step(self, sx, sy):
        if self.__ax != 0.0:
            self.__vx = vector_clamp(self.__vx + self.__ax, self.__tvx)
        
        if self.__ay != 0.0:
            self.__vy = vector_clamp(self.__vy + self.__ay, self.__tvy)

        self.__check_velocity_changing()

        if self.__vx != 0.0: sx += self.__vx
        if self.__vy != 0.0: sy += self.__vy

        return sx, sy

    def motion_bounce(self, horizon, vertical):
        if horizon:
            self.__vx *= -1.0
            if self.__bounce_acc:
                self.__ax *= -1.0

        if vertical:
            self.__vy *= -1.0
            if self.__bounce_acc:
                self.__ay *= -1.0

        if horizon or vertical:
            self.__on_velocity_changed()
            if self.__bounce_acc:
                self.__on_acceleration_changed()

    def motion_stop(self, horizon = True, vertical = True):
        if horizon:
            self.__vx = 0.0
            self.__ax = 0.0

        if vertical:
            self.__vy = 0.0
            self.__ay = 0.0

        if horizon and vertical:
            self.__ar = math.nan
            # self.__vr = math.nan
            self._on_motion_stopped()
        else:
            self.__on_acceleration_changed()
            self.__on_velocity_changed()

    def disable_acceleration_bounce(self, yes = True):
        self.__bounce_acc = (not yes)
    
# public
    def x_stopped(self):
        return self.__ax == 0.0 and self.__vx == 0.0

    def y_stopped(self):
        return self.__ay == 0.0 and self.__vy == 0.0
    
    def motion_stopped(self):
        return self.x_stopped() and self.y_stopped()

# protected
    def _on_heading_changed(self, theta_rad, vx, vy, prev_vr): pass
    def _on_motion_stopped(self): pass

# private
    def __on_acceleration_changed(self):
        self.__ar = math.atan2(self.__ay, self.__ax)

    def __on_velocity_changed(self):
        rad = math.atan2(self.__vy, self.__vx)

        self.__check_heading_changing(rad)

    def __check_heading_changing(self, rad):
        if self.__vr != rad:
            pvr = self.__vr

            self.__vr = rad
            self._on_heading_changed(rad, self.__vx, self.__vy, pvr)

    def __check_velocity_changing(self):
        if self.__ax != 0.0 or self.__ay != 0.0:
            if self.__ar != self.__vr:
                self.__on_velocity_changed()
