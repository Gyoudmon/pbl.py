#!/usr/bin/env python3

from digitama.big_bang.game import *    # 导入游戏模块，内含 Plane 类和常用函数

###############################################################################
# 本游戏中的常量设定
step_size = 2.0
step_duration = 0.2

###############################################################################
class DrunkardWalkWorld(Plane):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(DrunkardWalkWorld, self).__init__("醉汉漫步")

        # 本游戏世界有以下物体
        self.drunkard = None
        self.partner = None
        self.beach = None
        self.tent = None

    def load(self, Width, Height):
        self.beach = self.insert(Sprite(digimon_path("assets/beach", ".png")))
        self.tent = self.insert(SpriteGridSheet(digimon_path("assets/tents", '.png'), 1, 4))
        self.drunkard = self.insert(Agate())
        self.partner = self.insert(Tita())

    def reflow(self, width, height):
        self.move_to(self.beach, (width * 0.5, height), MatterAnchor.CB)
        self.move_to(self.tent, (0.0, height), MatterAnchor.LB)

    def update(self, count, interval, uptime):
        if not self.is_colliding(self.drunkard, self.partner):
            if self.partner.motion_stopped():
                self.__random_walk(self.partner)

            self.__drunkard_walk(self.drunkard)
        elif self.partner.current_mode() != BracerMode.Win:
            self.partner.motion_stop()
            self.drunkard.switch_mode(BracerMode.Win, 1)
            self.partner.switch_mode(BracerMode.Win, 1)

    def can_select(self, matter):
        return True
    
# protected
    def on_mission_start(self, width, height):
        self.drunkard.switch_mode(BracerMode.Walk)
        self.drunkard.set_heading(-180.0)

        self.move_to(self.drunkard, (width * 0.95, height * 0.9), MatterAnchor.CC)
        self.move_to(self.partner, (width * 0.24, height * 0.9), MatterAnchor.LC)

# private
    def __random_walk(self, who):
        # random.randint(-1, 1) 产生一个位于区间 [-1, 1] 的随机整数
        dx = random.randint(-1, 1) # 左右移动或不动
        dy = random.randint(-1, 1) # 上下移动或不动

        self.glide(step_duration, who, dx * step_size, dy * step_size)

    def __drunkard_walk(self, who):
        # 产生一个位于区间 [0, 100] 的随机整数
        chance = random.randint(0, 100)
        dx = 0.0
        dy = 0.0
        
        if chance < 10:
            pass # no move    
        elif chance < 58:
            dx = -1.0
        elif chance < 60:
            dx = +1.0
        elif chance < 80:
            dy = +1.0
        else:
            dy = -1.0

        self.move(who, dx, dy)

###############################################################################
launch_universe(DrunkardWalkWorld, __name__)
