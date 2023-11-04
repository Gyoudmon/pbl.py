#!/usr/bin/env python3

import sys # 系统相关参数和函数

coding_age = 2  # 创建一个全局变量并赋值为整数 2

################################################################################
def main(argc, argv):
    print("Python 学个 " + str(coding_age) + " 年就差不多得了。")

    coding_age = coding_age + 3 # <=== 尝试修改"全局变量", 失败

    return 1



################################################################################
if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))


