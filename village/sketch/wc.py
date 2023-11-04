#!/usr/bin/env python3

import sys
import io

###################################################################################################
def wc_by_line(src : io.TextIOWrapper):
    line_count = 0

    for _ in src:
        line_count += 1

    print(line_count, end=" ")

    if line_count == 1:
        print("line")
    else:
        print("lines")




###################################################################################################
def main(argc, argv):
    if argc > 1:
        for fname in argv[1:]:
            try:
                src = open(fname, 'r')
                wc_by_line(src)
                src.close()
            except FileNotFoundError:
                pass
    else:
        wc_by_line(sys.stdin)

    return 0



###################################################################################################
if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
