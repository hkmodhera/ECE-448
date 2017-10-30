#!/usr/bin/env python
import sys, os.path
from time import time
from random import sample, randint, random
from Queue import PriorityQueue
import copy


# ------------------------------- HEURISTICS --------------------------------- #

def dh1(positions):
    return 2 * len(positions) + random()


def of1(positions):
    return 2 * (30 - len(positions)) + random()


# --------------------------------- HELPERS ---------------------------------- #

# returns actions for a player
def getActions(player, positions):
    # actions = set()
    actions = []

    if player == 'A':
        actions = ['right', 'down', 'left']
        # for x, y in positions:
        #     if x + 1 < height and y + 1 < width:
        #         actions.add('right')
        #     if x + 1 < height:
        #         actions.add('down')
        #     if x + 1 < height and y - 1 >= 0:
        #         actions.add('left')
    elif player == 'B':
        actions = ['right', 'up', 'left']
        # for x, y in positions:
        #     if x - 1 >= 0 and y + 1 < width:
        #         actions.add('right')
        #     if x - 1 >= 0:
        #         actions.add('up')
        #     if x - 1 >= 0 and y - 1 >= 0:
        #         actions.add('left')

    return actions

# get positions for A and B
def getPositions(matrix):
    posA = []
    posB = []

    for x, row in enumerate(matrix):
        for y, val in enumerate(row):
            if val == 'A':
                posA.append((x, y))
            elif val == 'B':
                posB.append((x, y))

    return posA, posB


# --------------------------------- MINIMAX ---------------------------------- #

