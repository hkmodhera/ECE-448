#!/usr/bin/env python
import sys, os.path
from random import sample
from Queue import PriorityQueue

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


# ----------- BACKTRACKING FUNCTIONS ----------------- #

def dumbBacktracking(matrix, colorSet, srcCells, currentEmpty, numEmptyCells):
    if numEmptyCells == 0:
        return 0

    # try each color in the colorset
    for color in sample(colorSet, len(colorSet)):
        x, y = currentEmpty
        matrix[y][x] = color
        count += 1

        # print '\n'.join([''.join([col for col in row]) for row in matrix])
        # print '---------'

        result = dumbBacktracking(matrix, colorSet, srcCells, findNextEmpty(matrix), numEmptyCells-1)

        # if our assignment met constraints and this still satisfies them, we backtrack check
        if result == 0:
            adjCounter = 0
            if x-1 >= 0 and matrix[y][x-1] == color:
                adjCounter += 1
            if y-1 >=0 and matrix[y-1][x] == color:
                adjCounter += 1
            if x+1 < width and matrix[y][x+1] == color:
                adjCounter += 1
            if y+1 < height and matrix[y+1][x] == color:
                adjCounter += 1

            if (adjCounter == 2 and (x, y) not in srcCells) or (adjCounter == 1 and (x, y) in srcCells):
                return 0

        # if current color does not work, clear everything
        # from this position to the end of the matrix and try
        # a new color
        resetGrid(matrix, srcCells, x, y)

    return -1

def smartBacktracking(matrix, colorOptions):
    # if our priority queue has no variable left to assign, the puzzle must be solved
    if colorOptions.empty():
        return True

    mostConstVar = colorOptions.get()
    varDomain = list(mostConstVar[0])    #deep copy of the possible colors for (varX, varY) cell
    varX, varY = mostConstVar[1:]
    
    # if there's no color left to choose, then we clearly hit a dead end
    while varDomain:
        pickColor = varDomain.pop()
    
        # gather information on adjacent cells of current
        emptyNeighbors = []
        sameColorNeighborCt = 0
        if varX-1 >= 0:
            if matrix[varY][varX-1] == '_': 
                emptyNeighbors.append((varX-1, varY))
            elif matrix[varY][varX-1] == pickColor: 
                sameColorNeighborCt += 1
            # else NOT pickColor (do nothing here)
        if varY-1 >=0:
            if matrix[varY-1][varX] == '_': 
                emptyNeighbors.append((varX, varY-1))
            elif matrix[varY-1][varX] == pickColor: 
                sameColorNeighborCt += 1
        if x+1 < width:
             if matrix[varY][varX+1] == '_': 
                emptyNeighbors.append((varX+1, varY))
            elif matrix[varY][varX+1] == pickColor: 
                sameColorNeighborCt += 1
        if y+1 < height 
            if matrix[varY+1][varX] == '_': 
                emptyNeighbors.append((varX, varY+1))
            elif matrix[varY+1][varX] == pickColor: 
                sameColorNeighborCt += 1

        # perform CSP checks for the chosen color
        if len(emptyNeighbors) == 0 and sameColorNeighborCt != 2:
            # choose another color; this one doesn't work
            continue
        elif len(emptyNeighbors) == 1:
            if sameColorNeighborCt == 1:
                # empty neighbor must be restricted to same color
            elif sameColorNeighborCt == 2:
                # empty neighbor cannot be same color
            else: # sameColorNeighborCt == 0 or sameColorNeighborCt == 3:
                continue
        elif len(emptyNeighbors) == 2 and sameColorNeighborCt == 2:
            # empty neighbors cannot be same color
        else
            # color works

    return False

def main():
    if not os.path.exists(sys.argv[1]):
        print 'Input file does not exist'
        sys.exit(1)

    # parse input flow free as 2D char matrix
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

    # iterate through matrix line by line to determine colors, end points
    colors = set()
    endpts = set()
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell != '_':
                colors.add(cell)
                endpts.add((x, y))

    # set up most constrained variable data structure 
    colorOptions = PriorityQueue()
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell == '_':
                colorOptions.put((colors, x, y))  

    #sum = 0
    #max = 0
    #iters = 1000
    #for i in range(iters):
    #    count = 0
    #    if dumbBacktracking(matrix, colors, endpts, findNextEmpty(
    #        matrix), width * height - len(endpts)) == -1:
    #        print 'No solution to Free Flow puzzle was found!'
    #    else:
    #        # print 'num assignments: ' + str(count)
    #        sum += count
    #        if count > max: max = count

    # print '\n'.join([''.join([col for col in row]) for row in matrix])

    # initial call to the dumb backtracking
    
    #count = 0
    #if dumbBacktracking(SET PARAMS HERE) == -1:
    #    print 'No solution to Flow Free puzzle was found!'
    #else:
    #    print 'Solution to the Free Flow puzzle\n'
    #    print '\n'.join([''.join([col for col in row]) for row in matrix])
    #    print '\nnum assignments: ' + str(count)      
    
    # initial call to the smart backtracking
    
    count = 0
    if smartBacktracking(matrix, colorOptions) is False:
        print 'No solution to Flow Free puzzle was found!'
    else:
        print 'Solution to the Free Flow puzzle\n'
        print '\n'.join([''.join([col for col in row]) for row in matrix])
        print '\nnum assignments: ' + str(count)  
    
if __name__ == "__main__":
    main()