from ..mathematics import *

###############################################################################
class IPlatformMotion(object):
    def __init__(self, facing_right = True, walk_only = False):
        super(IPlatformMotion, self).__init__(self)

        if facing_right:
            self.__default_facing_sgn = +1.0
        else:
            self.__default_facing_sgn = -1.0
        
        self.__walk_only = walk_only

# protected
    def _dispatch_heading_event(self, theta_rad, vx, vy, prev_vr):
        hsgn, _ = self._get_flip_signs()

        if flsign(vx) * hsgn * self.__default_facing_sgn == -1.0:
            self._horizontal_flip()

        if self.__walk_only:
            if vx != 0.0:
                self._on_walk(theta_rad, vx, vy)
        else:
            if vy == 0.0:
                self._on_walk(theta_rad, vx, vy)
            elif vy < 0.0:
                self._on_jump(theta_rad, vx, vy)

    def _on_walk(self, theta_rad, vx, vy):
        pass

    def _on_jump(self, theta_rad, vx, vy):
        pass

# protected, abstract
    def _get_flip_signs(self): pass
    def _horizontal_flip(self): pass
