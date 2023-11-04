#!/usr/bin/env python3

### shape.py
from digitama.big_bang.game import *    # 导入游戏模块，内含 Plane 类和常用函数

###############################################################################
# 创建自定义数据类型，并命名为 ShapeWorld，继承自 Plane
class ShapeWorld(Plane):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(ShapeWorld, self).__init__("基本图形陈列馆(对象版)")

        # 本游戏世界有以下物体
        self.label = None
        self.roof = None
        self.wall = None
        self.door = None
        self.lock = None
        self.window = None

    # 实现 ShapeWorld::load 方法，在舞台上加入基础几何图形的实例，注意添加顺序
    def load(self, Width, Height):
        self.label = self.insert(Labellet("基本图形陈列馆(对象版)", GameFont.Title, BLACK))

        # 苍绿色院子
        self.garden = self.insert(Ellipselet(200.0, 80.0, PALEGREEN, KHAKI))
    
        # 房屋的组成
        self.roof = self.insert(RegularPolygonlet(3, 140.0, DEEPSKYBLUE, ROYALBLUE, -90.0)) # 深空蓝屋顶
        self.wall = self.insert(Rectanglet(200.0, 180.0, WHITESMOKE, SNOW));                # 白色墙壁
        self.door = self.insert(Rectanglet(42.0, 84.0, KHAKI, DARKKHAKI));                  # 卡其色门
        self.lock = self.insert(Circlet(4.0, CHOCOLATE));                                   # 巧克力色门锁
        self.window = self.insert(RoundedSquarelet(64.0, -0.15, LIGHTSKYBLUE, SKYBLUE));    # 淡天蓝色窗口

    # 实现 ShapeWorld::reflow 方法，重新排列几何图形在舞台上的位置
    def reflow(self, width, height):
        # 排列基本图形以组装房屋
        self.move_to(self.roof, (width * 0.5, height * 0.5), MatterAnchor.CB)
        self.move_to(self.wall, (self.roof, MatterAnchor.CB), MatterAnchor.CT)
        self.move_to(self.door, (self.wall, MatterAnchor.LB), MatterAnchor.LB, 24.0)
        self.move_to(self.lock, (self.door, MatterAnchor.RC), MatterAnchor.RC, -4.0)
        self.move_to(self.window, (self.wall, MatterAnchor.CC), MatterAnchor.LC)

        # 排列院子
        self.move_to(self.garden, (self.wall, MatterAnchor.CC), MatterAnchor.CT)

    # 为演示该设计思路的优点，运行游戏里的物体可以被选中
    def can_select(self, matter):
        return True
    
###############################################################################
launch_universe(ShapeWorld, __name__)
