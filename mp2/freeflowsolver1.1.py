#!/usr/bin/env python
import sys, os.path, copy
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

def findNeighborsColors(matrix, cmpColor, curX, curY):
    emptyNeighbors = []
    sameColorNeighbors = []
    if curX - 1 >= 0:
        if matrix[curY][curX-1] == '_': 
            emptyNeighbors.append((curX - 1, curY))
        elif matrix[curY][curX-1] == cmpColor: 
            sameColorNeighbors.append((curX - 1, curY))
        # else NOT same color as cmpColor (do nothing here)
    if curY - 1 >= 0:
        if matrix[curY-1][curX] == '_': 
            emptyNeighbors.append((curX, curY - 1))
        elif matrix[curY-1][curX] == cmpColor: 
            sameColorNeighbors.append((curX, curY - 1))
    if curX + 1 < width:
        if matrix[curY][curX+1] == '_': 
            emptyNeighbors.append((curX + 1, curY))
        elif matrix[curY][curX+1] == cmpColor:
            sameColorNeighbors.append((curX + 1, curY))
    if curY + 1 < height:
        if matrix[curY+1][curX] == '_': 
            emptyNeighbors.append((curX, curY + 1))
        elif matrix[curY+1][curX] == cmpColor: 
            sameColorNeighbors.append((curX, curY + 1))
    return (emptyNeighbors, sameColorNeighbors)

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

