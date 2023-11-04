#!/usr/bin/env python3

'''
若无特别设置，Python 软件包即为其 main 模块所在目录
如果使用相对路径导入其他模块，则所有被导入模块不能位于包外
因此，存放于子目录里的“过程式”示例程序不能构成独立 main 模块
否则就是“programming by coincidence”(撞大运式编程)
故此额外添加本脚本用于临时启动示例程序
'''

# 要运行其他示例程序，请修改下面的“from”路径
from village.procedural.paddleball import *  # 导入当前要启动的游戏

# __name__ 是一个特殊变量
# 可用于提示是否从这行代码启动应用程序
# 效果上相当于 C++ 的 main 函数，用以启动游戏

if __name__=="__main__":

    # 混沌初开，宇宙诞生，游戏世界就绪
    # Python 设计在惯例上无需 C++ 那样的“两步初始化”
    universe = PaddleBallWorld()

    # 宇宙大爆炸
    # 开启游戏主循环，直到玩家关闭游戏
    universe.big_bang()

    # Python 心满意足地退出
    # 顺便销毁游戏宇宙，回归虚无
    sys.exit(0)
