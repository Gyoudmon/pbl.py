#!/usr/bin/env python3

from digitama.big_bang.game import *

###################################################################################################
class Gallery(Plane):
    def __init__(this):
        super(Gallery, this).__init__("The Gallery of Sprites and Graphlets")
        
        this.label = None
        this.caption = None
        this.raft = None
        this.bow = None
        this.stern = None
        this.flag = None
        this.mast = None
        this.post = None
        this.paddle = None
        this.sea = None

    def load(this, width, height):
        this.label = this.insert(Labellet("精灵和图元陈列馆", GameFont.Title, BLACK))
        raft_width, raft_height = this.label.get_extent(0.0, 0.0)

        this.sea = this.insert(Ellipselet(raft_width * 1.618, raft_height, DEEPSKYBLUE))
                
        this.mast = this.insert(Rectanglet(4.0, raft_width, BURLYWOOD, SADDLEBROWN))
        this.flag = this.insert(Trianglet(-raft_height, raft_height * 0.618, -raft_height, -raft_height * 0.618, ROYALBLUE, DODGERBLUE))
        
        this.post = this.insert(RoundedRectanglet(raft_height * 0.618, raft_height * 2.0, -0.45, BURLYWOOD, BURLYWOOD))
        this.paddle = this.insert(Linelet(raft_width * 0.618, raft_height * 1.5, BROWN))
        this.raft = this.insert(RoundedRectanglet(raft_width, raft_height, -0.1, BURLYWOOD, BURLYWOOD))
        this.bow = this.insert(RegularPolygonlet(3, raft_height * 0.5, KHAKI, BURLYWOOD, 180.0))
        this.stern = this.insert(RegularPolygonlet(3, raft_height * 0.5, KHAKI, BURLYWOOD))
                
        this.caption = this.insert(Labellet(this.info.master.display().get_renderer_name(), GameFont.DEFAULT, BLACK))

    def reflow(this, width, height):
        _, raft_height = this.label.get_extent(0.0, 0.0)

        this.move_to(this.sea, (width * 0.5, height * 0.5), MatterAnchor.CT)
                
        this.move_to(this.raft, (this.sea, MatterAnchor.CT), MatterAnchor.CC)
        this.move_to(this.caption, (this.raft, MatterAnchor.CC), MatterAnchor.CC)
        this.move_to(this.bow, (this.raft, MatterAnchor.LC), MatterAnchor.RC)
        this.move_to(this.stern, (this.raft, MatterAnchor.RC), MatterAnchor.LC)
        this.move_to(this.post, (this.raft, MatterAnchor.RB), MatterAnchor.RB, -raft_height)
        this.move_to(this.paddle, (this.post, MatterAnchor.CT), MatterAnchor.LT, -raft_height, raft_height)

        this.move_to(this.mast, (this.raft, MatterAnchor.LB), MatterAnchor.LB, raft_height)
        this.move_to(this.flag, (this.mast, MatterAnchor.RT), MatterAnchor.LT, 0.0, raft_height * 0.5)

    def can_select(this, m): return True


###################################################################################################
launch_universe(Gallery, __name__)
