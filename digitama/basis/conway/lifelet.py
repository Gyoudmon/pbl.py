#!/usr/bin/env python3

from ...big_bang.game import *

import io

###############################################################################
def count_in_neighbor(world, row, col, r, c):
    row_okay = r >= 0 and r < row
    col_okay = c >= 0 and c < col

    if row_okay and col_okay and world[r][c] > 0:
        return 1
    else:
        return 0

def count_neighbors(world, row, col, r, c):
    up = count_in_neighbor(world, row, col, r - 1, c + 0)  # up
    dn = count_in_neighbor(world, row, col, r + 1, c + 0)  # down
    lt = count_in_neighbor(world, row, col, r + 0, c - 1)  # left
    rt = count_in_neighbor(world, row, col, r + 0, c + 1)  # right
    lp = count_in_neighbor(world, row, col, r - 1, c - 1)  # left-up
    rn = count_in_neighbor(world, row, col, r + 1, c + 1)  # right-down
    ln = count_in_neighbor(world, row, col, r + 1, c - 1)  # left-down
    rp = count_in_neighbor(world, row, col, r - 1, c + 1)  # right-up

    return up + dn + lt + rt + lp + rn + ln + rp

###############################################################################
class GameOfLifelet(IGraphlet):
    def __init__(self, size, gridsize = 8.0):
        # 通过父类的构造函数设置窗口标题和帧频
        super(GameOfLifelet, self).__init__()

        if isinstance(size, int):
            self.row, self.col = size, size
        else:
            self.row, self.col = size

        self.color = BLACK
        self.generation = 0
        self.gridsize = gridsize
        self.hide_grid = False
        self.world = None
        self.shadow = None

    def __del__(self):
        # 可以什么都不做
        pass

    def construct(self):
        super(GameOfLifelet, self).construct()
        self.shadow = [0] * (self.row * self.col)
        self.world = [[0 for c in range(self.col)]
                       for r in range(self.row)]

    def get_extent(self, x, y):
        w = math.ceil(self.gridsize * self.col) + 1.0
        h = math.ceil(self.gridsize * self.row) + 1.0

        return w, h

    def draw(self, renderer, x, y, Width, Height):
        game_draw_rect(renderer, x, y, Width - 1, Height - 1, self.color)

        # 绘制网格
        if not self.hide_grid:
            game_draw_grid(renderer, self.row, self.col, self.gridsize, self.gridsize, x, y, self.color)
        
        # 绘制生命状态
        game_fill_grid(renderer, self.world, self.row, self.col, self.gridsize, self.gridsize, x, y, self.color)

###############################################################################
    def reset(self):
        self.generation = 0
        for r in range(self.row):
            for c in range(self.col):
                self.world[r][c] = 0

    def construct_random_world(self):
        self.generation = 0
        for r in range(self.row):
            for c in range(self.col):
                if random.randint(1, 100) % 2 == 0:
                    self.world[r][c] = 1
                else:
                    self.world[r][c] = 0

    def toggle_life_at_location(self, x, y):
        c = int(math.floor(x / self.gridsize))
        r = int(math.floor(y / self.gridsize))

        if self.world[r][c] == 0:
            self.world[r][c] = 1
        else:
            self.world[r][c] = 0

        self.notify_updated()

    def pace_forward(self):
        evolved = False

        # 应用演化规则
        self.evolve(self.world, self.shadow, self.row, self.col)
        
        # 同步舞台状态
        for r in range(self.row):
            for c in range(self.col):
                state = self.shadow[r * self.col + c]

                if self.world[r][c] != state:
                    self.world[r][c] = state
                    evolved = True
        
        if evolved:
            self.generation += 1

        return evolved

    def evolve(self, world, shadow, row, col):
        raise Exception("Abstract Method, Please implement it in subclasses")

###############################################################################
    def load(self, life_world, golin):
        self.reset()

        r = 0
        for rowline in golin:
            if r < self.row:
                c = 0
                for col in rowline:
                    # WARNING: the `rowline` contains the trailing `newline`
                    if c < self.col:
                        if col == '1':
                            self.world[r][c] = 1
                        else:
                            self.world[r][c] = 0
                        c += 1
                    else:
                        break
                r += 1
            else:
                break

    def save(self, life_world, golout: io.TextIOWrapper):
        if self.world:
            for r in range(self.row):
                for c in range(self.col):
                    print(self.world[r][c], end="", file=golout)
                
                print('\n', end="", file=golout)

###############################################################################
    def show_grid(self, yes):
        if self.hide_grid == yes:
            self.hide_grid = not yes
            self.notify_updated()

    def set_color(self, hex):
        if self.color != hex:
            self.color = hex
            self.notify_updated()

###############################################################################
class ConwayLifelet(GameOfLifelet):
    def __init__(self, size, gridsize = 8):
        super().__init__(size, gridsize)

    def evolve(self, world, shadow, row, col):
        for r in range(row):
            for c in range(col):
                n = count_neighbors(world, row, col, r, c)
                i = r * col + c

                if n < 2:    # 独孤死(离群索居)
                    shadow[i] = 0
                elif n > 3:  # 内卷死(过渡竞争)
                    shadow[i] = 0
                elif n == 3: # 无性繁殖
                    shadow[i] = 1
                else:
                    shadow[i] = world[r][c]

class HighLifelet(GameOfLifelet):
    def __init__(self, size, gridsize = 8):
        super().__init__(size, gridsize)

    def evolve(self, world, shadow, row, col):
        for r in range(row):
            for c in range(col):
                n = count_neighbors(world, row, col, r, c)
                i = r * col + c

                if n == 2:
                    shadow[i] = world[r][c]
                elif n == 3 or n == 6:
                    shadow[i] = 1
                else:
                    shadow[i] = 0
