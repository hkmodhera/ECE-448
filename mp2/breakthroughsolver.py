#!/usr/bin/env python
import sys, os.path
from random import sample
from Queue import PriorityQueue

# --------------------------------- MINIMAX ---------------------------------- #

# returns actions for a player
def getActions(matrix, player, positions):
    actions = list()
    if player == 'A':
        for x, y in p:
            actions.append()
    elif player == 'B':
        for x, y in p:
            pass


    return

# returns a utility value for MAX
def maxVal(matrix, depth):
    # if state is a terminal state, then return the utility at that state


    # v = utility = -infinity

    # for each action in the world state,
    # result = world state after action
    # v = max(v, minVal(result))

    return

# returns a utility value for MIN
def minVal(matrix, depth):
    # if state is a terminal state, then return the utility at that state



    # v = utility = +infinity

    # for each action in the world state,
    # result = world state after action
    # v = min(v, maxVal(result))

    return

# returns an action arg max_(a inACTIONS(s)) minVal(result(state, a))
def minimaxSearch(matrix, positionsA, positionsB):
    # action = default action
    player = 'A'
    # actions = getActions(matrix, player, positionsA)
    actionsA = ['left', 'down', 'right']
    actionsB = ['left', 'up', 'right']
    for p in positionsA:
        for action in actionsA:
            pass

    # for each action in the world state,
    # result = world state after action
    # v = minVal(result)

    # return the action with the max value

    return ('down', (1, 0))


# ------------------------------- ALPHA BETA --------------------------------- #

def alphaBetaSearch():
    return


# ---------------------------------- MAIN ------------------------------------ #

def main():
    if not os.path.exists(sys.argv[1]):
        print 'Input file does not exist'
        sys.exit(1)

    # parse input board as 2D char matrix
    global width, height
    global count

    width = height = 0
    matrix = []
    with open(sys.argv[1], 'r') as flowfree:
        for line in flowfree:
            line = line.strip()
            matrix.append(list(line))
            height += 1
        width = len(matrix[0])

    # for l in matrix: print l

    # top player (black) = A, bottom player (white) = B
    initialPositionsA = [(0, 0), (0, 1), (0, 2), (0, 3),
                         (0, 4), (0, 5), (0, 6), (0, 7),
                         (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7)]

    initialPositionsB = [(6, 0), (6, 1), (6, 2), (6, 3),
                         (6, 4), (6, 5), (6, 6), (6, 7),
                         (7, 0), (7, 1), (7, 2), (7, 3),
                         (7, 4), (7, 5), (7, 6), (7, 7)]

    # for y, x in initialPositionsB: print matrix[y][x]

    action, (x, y) = minimaxSearch(matrix, initialPositionsA, initialPositionsB)
    if action == 'right':
        matrix[y][x] = '_'
        matrix[y + 1][x + 1] = 'A'
    elif action == 'down':
        matrix[x][y] = '_'
        matrix[x + 1][y] = 'A'
    elif action == 'left':
        matrix[y][x] = '_'
        matrix[y + 1][x - 1] = 'A'

    for l in matrix: print l


if __name__ == "__main__":
    main()