# returns a utility value for MAX
def maxVal(matrix, depth, positionsA, positionsB):
    # if state is a terminal state, then return the utility at that state
    # if depth == 3:
    #     return

    # v = utility = -infinity
    # v = float('-inf')
    v = -1000000 # -1 * (2**20)
    # depth += 1
    actions = getActions('A', positionsA)

    # for each action in the world state,
    # result = world state after action
    # v = max(v, minVal(result))
    for x, y in positionsA:
        for action in actions: # actionsA:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x + 1 < height and y + 1 < width:
                    if result[x + 1][y + 1] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    elif result[x + 1][y + 1] == 'B':
                        newPositionsB.remove((x + 1, y + 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'down':
                if x + 1 < height:
                    if result[x + 1][y] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y))
                        result[x][y] = '_'
                        result[x + 1][y] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x + 1 < height and y - 1 >= 0:
                    if result[x + 1][y - 1] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    elif result[x + 1][y - 1] == 'B':
                        newPositionsB.remove((x + 1, y - 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    else:
                        continue
                else:
                    continue

            if (depth - 1) < 3:
                val = minVal(result, depth + 1, newPositionsA, newPositionsB)
            else:
                # newDepth = depth
                # val = randint(1, 10)
                val = of1(positionsA)

            # choose the move with the max value
            if val > v:
                # print 'val greater'
                # print v, val
                v = val
                # print v, val
            else:
                # print 'val less than'
                # print v, val
                pass

    return v # , newDepth

# returns a utility value for MIN
def minVal(matrix, depth, positionsA, positionsB):
    # if state is a terminal state, then return the utility at that state
    # if depth == 3:
    #     return
    # print depth

    # v = utility = +infinity
    # v = float('inf')
    v = 1000000 # 2**20
    # depth += 1
    actions = getActions('B', positionsB)

    # for each action in the world state,
    # result = world state after action
    # v = min(v, maxVal(result))
    for x, y in positionsB:
        for action in actions: # actionsB:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x - 1 >= 0 and y + 1 < width:
                    if result[x - 1][y + 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    elif result[x - 1][y + 1] == 'A':
                        newPositionsA.remove((x - 1, y + 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'up':
                if x - 1 >= 0:
                    if result[x - 1][y] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y))
                        result[x][y] = '_'
                        result[x - 1][y] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x - 1 >= 0 and y - 1 >= 0:
                    if result[x - 1][y - 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    elif result[x - 1][y - 1] == 'A':
                        newPositionsA.remove((x - 1, y - 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    else:
                        continue
                else:
                    continue

            if (depth - 1) < 3:
                val = maxVal(result, depth + 1, newPositionsA, newPositionsB)
            else:
                # newDepth = depth
                # val = randint(1, 10)
                val = of1(positionsA)

            # choose the move with the min value
            if val < v:
                v = val

    return v # , newDepth

# returns an action arg max_(a in ACTIONS(state)) minVal(result(state, a))
def minimaxSearch(matrix, depth, positionsA, positionsB):
    player = 'A'

    # action = default action
    # actions = getActions(matrix, player, positionsA)
    # move = ('down', (1, 0))
    v = -1000000
    # depth += 1
    actions = getActions('A', positionsA)

    # for each action in the world state,
    # result = world state after action
    # v = minVal(result)
    for x, y in positionsA:
        for action in actions: # actionsA:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x + 1 < height and y + 1 < width:
                    if result[x + 1][y + 1] == '_':
                        newPositionsA.remove((x,y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    elif result[x + 1][y + 1] == 'B':
                        newPositionsB.remove((x + 1, y + 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'down':
                if x + 1 < height:
                    if result[x + 1][y] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y))
                        result[x][y] = '_'
                        result[x + 1][y] = 'A'
                    elif result[x + 1][y] == 'B':
                        newPositionsB.remove((x + 1, y))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y))
                        result[x][y] = '_'
                        result[x + 1][y] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x + 1 < height and y - 1 >= 0:
                    if result[x + 1][y - 1] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    elif result[x + 1][y - 1] == 'B':
                        newPositionsB.remove((x + 1, y - 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    else:
                        continue
                else:
                    continue

            val = minVal(result, depth + 1, newPositionsA, newPositionsB)

            # val = randint(1, 10)
            # choose the move with the max value
            print val, v, action, x, y
            if val >= v:
                v = val
                move = (action, (x, y))

            # if depth =


    # print depth + 1 # newDepth
    print move
    return move


# ------------------------------- ALPHA BETA --------------------------------- #

# returns a utility value for MAX
def minValAB(matrix, depth, positionsA, positionsB, alpha, beta):
    # if state is a terminal state, then return the utility at that state
    # if depth == 3:
    #     return

    # v = utility = +infinity
    # v = float('+inf')
    v = 1000000 # 2**20
    actions = getActions('A', positionsA)

    # for each action in the world state,
    # result = world state after action
    # v = min(v, maxVal(result))
    for x, y in positionsA:
        for action in actions:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x + 1 < height and y + 1 < width:
                    if result[x + 1][y + 1] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    elif result[x + 1][y + 1] == 'B':
                        newPositionsB.remove((x + 1, y + 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y + 1))
                        result[x][y] = '_'
                        result[x + 1][y + 1] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'down':
                if x + 1 < height:
                    if result[x + 1][y] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y))
                        result[x][y] = '_'
                        result[x + 1][y] = 'A'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x + 1 < height and y - 1 >= 0:
                    if result[x + 1][y - 1] == '_':
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    elif result[x + 1][y - 1] == 'B':
                        newPositionsB.remove((x + 1, y - 1))
                        newPositionsA.remove((x, y))
                        newPositionsA.append((x + 1, y - 1))
                        result[x][y] = '_'
                        result[x + 1][y - 1] = 'A'
                    else:
                        continue
                else:
                    continue

            if (depth - 1) < 4:
                val = maxValAB(result, depth + 1, newPositionsA, newPositionsB, alpha, beta)
            else:
                # newDepth = depth
                # val = randint(1, 10)
                val = of1(positionsB)

            # choose the move with the min value
            if val < v:
                v = val
            if v <= alpha:
                return v
            if v < beta:
                beta = v

    return v  # newDepth

# returns a utility value for MIN
def maxValAB(matrix, depth, positionsA, positionsB, alpha, beta):
    # if state is a terminal state, then return the utility at that state
    # if depth == 3:
    #     return

    # v = utility = -infinity
    # v = float('-inf')
    v = -1000000 # -1 * (2**20)
    actions = getActions('B', positionsB)

    # for each action in the world state,
    # result = world state after action
    # v = max(v, minVal(result))
    for x, y in positionsB:
        for action in actions:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x - 1 >= 0 and y + 1 < width:
                    if result[x - 1][y + 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    elif result[x - 1][y + 1] == 'A':
                        newPositionsA.remove((x - 1, y + 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'up':
                if x - 1 >= 0:
                    if result[x - 1][y] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y))
                        result[x][y] = '_'
                        result[x - 1][y] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x - 1 >= 0 and y - 1 >= 0:
                    if result[x - 1][y - 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    elif result[x - 1][y - 1] == 'A':
                        newPositionsA.remove((x - 1, y - 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    else:
                        continue
                else:
                    continue

            if (depth - 1) < 4:
                val = minValAB(result, depth + 1, newPositionsA, newPositionsB, alpha, beta)
            else:
                # newDepth = depth
                # val = randint(1, 10)
                val = of1(positionsB)

            # choose the move with the min value
            if val > v:
                v = val
            if v >= beta:
                return v
            if v > alpha:
                alpha = v

    return v  # , newDepth

# returns an action arg max_(a in ACTIONS(state)) minVal(result(state, a))
def alphaBetaSearch(matrix, depth, positionsA, positionsB):
    player = 'B'
    v = -1000000

    actions = getActions(player, positionsB)

    # for each action in the world state,
    # result = world state after action
    # v = maxVal(result)
    for x, y in positionsB:
        for action in actions:
            result = copy.deepcopy(matrix)
            newPositionsA = copy.deepcopy(positionsA)
            newPositionsB = copy.deepcopy(positionsB)

            if action == 'right':
                if x - 1 >= 0 and y + 1 < width:
                    if result[x - 1][y + 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    elif result[x - 1][y + 1] == 'A':
                        newPositionsA.remove((x - 1, y + 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y + 1))
                        result[x][y] = '_'
                        result[x - 1][y + 1] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'up':
                if x - 1 >= 0:
                    if result[x - 1][y] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y))
                        result[x][y] = '_'
                        result[x - 1][y] = 'B'
                    elif result[x - 1][y] == 'A':
                        newPositionsA.remove((x - 1, y))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y))
                        result[x][y] = '_'
                        result[x - 1][y] = 'B'
                    else:
                        continue
                else:
                    continue
            elif action == 'left':
                if x - 1 >= 0 and y - 1 >= 0:
                    if result[x - 1][y - 1] == '_':
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    elif result[x - 1][y - 1] == 'A':
                        newPositionsA.remove((x - 1, y - 1))
                        newPositionsB.remove((x, y))
                        newPositionsB.append((x - 1, y - 1))
                        result[x][y] = '_'
                        result[x - 1][y - 1] = 'B'
                    else:
                        continue
                else:
                    continue

            val = maxValAB(result, depth + 1, newPositionsA, newPositionsB, (-1) * 2**20, 2**20)

            # choose the move with the max value
            if val >= v:
                v = val
                move = (action, (x, y))

    print move
    return move


# ---------------------------------- MAIN ------------------------------------ #

def main():
    if not os.path.exists(sys.argv[1]):
        print 'Input file does not exist'
        sys.exit(1)

    # parse input board as 2D char matrix
    global width, height, actionsA, actionsB
    global count
    actionsA = ['left', 'down', 'right']
    actionsB = ['left', 'up', 'right']

    width = height = 0
    matrix = []
    with open(sys.argv[1], 'r') as flowfree:
        for line in flowfree:
            line = line.strip()
            matrix.append(list(line))
            height += 1
        width = len(matrix[0])

    # for l in matrix: print l
    # print width, height

    # top player (black) = A, bottom player (white) = B
    initialPositionsA = [(0, 0), (0, 1), (0, 2), (0, 3),
                         (0, 4), (0, 5), (0, 6), (0, 7),
                         (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7)]

    initialPositionsB = [(6, 0), (6, 1), (6, 2), (6, 3),
                         (6, 4), (6, 5), (6, 6), (6, 7),
                         (7, 0), (7, 1), (7, 2), (7, 3),
                         (7, 4), (7, 5), (7, 6), (7, 7)]

    initialPositionsA55 = [(0, 0), (0, 1), (0, 2), (0, 3),
                           (0, 4), (1, 0), (1, 1), (1, 2),
                           (1, 3), (1, 4)]

    initialPositionsB55 = [(3, 0), (3, 1), (3, 2), (3, 3),
                           (3, 4), (4, 0), (4, 1), (4, 2),
                           (4, 3), (4, 4)]

    initialPositionsA44 = [(0, 0), (0, 1), (0, 2), (0, 3)]

    initialPositionsB44 = [(3, 0), (3, 1), (3, 2), (3, 3)]

    initialPositionsA33 = [(0, 0), (0, 1), (0, 2)]

    initialPositionsB33 = [(2, 0), (2, 1), (2, 2)]


    # for y, x in initialPositionsB: print matrix[y][x]
    '''
    start = time()
    action, (x, y) = minimaxSearch(matrix, 0, initialPositionsA33, initialPositionsB33)
    print (time() - start) * 1000

    if action == 'right':
        matrix[x][y] = '_'
        matrix[x + 1][y + 1] = 'A'
    elif action == 'down':
        matrix[x][y] = '_'
        matrix[x + 1][y] = 'A'
    elif action == 'left':
        matrix[x][y] = '_'
        matrix[x + 1][y - 1] = 'A'

    for l in matrix: print l
    '''

    '''
    start = time()
    action, (x, y) = alphaBetaSearch(matrix, 0, initialPositionsA33, initialPositionsB33)
    print (time() - start) * 1000

    if action == 'right':
        matrix[x][y] = '_'
        matrix[x - 1][y + 1] = 'B'
    elif action == 'up':
        matrix[x][y] = '_'
        matrix[x - 1][y] = 'B'
    elif action == 'left':
        matrix[x][y] = '_'
        matrix[x - 1][y - 1] = 'B'

    for l in matrix: print l
    '''

    turn = 0
    posA = initialPositionsA33
    posB = initialPositionsB33

    while(1):
        print 'turn: ' + str(turn)
        depth = 0

        # check if game is complete
        if 'A' in matrix[height - 1] or 'B' in matrix[0] or len(posA) == 0 or len(posB) == 0:
            break

        if turn == 0:
            # player A's turn
            action, (x, y) = minimaxSearch(matrix, depth, posA, posB)
            if action == 'right':
                matrix[x][y] = '_'
                matrix[x + 1][y + 1] = 'A'
            elif action == 'down':
                matrix[x][y] = '_'
                matrix[x + 1][y] = 'A'
            elif action == 'left':
                matrix[x][y] = '_'
                matrix[x + 1][y - 1] = 'A'
        elif turn == 1:
            # player B's turn
            action, (x, y) = alphaBetaSearch(matrix, depth, posA, posB)
            if action == 'right':
                matrix[x][y] = '_'
                matrix[x - 1][y + 1] = 'B'
            elif action == 'up':
                matrix[x][y] = '_'
                matrix[x - 1][y] = 'B'
            elif action == 'left':
                matrix[x][y] = '_'
                matrix[x - 1][y - 1] = 'B'

        # calculate new positions
        posA, posB = getPositions(matrix)
        print posA, posB

        # next turn
        turn = turn ^ 1

        for l in matrix: print l


if __name__ == "__main__":
    main()
