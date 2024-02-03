#!/usr/bin/env python3

def display_the_truth_table(a, b):
    print("%s\t\t%s\t\t" % (a, b), end="")
    print("%s\t\t%s\t\t" % (not a, not b), end="")
    print("%s\t\t%s\t\t" % (a and b, a or b))

if __name__ == "__main__":
    print("A\t\tB\t\tnot A\t\tnot B\t\tA and B\t\tA or B")

    display_the_truth_table(False, False)
    display_the_truth_table(False, True)
    display_the_truth_table(True, False)
    display_the_truth_table(True, True)
