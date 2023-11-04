#!/usr/bin/env python3

from digitama.big_bang.game import *    # 导入游戏模块，内含 Plane 类和常用函数

# 本游戏中的常量设定
radius: float = 100.0
gliding_duration: float = 2.0

###############################################################################
class ColorMixtureWorld(Plane):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(ColorMixtureWorld, self).__init__("混色模型")

        # 本游戏世界有以下物体
        self.red = None
        self.green = None
        self.blue = None

    def load(self, Width, Height):
        # 思考：为什么背景一定要是黑色的？
        self.set_background(0x000000)

        self.red = self.insert(Circlet(radius, 0xFF0000))   # 红色
        self.green = self.insert(Circlet(radius, 0x00FF00)) # 绿色
        self.blue = self.insert(Circlet(radius, 0x0000FF))  # 蓝色
   
        # 设置混色模式，RGB 属加色模型
        self.red.set_color_mixture(ColorMixture.Add)
        self.green.set_color_mixture(ColorMixture.Add)
        self.blue.set_color_mixture(ColorMixture.Add)

    def reflow(self, width, height):
        self.move_to(self.green, (0.0, height * 0.5), MatterAnchor.LC)
        self.move_to(self.red, (self.green, MatterAnchor.CT), MatterAnchor.CB)
        self.move_to(self.blue, (self.green, MatterAnchor.CB), MatterAnchor.CT)

    def can_select(self, matter):
        return True

    # 实现 ColorMixtureWorld::after_select 方法
    def after_select(self, matter, yes):
        if not yes:
            if isinstance(matter, Circlet):
                self.glide_to_mouse(gliding_duration, matter, MatterAnchor.CC)

    def on_tap_selected(self, matter, x, y):
        self.no_selected()
    
###############################################################################
launch_universe(ColorMixtureWorld, __name__)
