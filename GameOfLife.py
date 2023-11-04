#!/usr/bin/env python3

from digitama.big_bang.game import *        # 导入游戏模块，内含 Plane 类和常用函数
from digitama.basis.conway.lifelet import * # 导入游戏图元

import os
import enum

###############################################################################
default_frame_rate = 8
generation_fmt = "Generation: %d"

AUTO_KEY = 'a'
STOP_KEY = 's'
PACE_KEY = 'p'
EDIT_KEY = 'e'
LOAD_KEY = 'l'
RAND_KEY = 'r'
RSET_KEY = 'z'
WRTE_KEY = 'w'

ordered_keys = (AUTO_KEY, STOP_KEY, PACE_KEY, EDIT_KEY, LOAD_KEY, WRTE_KEY, RAND_KEY, RSET_KEY)
colors_for_auto = (GRAY, GREEN, GRAY, GRAY, GRAY, GRAY, GRAY, GRAY)
colors_for_stop = (GREEN, GRAY, GREEN, GREEN, GRAY, GRAY, GRAY, GRAY)
colors_for_edit = (GREEN, GRAY, GREEN, GRAY, GREEN, GREEN, GREEN, GREEN)

###############################################################################
class GameState(enum.Enum):
    Auto = 0,
    Stop = 1,
    Edit = 2,
    _ = 3

###############################################################################
class GameOfLifeWorld(Plane):
    def __init__(self, life_demo = "", gridsize = 8.0):
        # 通过父类的构造函数设置窗口标题和帧频
        super(GameOfLifeWorld, self).__init__("生命游戏")

        # 本游戏世界有以下物体
        self.gameboard : GameOfLifelet = None
        self.generation : Labellet = None
        self.instructions  = {}

        # 私有变量
        self.__state: GameState = GameState._
        self.__gridsize = gridsize
        self.__demo_path = life_demo

    def load(self, width, height):
        self.__load_gameboard(width, height)
        self.__load_instructions(width, height)
        
        self.set_local_fps(default_frame_rate)
        self.__load_conway_demo()

    def reflow(self, width, height):
        self.move_to(self.gameboard, (width * 0.5, height * 0.5), MatterAnchor.CC)
        self.move_to(self.generation, (self.gameboard, MatterAnchor.RT), MatterAnchor.RB)

        self.move_to(self.instructions[ordered_keys[0]], (0.0, height), MatterAnchor.LB)
        for idx in range(1, len(ordered_keys)):
            self.move_to(self.instructions[ordered_keys[idx]],
                    (self.instructions[ordered_keys[idx - 1]], MatterAnchor.RB),
                    MatterAnchor.LB, 16.0)

    def update(self, count, interval, uptime):
        if self.__state == GameState.Auto:
            self.__pace_forward()
    
# protected
    def on_mission_start(self, width, height):
        self.__switch_game_state(GameState.Stop)

    def can_select(self, matter):
        return self.__state == GameState.Edit and isinstance(matter, GameOfLifelet)
    
    def on_tap(self, matter, x, y):
        if isinstance(matter, GameOfLifelet):
            self.gameboard.toggle_life_at_location(x, y)
            self.instructions[WRTE_KEY].set_text_color(GREEN)

    def on_char(self, keycode, modifiers, repeats, pressed):
        if not pressed:
            try:
                key = chr(keycode)
            except ValueError:
                key = keycode
                
            if key in self.instructions:
                if self.instructions[key].get_text_color() == GREEN:
                    if key == AUTO_KEY: self.__switch_game_state(GameState.Auto)
                    elif key == STOP_KEY: self.__switch_game_state(GameState.Stop)
                    elif key == EDIT_KEY: self.__switch_game_state(GameState.Edit)
                    elif key == RAND_KEY: self.gameboard.construct_random_world()
                    elif key == RSET_KEY: self.gameboard.reset()
                    elif key == PACE_KEY: self.__pace_forward()
                    elif key == LOAD_KEY: self.__load_conway_demo()
                    elif key == WRTE_KEY: self.__save_conway_demo()

                    self.notify_updated()
                else:
                    self.instructions[key].set_text_color(CRIMSON)

