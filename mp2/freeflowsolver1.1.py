#!/usr/bin/env python
import sys, os.path
from random import sample
from Queue import PriorityQueue
from collections import deque
import copy

count = 0

# ----------- HELPER FUNCTIONS ----------------------- #

def resetGrid(matrix, srcCells, x, y):
    for i in range(y * width + x, width * height):
            if (i % width, int(i / width)) not in srcCells:
               matrix[int(i / width)][i % width] = '_'

# find the next empty space in the matrix
# note that the matrix is indexed by (y,x)
def findNextEmpty(matrix):
    for row in range(0, height):
        for col in range(0, width):
            if matrix[row][col] == '_':
                return (col, row)
    return (0, 0)

# choose val that rules out fewest vals in remaining variables
def leastConstrainingVal():
    return

# choose location with fewest legal values
def mostConstrainedVar():
    return


# ----------- BACKTRACKING FUNCTIONS ----------------- #

def dumbBacktracking(matrix, colorSet, srcCells, currentEmpty, numEmptyCells):
    global count

    if numEmptyCells == 0:
        return 0

    # try each color in the colorset
    for color in sample(colorSet, len(colorSet)):
        # temp = copy.deepcopy(matrix)
        x, y = currentEmpty
        matrix[y][x] = color
        count += 1

        # print '\n'.join([''.join([col for col in row]) for row in matrix])
        # print '---------'

        result = dumbBacktracking(matrix, colorSet, srcCells, findNextEmpty(matrix), numEmptyCells-1)

        # if our assignment met constraints and this still satisfies them, we
        # backtrack check
        if result == 0:
            errorCnt = 0
            for i in range(width):
                for j in range(height):
                    adjCounter = 0
                    if i-1 >= 0 and matrix[j][i-1] == matrix[j][i]:
                        adjCounter += 1
                    if j-1 >=0 and matrix[j-1][i] == matrix[j][i]:
                        adjCounter += 1
                    if i+1 < width and matrix[j][i+1] == matrix[j][i]:
                        adjCounter += 1
                    if j+1 < height and matrix[j+1][i] == matrix[j][i]:
                        adjCounter += 1

                    # print i, j, matrix[j][i], adjCounter
                    # for l in matrix: print l
                    # print '\n'

                    if (adjCounter != 2 and (i, j) not in srcCells) or (adjCounter != 1 and (i, j) in srcCells):
                        errorCnt += 1

                    if errorCnt != 0: break

                    # problem: arbitrarily resetting grid
                    # need to test adj constraint in the order we set them in

            if errorCnt == 0: return 0

        # if current color does not work, clear everything from this position to
        # the end of the matrix and try a new color
        # resetGrid(matrix, srcCells, x, y)
        matrix[y][x] = '_'

    return -1


