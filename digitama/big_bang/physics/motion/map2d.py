from ..mathematics import *

###############################################################################
class I4WayMotion(object):
    def __init__(self):
        super(I4WayMotion, self).__init__()

# protected
    def _dispatch_heading_event(self, theta_rad, vx, vy, prev_vr):
        theta = abs(theta_rad)

        if theta < q_pi:
            self._on_eward(theta_rad, vx, vy)
        elif theta > q_pi * 3.0:
            self._on_wward(theta_rad, vx, vy)
        elif theta_rad >= 0.0:
            self._on_sward(theta_rad, vx, vy)
        else:
            self._on_nward(theta_rad, vx, vy)

# protected, abstract
    def _on_nward(self, theta_rad, vx, vy): pass
    def _on_eward(self, theta_rad, vx, vy): pass
    def _on_sward(self, theta_rad, vx, vy): pass
    def _on_wward(self, theta_rad, vx, vy): pass

###############################################################################
class I8WayMotion(I4WayMotion):
    def __init__(self):
        super(I8WayMotion).__init__()

# protected
    def _dispatch_heading_event(self, theta_rad, vx, vy, prev_vr):
        theta = theta_rad

        if theta < 0.0:
            theta = pi * 2.0 + theta

        if theta <= _theta_thresholds[0]:
            self._on_eward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[1]:
            self._on_esward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[2]:
            self._on_sward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[3]:
            self._on_wsward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[4]:
            self._on_wward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[5]:
            self._on_wnward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[6]:
            self._on_nward(theta_rad, vx, vy)
        elif theta <= _theta_thresholds[7]:
            self._on_enward(theta_rad, vx, vy)
        else:
            self._on_eward(theta_rad, vx, vy)

# protected, abstract
    def _on_enward(self, theta_rad, vx, vy): pass
    def _on_wnward(self, theta_rad, vx, vy): pass
    def _on_esward(self, theta_rad, vx, vy): pass
    def _on_wsward(self, theta_rad, vx, vy): pass

###############################################################################
_pi_125 = q_pi * 0.5
_theta_thresholds = [
    _pi_125,
    _pi_125 + q_pi, _pi_125 + h_pi, _pi_125 + q_pi * 3.0, _pi_125 + pi,
    _pi_125 + q_pi * 5.0, _pi_125 + q_pi * 6.0, _pi_125 + q_pi * 7.0
]
