### paddleball.py

from digitama.big_bang.game import *    # 导入游戏模块

############################### 定义游戏世界里的物体 ##############################
# 定义一个类型，并命名为 Ball（球）
class Ball(object):
    def __init__(self):
        # 球的位置
        self.x = 0.0
        self.y = 0.0

        # 球的速度
        self.dx = 0.0
        self.dy = 0.0

        # 球的颜色
        self.color = ORANGE

# 定义一个字典，用来搜集 Paddle（桨）的属性
def make_paddle():
    # 桨的位置，以键值对的形式表达
    return { 'x': 0.0, 'y': 0.0, 'speed': 0.0 }

################################ 定义游戏世界的常量 ##############################
ball_radius = 8.0
paddle_width = 128.0
paddle_height = 8.0

ball_speed = 4.0
paddle_speed = ball_speed * 3.0

###############################################################################
class PaddleBallWorld(Universe):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题
        super(PaddleBallWorld, self).__init__()

        # 本游戏世界中的物体
        self.ball = Ball()
        self.paddle = make_paddle()

    def construct(self, argv):
        self.set_window_title("托球游戏(过程式)")

    # 实现 PaddleBallWorld::reflow 方法，调整球和桨的初始位置
    def reflow(self, width, height):
        # 确保球产生与屏幕上方的中间
        self.ball.x = width / 2.0
        self.ball.y = ball_radius

        self.ball.dx = ball_speed * 1.0
        self.ball.dy = ball_speed * 1.0

        # 确保桨产生在靠近屏幕下方的中间
        self.paddle['x'] = self.ball.x - paddle_width / 2.0
        self.paddle['y'] = height - paddle_height * 3.0

    # 实现 PaddleBallWorld::draw 方法，在舞台上绘制出当前位置的球和桨
    def draw(self, renderer, x, y, width, height):
        game_fill_circle(renderer, self.ball.x, self.ball.y, ball_radius, self.ball.color)
        game_fill_rect(renderer, self.paddle['x'], self.paddle['y'], paddle_width, paddle_height, FORESTGREEN)

    # 实现 PaddleBallWorld::update 方法，刷新球和桨的位置，这就是“运动动画”的基本原理
    def update(self, count, interval, uptime):
        width, height = self.get_window_size()

        if self.ball.y < height - ball_radius: # 球未触底
            # 移动球，碰到左右边界、上边界反弹
            self.ball.x = self.ball.x + self.ball.dx
            self.ball.y = self.ball.y + self.ball.dy

            if self.ball.x <= ball_radius or self.ball.x >= width - ball_radius:
                self.ball.dx = -self.ball.dx

            if self.ball.y <= ball_radius:
                self.ball.dy = -self.ball.dy

            # 移动桨，碰到边界停止
            if self.paddle['speed'] != 0.0:
                self.paddle['x'] += self.paddle['speed']

                if self.paddle['x'] < 0.0:
                    self.paddle['x'] = 0.0
                elif self.paddle['x'] + paddle_width > width:
                    self.paddle['x'] = width - paddle_width

            # 检测小球是否被捕获
            ball_bottom = self.ball.y + ball_radius

            if ball_bottom >= self.paddle['y']:
                if self.ball.x >= self.paddle['x'] and self.ball.x <= self.paddle['x'] + paddle_width:
                    self.ball.dy = -self.ball.dy
                else:
                    self.ball.color = RED

            self.notify_updated() # 更新有效，通知系统舞台需要重绘

    # 实现 PaddleBallWorld::on_char 方法，处理键盘事件，用于控制桨的移动
    def _on_char(self, key, modifiers, repeats, pressed):
        if key == pygame.K_a:
            if pressed:
                self.paddle['speed'] = -paddle_speed
            else:
                self.paddle['speed'] = 0.0
        elif key == pygame.K_d:
            if pressed:
                self.paddle['speed'] = +paddle_speed
            else:
                self.paddle['speed'] = 0.0
