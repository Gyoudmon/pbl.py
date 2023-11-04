#!/usr/bin/env python3

from digitama.big_bang.game import *    # 导入游戏模块，内含 Plane 类和常用函数

###############################################################################
# 本游戏中的常量设定
MAZE_SIZE = 15

pace_duration = 0.5

maze_ground_type = GroundBlockType.Dirt
maze_path_type = GroundBlockType.Soil
maze_wall_type = GroundBlockType.Grass

###############################################################################
class SelfAvoidingWalkWorld(Plane):
    def __init__(self):
        # 通过父类的构造函数设置窗口标题和帧频
        super(SelfAvoidingWalkWorld, self).__init__("自回避游走")

        # 本游戏世界有以下物体
        self.tiles = [None] * MAZE_SIZE
        self.walker: Bracer = None

        # 私有变量
        self.__maze = [None] * MAZE_SIZE
        self.__cell_width = 0.0
        self.__cell_height = 0.0
        self.__row = -1
        self.__col = 0

    def load(self, width, height):
        for row in range(0, MAZE_SIZE):
            # 丑陋的二维数组初始化
            self.tiles[row] = [None] * MAZE_SIZE
            self.__maze[row] = [False] * MAZE_SIZE

            for col in range(0, MAZE_SIZE):
                if _is_inside_maze(row, col):
                    self.tiles[row][col] = self.insert(PlanetCuteTile(maze_ground_type))
                else:
                    self.tiles[row][col] = self.insert(PlanetCuteTile(maze_wall_type))

        self.walker = self.insert(Tita())

        self.__cell_width, self.__cell_height = self.tiles[0][0].get_extent(0.0, 0.0)
        top, _, _, _ = self.tiles[0][0].get_margin(0.0, 0.0)
        bottom = self.tiles[0][0].get_thickness()

        self.__cell_width -= 1.0
        self.__cell_height -= (top + bottom)

    def reflow(self, width, height):
        cx = width * 0.5
        cy = height * 0.5
        maze_x = cx - float(MAZE_SIZE) * self.__cell_width * 0.5
        maze_y = cy - float(MAZE_SIZE) * self.__cell_height * 0.5

        self.move_to(self.walker, (cx, cy), MatterAnchor.CC,
                     0.0, - self.tiles[0][0].get_thickness() - self.__cell_height * 0.5)

        for row in range(0, MAZE_SIZE):
            for col in range(0, MAZE_SIZE):
                dx = maze_x + float(col + 1) * self.__cell_width
                dy = maze_y + float(row + 1) * self.__cell_height

                self.glide_to(pace_duration, self.tiles[row][col], (dx, dy), MatterAnchor.RB)

    def update(self, count, interval, uptime):
        if self.__row >= 0:
            if self.walker.current_mode() == BracerMode.Run:
                if self.walker.motion_stopped():
                    if _is_inside_maze(self.__row, self.__col):
                        if not _is_dead_end(self.__maze, self.__row, self.__col):
                            cur_r = self.__row
                            cur_c = self.__col

                            self.__row, self.__col = _backtracking_pace(self.__maze, self.__row, self.__col)
                            self.__maze[self.__row][self.__col] = True

                            self.glide(pace_duration, self.walker,
                                        (self.__col - cur_c) * self.__cell_width,
                                        (self.__row - cur_r) * self.__cell_height)
                        else:
                            self.walker.switch_mode(BracerMode.Lose)
                    else:
                        self.walker.switch_mode(BracerMode.Win, 1)
                elif self.is_colliding(self.tiles[self.__row][self.__col], (self.walker, MatterAnchor.CC)):
                    if _is_inside_maze(self.__row, self.__col):
                        self.tiles[self.__row][self.__col].set_type(maze_path_type)
            elif not self.walker.in_playing():
                self.__row = -1

    def can_select(self, matter):
        return matter is self.walker
    
# protected
    def on_mission_start(self, width, height):
        self.__reset_maze()
        self.__row = -1

    def after_select(self, m, yes):
        if yes:
            if m == self.walker:
                self.__row = MAZE_SIZE // 2
                self.__col = MAZE_SIZE // 2

                self.walker.switch_mode(BracerMode.Run)
                self.__reset_maze()

                self.move_to(self.walker, (self.tiles[self.__row][self.__col], MatterAnchor.CC),
                             MatterAnchor.CC, 0.0,
                             -self.tiles[self.__row][self.__col].get_thickness())
                
                self.tiles[self.__row][self.__col].set_type(maze_path_type)
                self.__maze[self.__row][self.__col] = True

                self.no_selected()

# private
    def __reset_maze(self):
        for row in range(0, MAZE_SIZE):
            for col in range(0, MAZE_SIZE):
                self.__maze[row][col] = False
                
                if _is_inside_maze(row, col):
                    self.tiles[row][col].set_type(maze_ground_type)
                else:
                    self.tiles[row][col].set_type(maze_wall_type)

###############################################################################
def _is_inside_maze(row, col):
    row_okay = (row >= 1 and row < (MAZE_SIZE - 1))
    col_okay = (col >= 1 and col < (MAZE_SIZE - 1))
    
    return row_okay and col_okay

def _is_dead_end(maze, row, col):
    left_dead  = maze[row + 0][col - 1]
    right_dead = maze[row + 0][col + 1]
    up_dead    = maze[row - 1][col + 0]
    down_dead  = maze[row + 1][col + 0]

    return left_dead and right_dead and up_dead and down_dead

def _backtracking_pace(maze, row, col):
    btr, btc = row, col

    while True:
        r, c = btr, btc
        hint = random.randint(0, 3) % 4

        if hint == 0:
            r -= 1
        elif hint == 1:
            c -= 1
        elif hint == 2:
            r += 1
        elif hint == 3:
            c += 1

        if not maze[r][c]:
            break
    
    return r, c

###############################################################################
launch_universe(SelfAvoidingWalkWorld, __name__)