def smartBacktracking(matrix, colorOptions, srcCells, numEmptyCells):
    global count

    # check if assignment is complete
    if numEmptyCells == 0:
        return 0

    # assign value to cell with fewest options
    colorOptions = sorted(colorOptions)
    colorSetLen, colorSet, currentEmpty = colorOptions[0]
    # print colorSetLen, colorSet, currentEmpty

    # copy matrix and color options (to be reset upon failure)
    # tmpMatrix = copy.deepcopy(matrix)
    # tmpColors = copy.deepcopy(colorOptions)

    # colorOptions.remove((colorSetLen, colorSet, currentEmpty))
    newColorOptions = copy.deepcopy(colorOptions)
    newColorOptions.remove((colorSetLen, colorSet, currentEmpty))

    # try each color in the colorset
    for color in colorSet: # sample(colorSet, len(colorSet)):
        '''
        for l in matrix: print l
        print '\n'
        '''
        x, y = currentEmpty
        matrix[y][x] = color
        # tmpColors = copy.deepcopy(colorOptions)
        # print color, colorOptions
        # print '--------'
        # colorOptions.remove((colorSetLen, colorSet, currentEmpty))
        # print colorOptions
        # print '\n'
        count += 1

        print '\n'.join([''.join([col for col in row]) for row in matrix])
        print '---------'

        # FORWARD CHECKING
        # Idea is to terminate search when no valid color assignments exists
        # most constrained var: choose location with fewest legal values
        # least constraining val: choose val that rules out fewest vals in
        # remaining variables

        # TODO: check adj for all cells & reduce colorSet in colorOptions accordingly

        # newColorOptions = (colorSetLen - 1, colorSet.remove(color), (x, y))
        # oldColorOptions = (colorSetLen, colorSet, currentEmpty)
        # colorOptions.remove((colorSetLen, colorSet, currentEmpty))

        result = smartBacktracking(matrix, newColorOptions, srcCells, numEmptyCells-1)

        # if our assignment met constraints and this still satisfies them, we
        # backtrack check
        if result == 0:
            errorCnt = 0
            # for i in range(width):
            #     for j in range(height):
            adjCounter = 0
            if x - 1 >= 0 and matrix[y][x - 1] == matrix[y][x]:
                adjCounter += 1
            if y - 1 >= 0 and matrix[y - 1][x] == matrix[y][x]:
                adjCounter += 1
            if x + 1 < width and matrix[y][x + 1] == matrix[y][x]:
                adjCounter += 1
            if y + 1 < height and matrix[y + 1][x] == matrix[y][x]:
                adjCounter += 1

            if (adjCounter != 2 and (x, y) not in srcCells) or (adjCounter != 1 and (x, y) in srcCells):
                errorCnt += 1

            # if errorCnt != 0: break

            if errorCnt == 0: return

        # if current color does not work, clear everything from this position to
        # the end of the matrix and try a new color
        # matrix = copy.deepcopy(tmpMatrix)
        matrix[y][x] = '_'
        # print '--------------'
        # print colorSet, color, colorOptions
        # colorOptions.append((len(colorSet), colorSet, currentEmpty))
        # colorOptions = copy.deepcopy(tmpColors)
        # resetGrid(matrix, srcCells, x, y)

    # colorOptions.append(newColorOptions)
    # colorOptions.append((len(colorSet), colorSet, currentEmpty))
    return -1

def main():
    global count
    if not os.path.exists(sys.argv[1]):
        print 'Input file does not exist'
        sys.exit(1)

    # parse input flow free as 2D char matrix
    global width, height

    width = height = 0
    matrix = []
    with open(sys.argv[1], 'r') as flowfree:
        for line in flowfree:
            line = line.strip()
            matrix.append(list(line))
            height += 1
        width = len(matrix[0])

    # iterate through matrix line by line to determine colors, end points
    colors = set()
    endpts = set()
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell != '_':
                colors.add(cell)
                endpts.add((x, y))

    colors = sorted(colors)

    # -- replace the dumb algorithm with smart algorithm here --
    # initial call to the recursive backtracking

    # if dumbBacktracking(matrix, colors, endpts, findNextEmpty(matrix), width*height-len(endpts)) == -1:
    #     print 'No solution to Flow Free puzzle was found!'

    # print '\n'.join([''.join([col for col in row]) for row in matrix])

    '''
    sum = 0
    max = 0
    iters = 1
    for i in range(iters):
        count = 0
        if dumbBacktracking(matrix, colors, endpts, findNextEmpty(
            matrix), width * height - len(endpts)) == -1:
            print 'No sol found'
        else:
            # print 'num assignments: ' + str(count)
            sum += count
            if count > max: max = count


        resetGrid(matrix, endpts, 0, 0)

    sum /= iters
    print 'avg iterations: ' + str(sum)
    print 'max iterations: ' + str(max)
    '''

    # -------------------- SMART ALGO ------------------------ #
    pqueue = PriorityQueue()
    colorOptions = []

    # init priority queue with possible colors for each non source cell
    # len of color choices, set of colors, (x, y)
    for i in range(width):
        for j in range(height):
            if (i, j) not in endpts:
                pqueue.put((len(colors), colors, (i, j)))
                colorOptions.append((len(colors), colors, (i, j)))

    # print pqueue.queue

    # -------------------- COMPUTE ASSIGNMENT ---------------- #

    # if dumbBacktracking(matrix, colors, endpts, findNextEmpty(matrix), width*height-len(endpts)) == -1:
    #     print 'No solution to Flow Free puzzle was found!'

    if smartBacktracking(matrix, colorOptions, endpts, width*height-len(endpts)) == -1:
        print 'No solution to Flow Free puzzle was found!'

    print '\n'.join([''.join([col for col in row]) for row in matrix])

if __name__ == "__main__":
    main()
