#!/usr/bin/env python3

###############################################################
def is_light_on_by_remainder(m):
    return m % 2 == 1

def is_light_on_by_simulation(m):
    if m <= 0:
        return False
    else:
        return not is_light_on_by_simulation(m - 1)

def print_status(is_on):
    if is_on:
        print(1)
    else:
        print(0)

###############################################################
def main():
    m = int(input())
    is_on = is_light_on_by_remainder(m)
    print_status(is_on)

###############################################################
if __name__ == "__main__":
    main()
