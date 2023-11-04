#!/usr/bin/env python3

###############################################################
def parse_scores(src):
    scores = []

    for s in src.split(","):
        scores.append(int(s))

    return scores

def remove_extreme_scores(scores):
    min = 100
    max = 0

    for s in scores:
        if s < min:
            min = s
        elif s > max:
            max = s

    scores.remove(min)
    scores.remove(max)

def compute_average(scores):
    total = 0

    for s in scores:
        total += s

    return total / len(scores)

def compute_competition_average(scores):
    total = 0
    min = 100
    max = 0

    for s in scores:
        total += s

        if s < min:
            min = s
        elif s > max:
            max = s

    return (total - min - max) / (len(scores) - 2)

###############################################################
def main():
    src = input()
    scores = parse_scores(src)
    remove_extreme_scores(scores)
    avg = compute_average(scores)
    print("%.2f" % avg)

###############################################################
if __name__ == "__main__":
    main()
