#!/usr/bin/env python3

from digitama.big_bang.game import *    # 导入游戏模块，内含 Plane 类和常用函数

###############################################################################
# 本游戏中的常量设定
hue_count = 36
hue_radius = 16.0
wheel_radius = 360.0

primary_radius: float = 100.0

###############################################################################
class ColorWheelWorld(Plane):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(ColorWheelWorld, self).__init__("色相环")

        # 本游戏世界有以下物体
        self.hues = []
        self.primaries = []
        self.tooltip = None

        # 私有变量
        self.__selection_seq = 0

    def load(self, Width, Height):
        # 思考：为什么背景一定要是黑色的？
        self.set_background(0x000000)

        self.primaries.append(self.insert(Ellipselet(primary_radius, primary_radius, 0xFF0000))) # 红色
        self.primaries.append(self.insert(Ellipselet(primary_radius, primary_radius, 0x00FF00))) # 绿色
        self.primaries.append(self.insert(Ellipselet(primary_radius, primary_radius, 0x0000FF))) # 蓝色
   
        # 设置混色模式，RGB 属加色模型
        for c in self.primaries:
            c.set_color_mixture(ColorMixture.Add)

        self.__load_hues()
        self.tooltip = self.insert(make_label_for_tooltip(GameFont.DEFAULT))
        self.set_tooltip_matter(self.tooltip)

    def reflow(self, width, height):
        cx, cy = width * 0.5, height * 0.5
        
        for cc in self.hues:
            x, y = circle_point(wheel_radius, cc.get_color_hue() - 90.0, False)
            self.move_to(cc, (cx + x, cy + y), MatterAnchor.CC)

        self.__reflow_primaries(cx, cy)

    def can_select(self, matter):
        return isinstance(matter, Circlet)

    def after_select(self, matter, yes):
        if yes:
            self.primaries[self.__selection_seq].set_color(matter.get_color())
            self.__selection_seq = (self.__selection_seq + 1) % len(self.primaries)

    def update_tooltip(self, m, local_x, local_y, global_x, global_y):
        updated = False

        if isinstance(m, Circlet):
            self.tooltip.set_text(" #%06X [Hue: %.2f] " % (m.get_color(), m.get_color_hue()))
            self.no_selected()
            updated = True    

        return updated

# private
    def __load_hues(self):
        delta_deg = 360.0 / float(hue_count)
        deg = 0.0

        while deg < 360.0:
            self.hues.append(self.insert(Circlet(hue_radius, deg)))
            deg += delta_deg

    def __reflow_primaries(self, x, y):
        cc_off = primary_radius * 0.5

        self.move_to(self.primaries[0], (x, y), MatterAnchor.CB, 0.0, cc_off)
        self.move_to(self.primaries[1], (self.primaries[0], MatterAnchor.CB), MatterAnchor.RC, cc_off)
        self.move_to(self.primaries[2], (self.primaries[1], MatterAnchor.CC), MatterAnchor.LC)

###############################################################################
launch_universe(ColorWheelWorld, __name__)
