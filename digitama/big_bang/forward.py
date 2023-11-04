import enum

###############################################################################
class MatterAnchor(enum.Enum):
    LT = 0x4983917e165afce8
    CT = 0x45469ade8ed1ff0e
    RT = 0x43fa3ada0199d0ed
    LC = 0x45be256177a1bacb
    CC = 0x4d3b7e0e5d4bf118
    RC = 0x4a89be34d21896a6
    LB = 0x49071ea39c89fc24
    CB = 0x40774aafb4b0d0ae
    RB = 0x4208392ecc81b775

class BorderEdge(enum.Enum):
    TOP = 0x4d52cf9d2eeb506f
    RIGHT = 0x488d2013b5d8f2ad
    BOTTOM = 0x463b469498d6f36a
    LEFT = 0x45c62f50ae7e873d
    NONE = 0x4151ac35cfedfb3d

class BorderStrategy(enum.Enum):
    IGNORE = 0x402f7a5172c81a41
    STOP = 0x407c35437235f05f
    BOUNCE = 0x4fcc175c111c2d94

###############################################################################
def matter_anchor_fraction(a):
    fx, fy = 0.0, 0.0

    if isinstance(a, enum.Enum): 
        if a == MatterAnchor.LT: pass
        elif a == MatterAnchor.LC: fy = 0.5
        elif a == MatterAnchor.LB: fy = 1.0
        elif a == MatterAnchor.CT: fx = 0.5          
        elif a == MatterAnchor.CC: fx, fy = 0.5, 0.5
        elif a == MatterAnchor.CB: fx, fy = 0.5, 1.0
        elif a == MatterAnchor.RT: fx = 1.0
        elif a == MatterAnchor.RC: fx, fy = 1.0, 0.5
        elif a == MatterAnchor.RB: fx, fy = 1.0, 1.0
    else:
        fx, fy = a[0], a[1]

    return fx, fy
