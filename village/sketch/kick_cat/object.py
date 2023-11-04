# 场景：踢猫效应

# 自然语言描述：小孩很气愤，就用左脚踢了身边的猫
# 提取关键词：左脚 踢 猫 => 左 踢 猫
# 调整语序：踢 猫 左

# 1. 可以将主语信息以补语形式给出(并适当调整变量名)
def 踢(猫, 谁, 这只):
    # 根据函数签名，还原自然语言描述
    # kick the cat with one's this foot
    print(f"踢{猫}, 用{谁}的{这只}脚, {猫}很气愤")

# 2. 主语作为“对象”

# 定义类和方法
class BadPerson(object):
    def __init__(self, name):
        # 坏人有名字，用于通报批评
        self.name = name
        print(f"{name}已就绪")

    # 坏人会踢人
    # 方法令人不齿：欺软怕硬，欺负弱小
    # 不过，坏人一旦踢了人，大家就都知道坏人是谁了
    def 踢(self, 弱者, 这只):
        # 根据方法签名，还原自然语言描述
        # I kick the cat with this foot
        print(f"{self.name}用{这只}脚踢了{弱者}, {弱者}很气愤")

# 角色就绪
老板 = BadPerson("老板")
员工 = BadPerson("员工")
孩子 = BadPerson("孩子")

# 完整还原情景
老板.踢(员工.name, "左")
员工.踢(孩子.name, "左")
孩子.踢("猫", "左")
