import random

# 场景：邹忌讽齐王纳谏

# 定义类和方法
class Person(object):
    def __init__(self, name, good_looking = random.randint(1, 10)):
        self.name = name
        self.颜值 = good_looking
        print(f"{name}已就绪")

    # 人会臭美，喜欢问别人谁颜值高
    def 问(self, 回答者, 比较者):
        print(f"{self.name}: 吾孰与{比较者.name}美？")
        回答者.曰(self, 比较者)
    
    # 人会奉承，见人说人话 见鬼说鬼话
    def 曰(self, 提问者, 比较者):
        print(f"{self.name}: 君美甚，{比较者.name}何能及君也！")

    # 人会自省，但多少有点偏心，即使颜值相同也会觉得自己更美
    def 自省(self, 比较者):
        if self.颜值 < 比较者.颜值:
            print(f"[{self.name}窥镜而自视：吾诚知不如{比较者.name}美！]")
        else:
            print(f"[{self.name}窥镜而自视：吾诚知{比较者.name}何能及吾也！]")

# 角色就绪
邹忌 = Person("邹忌", 8)
徐公 = Person("徐公", 10)

妻 = Person("妻")
妾 = Person("妾")
客 = Person("客")

# 完整还原情景
邹忌.问(妻, 徐公)
邹忌.问(妾, 徐公)
邹忌.问(客, 徐公)
邹忌.自省(徐公)
