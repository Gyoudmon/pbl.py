#!/usr/bin/env python3

###############################################################
def strlen_loop(s):
    size = 0

    for c in s:
        size += 1

    return size


###############################################################
def main():
    src = input()
    size = strlen_loop(src)

    print(size)

###############################################################
if __name__ == "__main__":
    main()
