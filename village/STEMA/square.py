#!/usr/bin/env python3

###############################################################
def make_square_dict(n):
    sd = {}
    for i in range(1, n + 1):
        sd[i] = i * i
    return sd

def make_square_dict_elegant(n):
    return { x : x*x for x in range(1, n + 1) }

def to_string(sd, i):
    if i == 1:
        s = "{}:{}".format(i, sd[i])
    else:
        s = ",{}:{}".format(i, sd[i])
    
    return s

def print_square_dict(sd):
    for i in range(1, len(sd) + 1):
        print(to_string(sd, i), end = "")
    print()

###############################################################
def main():
    n = int(input())
    sd = make_square_dict(n)
    print_square_dict(sd)



###############################################################
if __name__ == "__main__":
    main()

