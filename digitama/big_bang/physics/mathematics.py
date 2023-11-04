import math

###################################################################################################
pi = math.pi
d_pi = math.pi * 2.0
h_pi = math.pi * 0.5
q_pi = math.pi * 0.25
	
###################################################################################################
def radians_to_degrees(radians):
    return math.degrees(radians)

def degrees_to_radians(degrees):
    return math.radians(degrees)

def degrees_normalize(degrees, degrees_start = 0.0):
    degrees_end = degrees_start + 360.0
    
    while degrees < degrees_start:
        degrees += 360.0
    
    while degrees >= degrees_end:
        degrees -= 360.0

    return degrees
        
def radians_normalize(radians, degrees_start = 0.0):
    radians_start = degrees_to_radians(degrees_start)
    radians_end = radians_start + d_pi
    
    while radians < radians_start:
        radians += d_pi

    while radians >= radians_end:
        radians -= d_pi

    return radians

###################################################################################################
def flin(dmin, datum, dmax):
    return dmin <= datum and datum <= dmax

def flout(dmin, datum, dmax):
    return datum < dmin or datum > dmax

def flsign(x):
    return math.copysign(1, x)

###################################################################################################
def point_inside(px, py, x1, y1, x2, y2):
    if x1 <= x2:
        x_okay = flin(x1, px, x2)
    else:
        x_okay = flin(x2, px, x1)

    if y1 <= y2:
        y_okay = flin(y1, px, y2)
    else:
        y_okay = flin(y2, px, y1)

    return x_okay and y_okay

def rectangle_inside(tlx1, tly1, brx1, bry1, tlx2, tly2, brx2, bry2):
    x_in = flin(tlx2, tlx1, brx2) and flin(tlx2, brx1, brx2)
    y_in = flin(tly2, tly1, bry2) and flin(tly2, bry1, bry2)

    return x_in and y_in

def rectangle_overlay(tlx1, tly1, brx1, bry1, tlx2, tly2, brx2, bry2):
    x_off = brx1 < tlx2 or tlx1 > brx2
    y_off = bry1 < tly2 or tly1 > bry2

    return not (x_off or y_off)

def rectangle_contain(tlx, tly, brx, bry, x, y):
    return flin(tlx, x, brx) and flin(tly, y, bry)

###################################################################################################
def orthogonal_decomposition(magnitude, direction, is_radian):
    if is_radian:
        rad = direction
    else:
        rad = degrees_to_radians(direction)

    return magnitude * math.cos(rad), magnitude * math.sin(rad)

def vector_magnitude(x, y):
    return math.sqrt(x * x + y * y)

def vector_direction(x, y, need_radian):
    rad = math.atan2(y, x)

    if not need_radian:
        rad = radians_to_degrees(rad)

    return rad

def vector_rotate(x, y, theta, ox, oy, is_radian = True):
    if is_radian:
        rad = theta
    else:
        rad = degrees_to_radians(theta)
	
    cosr = math.cos(rad)
    sinr = math.sin(rad)
    dx = x - ox
    dy = y - oy

    rx = dx * cosr - dy * sinr + ox
    ry = dx * sinr + dy * cosr + oy

    return rx, ry

def vector_clamp(v, ceil):
    if v > ceil:
        v = ceil
    elif v < -ceil:
        v = -ceil

    return v

###################################################################################################
def circle_point(radius, angle, is_radian = False):
    if not is_radian:
        angle = degrees_to_radians(angle)

    return radius * math.cos(angle), radius * math.sin(angle)

def ellipse_point(radiusX, radiusY, angle, is_radian = False):
    if not is_radian:
        angle = degrees_to_radians(angle)

    return radiusX * math.cos(angle), radiusY * math.sin(angle)

###################################################################################################
def lines_intersection(x11, y11, x12, y12, x21, y21, x22, y22):
    '''
     find the intersection point P(px, py) of L1((x11, y11), (x12, y12)) and L2((x21, y21), (x22, y22))
    '''

    denominator = ((x11 - x12) * (y21 - y22) - (y11 - y12) * (x21 - x22))
    intersected = (denominator != 0.0)
    
    if intersected:
        T1 = +((x11 - x21) * (y21 - y22) - (y11 - y21) * (x21 - x22)) / denominator
        T2 = -((x11 - x12) * (y11 - y21) - (y11 - y12) * (x11 - x21)) / denominator
        px = x21 + T2 * (x22 - x21)
        py = y21 + T2 * (y22 - y21)
    else:
        px = py = T1 = T2 = math.nan

    return px, py, T1, T2
