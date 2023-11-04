#!/usr/bin/env python3

from digitama.big_bang.datum.uuid import *
from digitama.big_bang.forward import *

import sys

def main(argv):
    argc = len(argv)

    if argc > 2:
        ids = []
        for i in range(2, len(argv)):
            id = pk64_random()
            while id in ids:
                print("Retrying due to a hash conflict: %s" % id)
                id = pk64_random()
            ids.append(id)

        print("class %s(enum.Enum):" % argv[1])
        for i in range(0, len(ids)):
            print("    %s = 0x%x" % (argv[i + 2], ids[i]))


if __name__=="__main__":
    sys.exit(main(sys.argv))
