#!/usr/bin/env python3

###############################################################
def make_josephus_circle(n):
    ls = []
    for i in range(1, n + 1):
        ls.append(i)
    return ls

def can_finish(ls):
    return len(ls) <= 1

def count_off(ls, idx):
    return (idx + 3 - 1) % len(ls)

###############################################################
def main():
    n = int(input())
    ls = make_josephus_circle(n)

    idx = 0
    while not can_finish(ls):
        idx = count_off(ls, idx)
        ls.pop(idx)
    
    if (len(ls) > 0):
        print(ls[0])



###############################################################
if __name__ == "__main__":
    main()

