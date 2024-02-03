#!/usr/bin/env python3

if __name__ == "__main__":
    # 直接赋值
    t = True
    f = False

    # 数值类型到布尔类型的隐式类型转换
    pi = bool(3.14)
    zero = bool(0.0)

    print("变量 t 的值是 %s" % (t))
    print("变量 f 的值是 %s" % (f))
    print("变量 pi 的值是 %s" % (pi))
    print("变量 zero 的值是 %s" % (zero))