# private
    def __load_gameboard(self, width, height):
        border_height = height - generic_font_size(FontSize.xx_large) * 2.0
        border_width = border_height
        col = round(border_width / self.__gridsize) - 1
        row = round(border_height / self.__gridsize) - 1

        self.gameboard = self.insert(HighLifelet((row, col), self.__gridsize))
        self.generation = self.insert(Labellet(generation_fmt % (self.gameboard.generation), GameFont.math, GREEN))

    def __load_instructions(self, width, height):
        self.instructions[AUTO_KEY] = self.insert(Labellet("%c. 自行演化" % AUTO_KEY, GameFont.monospace))
        self.instructions[STOP_KEY] = self.insert(Labellet("%c. 停止演化" % STOP_KEY, GameFont.monospace))
        self.instructions[EDIT_KEY] = self.insert(Labellet("%c. 手动编辑" % EDIT_KEY, GameFont.monospace))
        self.instructions[RAND_KEY] = self.insert(Labellet("%c. 随机重建" % RAND_KEY, GameFont.monospace))
        self.instructions[RSET_KEY] = self.insert(Labellet("%c. 世界归零" % RSET_KEY, GameFont.monospace))
        self.instructions[PACE_KEY] = self.insert(Labellet("%c. 单步跟踪" % PACE_KEY, GameFont.monospace))
        self.instructions[LOAD_KEY] = self.insert(Labellet("%c. 载入范例" % LOAD_KEY, GameFont.monospace))
        self.instructions[WRTE_KEY] = self.insert(Labellet("%c. 保存范例" % WRTE_KEY, GameFont.monospace))

    def __switch_game_state(self, new_state):
        if self.__state != new_state:
            if new_state == GameState.Auto:
                self.gameboard.set_color(LIGHTBLUE)
                self.gameboard.show_grid(False)
                self.__update_instructions_state(colors_for_auto)
            elif new_state == GameState.Stop:
                self.gameboard.set_color(DIMGRAY)
                self.__update_instructions_state(colors_for_stop)
            elif new_state == GameState.Edit:
                self.gameboard.set_color(ROYALBLUE)
                self.gameboard.show_grid(True)
                self.__update_instructions_state(colors_for_edit)
        
            self.__state = new_state
            self.notify_updated()

    def __update_instructions_state(self, colors):
        for idx in range(len(ordered_keys)):
            self.instructions[ordered_keys[idx]].set_text_color(colors[idx])

    def __pace_forward(self):
        if self.gameboard.pace_forward():
            self.generation.set_text_color(GREEN)
            self.generation.set_text(generation_fmt % (self.gameboard.generation), MatterAnchor.RB)
        else:
            self.generation.set_text_color(ORANGE)
            self.generation.set_text(generation_fmt % (self.gameboard.generation), MatterAnchor.RB)
        
            if self.__state == GameState.Auto:
                self.__switch_game_state(GameState.Stop)

# private
    def __default_conway_demo(self):
        return digimon_path("demo/conway/typical", ".gof")

    def __save_conway_demo(self):
        if not os.path.exists(self.__demo_path):
            self.__demo_path = self.__default_conway_demo()
    
        try:
            os.makedirs(os.path.dirname(self.__demo_path), exist_ok=True)

            golout = open(self.__demo_path, 'w')
            self.gameboard.save(self.__demo_path, golout)
            golout.close()
            self.instructions[WRTE_KEY].set_text_color(ROYALBLUE)
        except IOError as reason:
            self.instructions[WRTE_KEY].set_text_color(FIREBRICK)
            print("Failed to save the demo: %s" % reason)

    def __load_conway_demo(self):
        if not os.path.exists(self.__demo_path):
            self.__demo_path = self.__default_conway_demo()
    
        try:
            golin = open(self.__demo_path, 'r')
            self.gameboard.load(self.__demo_path, golin)
            golin.close()
        except IOError as reason:
            self.instructions[LOAD_KEY].set_text_color(FIREBRICK)
            print("Failed to load the demo: %s" % reason)

###############################################################################
launch_universe(GameOfLifeWorld, __name__)
