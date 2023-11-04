#!/usr/bin/env python3

###############################################################
def is_divisible(m, n):
    return (m % n == 0)

def print_datum(z, i, M):
    if i > 0:
        print(",", end = "")

    print(z, end = "")

###############################################################
def main():
    M = int(input())
    N = int(input())

    i = 0
    for z in range(M, N+1):
        if is_divisible(z, 7) and not is_divisible(z, 5):
            print_datum(z, i, M)
            i += 1
    
    print()



###############################################################
if __name__ == "__main__":
    main()