def smartBacktracking(matrix, colorOptions, srcCellsSet):
    # if our priority queue has no variable left to assign, the puzzle must be solved
    if colorOptions.empty():
        # for srcCellX, srcCellY in srcCellsSet:
        #     srcCellColor = matrix[srcCellY][srcCellX]
        #     _, sameColNeighbors = findNeighborsColors(matrix, srcCellColor, srcCellX, srcCellY)
        #     if len(sameColNeighbors) != 1:
        #         return False
        return True

    mostConstVar = colorOptions.get()
    try:
        varDomain = list(mostConstVar[0])    #deep copy of the possible colors for (varX, varY) cell
        varX, varY = mostConstVar[1:]
    except Exception:
        print '----------'
        print mostConstVar

    # if there's no color left to choose, then we clearly hit a dead end
    while varDomain:
        pickColor = varDomain.pop()

        print '\n'.join([''.join([col for col in row]) for row in matrix])
        print '--------- (%d, %d): %c' % (varX, varY, pickColor)

        # gather information on adjacent cells of current
        emptyNeighbors, sameColorNeighbors = findNeighborsColors(matrix, pickColor, varX, varY)
        if len(sameColorNeighbors) == 2:
            (x1, y1), (x2, y2) = sameColorNeighbors[:]
            if x1 != x2 and y1 != y2:
                cornerX = x1 if x1 != varX else x2
                cornerY = y1 if y1 != varY else y2
                if matrix[cornerY][cornerX] == pickColor:
                    continue    # if corner color matches pick, change to avoid zigzag

        # perform CSP checks for the chosen color
        saveTmpVars = []
        if len(emptyNeighbors) == 0 and len(sameColorNeighbors) != 2:
            continue    # choose another color; this one doesn't work
        elif len(emptyNeighbors) == 1:
            if len(sameColorNeighbors) == 1:
                # empty neighbor must be restricted to same color
                tempStorage = []
                while not colorOptions.empty():
                    tmpVar = colorOptions.get()
                    if tmpVar[1:] in emptyNeighbors:
                        saveTmpVars.append(copy.deepcopy(tmpVar))
                        tempStorage.append( ([pickColor], tmpVar[1], tmpVar[2]) )
                        break    # we found the only empty neighbor whose domain we want to restrict
                    else:
                        tempStorage.append(tmpVar)
                [colorOptions.put(var) for var in tempStorage]
            elif len(sameColorNeighbors) == 2:
                # empty neighbor cannot be same color
                tempStorage = []
                while not colorOptions.empty():
                    tmpVar = colorOptions.get()
                    if tmpVar[1:] in emptyNeighbors:
                        saveTmpVars.append(copy.deepcopy(tmpVar))
                        tmpVar[0].remove(pickColor)
                        tempStorage.append(tmpVar)
                        break    # we found the only empty neighbor whose domain we want to restrict
                    else:
                        tempStorage.append(tmpVar)
                [colorOptions.put(var) for var in tempStorage]
            else: # sameColorNeighborCt == 0 or sameColorNeighborCt == 3:
                continue    # pickColor doesn't work; try next available color
        elif len(emptyNeighbors) == 2:
            if len(sameColorNeighbors) == 0:      # empty neighbors have to be same color
                tempStorage = []
                while not colorOptions.empty():
                    tmpVar = colorOptions.get()
                    if tmpVar[1:] in emptyNeighbors:
                        saveTmpVars.append(copy.deepcopy(tmpVar))
                        tempStorage.append( ([pickColor], tmpVar[1], tmpVar[2]) )
                    else:
                        tempStorage.append(tmpVar)
                [colorOptions.put(var) for var in tempStorage]
            elif len(sameColorNeighbors) == 2:    # empty neighbors cannot be same color
                tempStorage = []
                while not colorOptions.empty():
                    tmpVar = colorOptions.get()
                    if tmpVar[1:] in emptyNeighbors:
                        saveTmpVars.append(copy.deepcopy(tmpVar))
                        try:
                            tmpVar[0].remove(pickColor)
                        except Exception:
                            pass
                        tempStorage.append(tmpVar)
                    else:
                        tempStorage.append(tmpVar)
                [colorOptions.put(var) for var in tempStorage]
        print 'saveTmpVars before: ' + str(saveTmpVars)
        print 'varDomain before: ' + str(varDomain)
        print '--------- (%d, %d): %c' % (varX, varY, pickColor)
        # else: color works; move onto recursive call

        matrix[varY][varX] = pickColor
        if smartBacktracking(matrix, colorOptions, srcCellsSet) is True:
            return True
        else:
            matrix[varY][varX] = '_'
            print 'saveTmpVars after: ' + str(saveTmpVars)
            print 'varDomain after: ' + str(varDomain)
            print '--------- (%d, %d): %c' % (varX, varY, pickColor)
            if saveTmpVars:
                tempStorage = []
                while not colorOptions.empty():
                    tmpVar = colorOptions.get()
                    if tmpVar[1:] not in emptyNeighbors:
                        tempStorage.append(tmpVar)
                [colorOptions.put(var) for var in tempStorage]
                [colorOptions.put(var) for var in saveTmpVars]

    colorOptions.put(mostConstVar)  # restore most constrained var if path is not part of soln
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

    # ---- THIS EXTRA CHECK MAKES THE 5x5 PUZZLE WORK ----- #
    # Some how need to do something like this at the beginning of the recursion
    coordColorOptions = []
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            empty = []
            if cell != '_':
                print x, y
                if x - 1 >= 0:
                    if matrix[y][x-1] == '_': 
                        empty.append((x - 1, y))
                if y - 1 >= 0:
                    if matrix[y-1][x] == '_': 
                        empty.append((x, y - 1))
                if x + 1 < width:
                    if matrix[y][x+1] == '_': 
                        empty.append((x + 1, y))
                if y + 1 < height:
                    if matrix[y+1][x] == '_': 
                        empty.append((x, y + 1))
                if len(empty) == 1:
                    i, j = (empty[0][0], empty[0][1])
                    coordColorOptions.append((empty[0][0], empty[0][1]))
                    # colorOptions.put(([cell], empty[0][0], empty[0][1]))
                    matrix[j][i] = cell
                    print colorOptions.queue, empty

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell == '_' and (x,y) not in coordColorOptions:
                colorOptions.put((colors, x, y))

    print '-----------'
    print colorOptions.queue

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
    if smartBacktracking(matrix, colorOptions, endpts) is False:
        print 'No solution to Flow Free puzzle was found!'
    else:
        print 'Solution to the Free Flow puzzle\n'
        print '\n'.join([''.join([col for col in row]) for row in matrix])
        print '\nnum assignments: ' + str(count)  
    
if __name__ == "__main__":
    main()