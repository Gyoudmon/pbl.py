import pygame           # PyGame 函数

import sys              # 系统相关参数和函数
import atexit           # 用于管理程序退出时执行的函数
import datetime         # 日期时间函数

from .graphics.font import *
from .graphics.text import *
from .graphics.colorspace import *

from .virtualization.display import *

###############################################################################
def game_initialize():
    if GameFont.DEFAULT is None:
        pygame.init()
        atexit.register(pygame.quit)

        GameFonts_initialize()

        #atexit.register(GameFonts_destroy)

def game_world_create(width, height):
    flags = pygame.SHOWN

    if width <= 0 and height <= 0:
        flags |= pygame.FULLSCREEN
    elif width <= 0 or height <= 0:
        flags |= pygame.RESIZABLE
        width, height = pygame.display.get_desktop_sizes()[0]
    else:
        flags |= pygame.RESIZABLE
    
    return pygame.display.set_mode((width, height), flags)

def game_world_reset(renderer, fgc, bgc, flipping):
    renderer.fill(RGB_FromHexadecimal(bgc))
    
    if flipping:
        pygame.display.flip()

def game_world_refresh(renderer):
    pygame.display.flip()

###############################################################################
class Universe(IDisplay):
# public
    def __init__(self, fps = 60, fgc = 0x0000000, bgc = 0xFFFFFF):
        """ 构造函数，在创建游戏世界时自动调用，以设置帧频、窗口标题、前背景色和混色模式 """
        
        # The constructors of base classes must be invoked explicitly
        # even if there is only one that has no argument
        super(Universe, self).__init__()
        
        game_initialize()
        
        self.__window = game_world_create(1, 0)
        self.__window_width, self.__window_height = 0, 0
        self.__fgc, self.__bgc = fgc, bgc
        self.__fps, self.__count = fps, 0

        if self.__fps > 0:
            self.__frame_delta = 1000 // self.__fps
        else:
            self.__frame_delta = 0

        game_world_reset(self.__window, self.__fgc, self.__bgc, True)

        self.__snapshot_rootdir = ""
        
        # Python doesn't need two-step initialization as C++ does
        self.construct(sys.argv)

    def __del__(self):
        """ 析构函数，在对象被销毁时自动调用，默认销毁游戏宇宙 """
        pygame.quit()

# public
    def construct(self, argv):
        """ 给游戏世界一个解析命令行参数的机会，默认什么都不做 """
        pass

    def reflow(self, width, height):
        """ 排列可视化元素，在合适的时候自动调用，默认什么都不做 """
        pass

    def update(self, count, interval, uptime):
        """ 更新游戏世界，定时器到期时自动调用，默认什么都不做 """
        pass

    def draw(self, renderer, x, y, width, height):
        """ 绘制游戏世界，在合适的时候自动调用，默认什么都不做 """
        pass

    def can_exit(self):
        """ 告诉游戏主循环，是否游戏已经结束可以退出了，默认永久运行 """
        return False

    def big_bang(self):
        """ 宇宙大爆炸，开启游戏主循环，返回游戏运行时间 """
        quit_time = 0

        if self.__frame_delta > 0:
            pygame.time.set_timer(pygame.USEREVENT, self.__frame_delta)

        self.__window_width, self.__window_height = self.get_window_size()
        self.begin_update_sequence()
        self._on_big_bang(self.__window_width, self.__window_height)
        self._on_resize(self.__window_width, self.__window_height)
        self._on_game_start()
        self.notify_updated()
        self.end_update_sequence()
        
        while (quit_time == 0) and not self.can_exit():
            e = pygame.event.wait()
            self.begin_update_sequence()

            if e.type == pygame.USEREVENT:
                self.__count += 1
                self._on_elapse(self.__count, self.__frame_delta, pygame.time.get_ticks())
            elif e.type == pygame.MOUSEMOTION:
                self._on_mouse_motion_event(e)
            elif e.type == pygame.MOUSEWHEEL:
                self._on_mouse_wheel_event(e)
            elif e.type == pygame.MOUSEBUTTONUP:
                self._on_mouse_button_event(e, False)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button_event(e, True)
            elif e.type == pygame.KEYUP:
                self._on_keyboard_event(e, False)
            elif e.type == pygame.KEYDOWN:
                self._on_keyboard_event(e, True)
            elif e.type == pygame.VIDEORESIZE:
                self._on_resize(e.w, e.h)    
            elif e.type == pygame.QUIT:
                if self.__frame_delta > 0:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                quit_time = pygame.time.get_ticks()
        
            self.end_update_sequence()

# public
    def set_snapshot_folder(self, path):
        self.__snapshot_rootdir = os.path.normpath(path)

    def snapshot(self):
        return self.__window, False

