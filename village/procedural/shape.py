### shape.py

from digitama.big_bang.game import *    # 导入游戏模块，内含 World 类和常用函数

###############################################################################
# 创建自定义数据类型，并命名为 ShapeWorld，继承自 World
class ShapeWorld(Universe):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(ShapeWorld, self).__init__(0)

    # 实现 ShapeWorld::construct 函数，设置窗口大小
    def construct(self, argv):
        self.set_window_title("基本图形陈列馆(过程式)")
        self.set_window_size(800, 600)

    # 实现 ShapeWorld::draw 函数，本例中绘制一系列几何图形
    def draw(self, renderer, x, y, width, height):
        game_draw_blended_text(GameFont.Title, renderer,
            self.get_foreground_color(), 10, 10, "基本图形陈列馆(过程版)")

        ### 绘制椭圆院子 ###
        game_fill_ellipse(renderer, 400, 500, 200, 80, PALEGREEN)                  # 画苍绿色椭圆
        game_draw_ellipse(renderer, 400, 500, 200, 80, KHAKI)                      # 画卡其色轮廓

        ### 绘制(正)三角形屋顶 ###
        game_fill_regular_polygon(renderer, 3, 400, 260, 140, -90, DEEPSKYBLUE)    # 画深空篮正三角形
        game_draw_regular_polygon(renderer, 3, 400, 260, 140, -90, ROYALBLUE)      # 画皇家蓝轮廓

        ### 绘制矩形墙壁 ###
        game_fill_rect(renderer, 300, 330, 200, 180, WHITESMOKE)                   # 画烟雾白矩形
        game_draw_rect(renderer, 300, 330, 200, 180, SNOW)                         # 画雪白色边框

        ### 绘制矩形门 ###
        game_fill_rect(renderer, 324, 426, 42, 84, KHAKI)                          # 画卡其色矩形
        game_draw_rect(renderer, 324, 426, 42, 84, DARKKHAKI)                      # 画深卡其色边框

        ### 绘制门锁 ###
        game_fill_circle(renderer, 358, 468, 4, CHOCOLATE)                         # 画巧克力色圆
        game_draw_circle(renderer, 358, 468, 4, CHOCOLATE)                         # 画巧克力色轮廓

        ### 绘制窗户 ###
        game_fill_rect(renderer, 400, 388, 64, 64, LIGHTSKYBLUE)                   # 画淡天蓝色矩形
        game_draw_rect(renderer, 400, 388, 64, 64, SKYBLUE)                        # 画天蓝色边框
