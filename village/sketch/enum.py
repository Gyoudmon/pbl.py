#!/usr/bin/env python3

import sys  # 系统相关参数和函数
import enum # 枚举模块

################################################################################
class WeekDay(enum.Enum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

################################################################################
def main(argc, argv):
    day = WeekDay.Tuesday

    if argc > 1:
        day = WeekDay(int(argv[1]))

    print("今天是 {}({}), 它的整型值是 {}。".format(day.name, type(day), day.value))

    return 0



################################################################################
if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