# public
    def set_window_title(self, title):
        pygame.display.set_caption(title)

    def get_window_title(self):
        title, _ = pygame.display.get_caption()
        return title
    
    def toggle_window_fullscreen(self):
        # This doesn't work for Meta and OpenGL backend
        pygame.display.toggle_fullscreen()

    def set_window_size(self, width, height):
        oldw, oldh = self.get_window_size()
        
        if width <= 0:
            width = oldw

        if height <= 0:
            height = oldh

        if width != oldw or height != oldh:
            self.__window = game_world_create(width, height)

            if (self.__window_width > 0) and (self.__window_height > 0):
                # the universe has been completely initialized
                self._on_resize(width, height)
            else:
                # the big_bang() will do resizing later
                pass

    def get_window_size(self, logical = True):
        if self.__window:
            return self.__window.get_size()
        else:
            return (0, 0)

    def get_renderer_name(self):
        return pygame.display.get_driver()

    def get_foreground_color(self):
        return self.__fgc

    def get_background_color(self):
        return self.__bgc

    def frame_rate(self):
        return self.__fps

# public
    def get_extent(self):
        return self.get_window_size()

    def refresh(self):
        self.__do_redraw(self.__window, 0, 0, self.__window_width, self.__window_height)
        game_world_refresh(self.__window)

# protected (virtual, default)
    def _on_click(self, x, y): pass                                         # 处理单击事件
    def _on_right_click(self, x, y): pass                                   # 处理右击事件
    def _on_double_click(self, x, y): pass                                  # 处理双击事件
    def _on_mouse_move(self, state, x, y, dx, dy): pass                     # 处理移动事件
    def _on_scroll(self, horizon, vertical, hprecise, vprecise): pass       # 处理滚轮事件

    def _on_char(self, key, modifiers, repeats, pressed): pass              # 处理键盘事件
    def _on_text(self, text, size, entire): pass                            # 处理文本输入事件
    def _on_editing_text(self, text, pos, span): pass                       # 处理文本输入事件

# protected
    # 大爆炸之前最后的初始化宇宙机会，默认什么都不做
    def _on_big_bang(self, width, height): pass

    # 宇宙初始化之后，游戏世界开始运行，默认什么都不做
    def _on_game_start(self): pass

    # 响应定时器事件，刷新游戏世界
    def _on_elapse(self, count, interval, uptime):
        """ 响应定时器事件，刷新游戏世界 """
        self.update(count, interval, uptime)

    # 响应鼠标事件，并按需触发单击、右击、双击、移动、滚轮事件
    def _on_mouse_button_event(self, mouse, pressed):
        if not pressed:
            x, y = mouse.pos
            if mouse.button == 1:
                self._on_click(x, y)
            elif mouse.button == 3:
                self._on_right_click(x, y)

    def _on_mouse_motion_event(self, mouse):
        mx, my = mouse.pos
        xrel, yrel = mouse.rel
        self._on_mouse_move(0, mx, my, xrel, yrel)

    def _on_mouse_wheel_event(self, mouse):
        horizon = mouse.x
        vertical = mouse.y
        hprecise = float(horizon)  # mouse.preciseX
        vprecise = float(vertical) # mouse.preciseY

        if mouse.flipped:
            horizon  *= -1
            vertical *= -1
            hprecise *= -1.0
            vprecise *= -1.0

        self._on_scroll(horizon, vertical, hprecise, vprecise)

    # 响应键盘事件，并按需触发按下、松开事件
    def _on_keyboard_event(self, keyboard, pressed):
        keycode = keyboard.key
        keymod = keyboard.mod
        repeat = 1

        if not pressed:
            ctrl_mod = pygame.KMOD_CTRL

            if sys.platform == 'darwin':
                ctrl_mod = ctrl_mod | pygame.KMOD_META

            if keymod & ctrl_mod:
                if keycode == pygame.K_p:
                    self._take_snapshot()
                else:
                    self._on_char(keycode, keymod, repeat, pressed)
            else:
                self._on_char(keycode, keymod, repeat, pressed)
        else:
            self._on_char(keycode, keymod, repeat, pressed)

    # 响应窗体事件，并按需触发尺寸改变事件
    def _on_resize(self, width, height):
        self.__window_width, self.__window_height = width, height

        self.begin_update_sequence()
        game_world_reset(self.__window, self.__fgc, self.__bgc, True)
        self.reflow(width, height)
        self.notify_updated()
        self.end_update_sequence()

    # 处理预设事件
    def _take_snapshot(self):
        bname = self.get_window_title()
        dtime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        basename = "%s-%s.png" % (bname, dtime)

        if self.__snapshot_rootdir:
            snapshot_png = self.__snapshot_rootdir + os.sep + basename
        else:
            snapshot_png = os.getcwd() + os.sep + basename

        if self.save_snapshot(snapshot_png):
            print("A snapshot has been save as '%s'." % snapshot_png)
        else:
            pass

# private
    def __do_redraw(self, renderer, x, y, width, height):
        game_world_reset(renderer, self.__fgc, self.__bgc, False)
        self.draw(renderer, x, y, width, height)
