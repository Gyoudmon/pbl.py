#!/usr/bin/env python3

###############################################################
def elevator_layers(src):
    layers = []

    for token in src.split(","):
        layer = int(token)

        if (layer < 0): layer += 1

        layers.append(layer)

    return layers

def elevator_moves(layers):
    moves = []

    for idx in range(1, len(layers)):
        moves.append(layers[idx] - layers[idx - 1])

    return moves

def compute_cost(moves, upcost, downcost):
    cost = 0.0

    for move in moves:
        if (move < 0):
            cost -= move * downcost
        else:
            cost += move * upcost

    return cost

###############################################################
def main():
    src = input()
    layers = elevator_layers(src)
    moves = elevator_moves(layers)
    cost = compute_cost(moves, 1.0, 0.3)
    print("%.1f" % cost)

###############################################################
if __name__ == "__main__":
    main()
