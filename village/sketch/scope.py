#!/usr/bin/env python3

import sys # 系统相关参数和函数

class ClassData:
    def __init__(self):
        self.var = 3

gvar = 3

ddata = dict()
ddata['var'] = 3

cdata = ClassData()

def main(argc, argv):
    # function cannot modify global variable by default.
    global gvar
    gvar = gvar + 2
    
    # okay
    ddata['var'] = ddata['var'] + 2
    cdata.var = cdata.var + 2

    return 0



# __name__ 是一个特殊变量
# 可用于提示是否从这行代码启动应用程序
# 效果上相当于 C++ 程序的启动器，负责调用 main 函数
if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))


