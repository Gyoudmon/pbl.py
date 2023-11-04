#!/usr/bin/env python3

###############################################################
def count_bricks_loop(n):
    该层砖块数 = 0
    总砖块数 = 0
    for 层数 in range(1, n + 1):
        该层砖块数 += 层数
        总砖块数 += 该层砖块数
    return 总砖块数
    
def count_bricks_recursion(n):
    if n <= 0:
        return [0, 0]
    else:
        上层结果 = count_bricks_recursion(n - 1)
        该层砖块数 = 上层结果[0] + n
        总砖块数 = 上层结果[1] + 该层砖块数
        return [该层砖块数, 总砖块数]

###############################################################
def main():
    n = int(input())
    ls = count_bricks_recursion(n)
    print(ls[1])

###############################################################
if __name__ == "__main__":
    main()
