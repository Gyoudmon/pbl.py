#!/usr/bin/env python3

def initialize_array(a, row, col):
    for r in range(0, row):
        for c in range(0, col):
            a[r][c] = (r, c)

def print_array(a):
    for r in range(0, len(a)):
        print(a[r])

###############################################################################
if __name__ == "__main__":
    ROW_SIZE = 8
    COL_SIZE = 5

    print("wrong arrays")
    wrong_as = [[0] * COL_SIZE] * ROW_SIZE
    initialize_array(wrong_as, ROW_SIZE, COL_SIZE)
    print_array(wrong_as)

    print()
    print("list comprehension")
    right_as = [[0 for c in range(COL_SIZE)]
                 for r in range(ROW_SIZE)]
    initialize_array(right_as, ROW_SIZE, COL_SIZE)
    print_array(right_as)
