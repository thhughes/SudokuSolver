__author__ = 'troyhughes'
from Node import Node
import math

class Sudoku:
    def __init__(self, size, populatedBoard):
        if math.floor(math.sqrt(size)) != math.ceil(math.sqrt(size)):
            raise SudokuException("The value you have provided is not a perfect square, "
                                  "therefore you cannot make a Sudoku board out of it")
        self._size = size
        self._b = [[]]
        self._setBoard(populatedBoard)
        self._validList = set()
        for i in xrange(size):
            self._validList.add(Node(i+1,size))




    def __call__(self): return self._b
    def __str__(self):  return self._printCurrentBoard()
    def __repr__(self): return self._printCurrentBoard()


    def _setBoard(self, someBoard):
        self._b = [[]]
        if self._size != len(someBoard) and self._size != len(someBoard[0]):
            raise SudokuException("Board provided does not match set board size")
        self._b = someBoard




    def _printCurrentBoard(self):
        rowDivider = "----------------------"
        for y,row in enumerate(self._b):
            if y % 3 == 0: print rowDivider
            pstring = ""
            for x,val in enumerate(row):
                if (x) % 3 == 0: pstring = pstring+'|'
                pstring = pstring+str(val)+' '
            pstring = pstring+'|'
            print pstring
        print rowDivider
        return ""


    def printDepthMap(self):
        rowDivider = "----------------------"
        for y,row in enumerate(self._b):
            if y % 3 == 0: print rowDivider
            pstring = ""
            for x,val in enumerate(row):
                if (x) % 3 == 0: pstring = pstring+'|'

                try:
                    val = str(len(self.getPossible(y,x)))
                except SudokuException, e:
                    val = str(0)
                pstring = pstring+ val + ' '
            pstring = pstring+'|'
            print pstring
        print rowDivider
        return ""

    def show(self):
        self._printCurrentBoard()
        self.printDepthMap()


    def _inbounds(self,val):
        if val > self._size or val < 0:
            raise SudokuException("Value is out of bounds")




    """ ------------------------------------------
        Getter Functions
    """
    def getBoard(self):
        return self._b

    def getRow(self, val):
        try:
            self._inbounds(val)
        except SudokuException,e:
            print "Get Row Out of bounds Error"
            raise e
        row = []
        emptyNode = Node(None, )
        for i in self._b[val]:
            if not (i == emptyNode):
                row.append(i)
        return row

    def getColumn(self, val):
        try:
            self._inbounds(val)
        except SudokuException,e:
            print "Get Column Out of bounds Error"
            raise e
        column = []
        for row in self._b:
            if not (row[val] == Node(None)):
                column.append(row[val])
        return column

    def getSquare(self, val):
        sq = math.sqrt(self._size)
        row = math.floor(float(val)/sq)
        column = val % sq
        sqResult = []
        for j in xrange(3):
            sqRow = []
            for i in xrange(3):
                if not (self._b[int(row*sq+j)][int(column*sq+i)] == Node(None)):
                    sqRow.append(self._b[int(row*sq+j)][int(column*sq+i)])
            sqResult.append(sqRow)
        return sqResult

    def getSquareFromPoint(self, row, column):
        sq = math.sqrt(self._size)
        cubeRow = math.floor(row/sq)
        cubeColumn = math.floor(column/sq)
        cubeNum = (cubeRow*sq)+cubeColumn

        return int(cubeNum)


    def getPossible(self, row, column):
        if not (self._b[row][column] == Node(None)):
            raise SudokuException("Given node is already filled")
        usedRow = self.getRow(row)
        usedCol = self.getColumn(column)
        usedSq = self.getSquare(self.getSquareFromPoint(row,column))

        totalUsed = set(usedRow)
        for i in usedCol: totalUsed.add(i)
        for row in usedSq:
            for val in row:
                totalUsed.add(val)

        notUsed = list(self._validList - totalUsed)
        return notUsed

    def getDepthOf(self,val):
        depthList = []
        for row,r in enumerate(self._b):
            for column,v in enumerate(r):
                try:
                    possibleList = self.getPossible(row,column)
                    if len(possibleList) == val:
                        depthList.append((possibleList[0],row,column))
                except SudokuException,e:
                    continue
        return depthList

    def getCountOfDepth(self,val):
        counter = 0
        for row,r in enumerate(self._b):
            for column,v in enumerate(r):
                try:
                    possibleList = self.getPossible(row,column)
                    if len(possibleList) == val:
                        counter = counter + 1
                except SudokuException,e:
                    continue
        return counter


    """ -----------------------------------
        Setter Function
    """

    def placeNode(self,value, row, column):
        try:
            possible = self.getPossible(row,column)
        except SudokuException,e:
            raise SudokuNodeException("There are no possible values for this locaiton")

        if not value in possible:
            return False
        else:
            self._b[row][column] = Node(value, self._size)
            return True




class SudokuException(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class SudokuNodeException(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def makeSudokuBoard(fileName):
    f = open(fileName,"r")
    file_content = f.read()
    file_content = file_content.split('\n')
    raw_board = []
    for row in file_content:
        raw_board.append(row.split(','))

    board = []

    for row in raw_board:
        soduku_row = []
        for square in row:
            if square is ' ':
                soduku_row.append(Node(None))
            else:
                soduku_row.append(Node(int(square)))
        board.append(soduku_row)
        soduku_row = []
    return board


# print "Starting"
# makeSudokuBoard('Board00.txt')
# s = Sudoku(9,makeSudokuBoard('Board00.txt'))
# print s
# s.printDepthMap()


