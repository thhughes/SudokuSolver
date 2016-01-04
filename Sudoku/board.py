__author__ = 'troyhughes'
from Node import Node
from Node import NodeException
import math

class Sudoku:
    """
        This is the Sudoku Board class. It was constructed to represent n by n sudoku boards
        where the sudoku cubes in the board are sqrt(n) by sqrt(n).

    """
    def __init__(self, size, populatedBoard):
        """

        :param size: <int> representing the n in the n by n sudoku board
        :param populatedBoard : list of lists of Nodes where there are n items in each list.
        :raise:
            SudokuException if n doe not contain a round square root.
            SudokuException if each list does not contain n items
        """
        if math.floor(math.sqrt(size)) != math.ceil(math.sqrt(size)):
            raise SudokuException("The value you have provided is not a perfect square, "
                                  "therefore you cannot make a Sudoku board out of it")
        self._size = size
        self._b = [[]]
        if not (len(populatedBoard) == self._size):
            raise SudokuException("You don not have enough Row's in this sudoku board")
        for r,row in enumerate(populatedBoard):
            if not (len(row)==self._size):
                raise SudokuException("Row "+str(r)+" does not have the proper number of elements (zero indexed)")

        self._setBoard(populatedBoard)
        self._validSet = set()

        ## Create a '_validSet' of nodes to know the allowable nodes
        for i in xrange(size):
            self._validSet.add(Node(i+1,maxSize=size))




    def __call__(self): return self._b
    def __str__(self):  return self._printCurrentBoard()
    def __repr__(self): return self._printCurrentBoard()


    def _setBoard(self, someBoard):
        """
        stores a list of list of Nodes in the class. Does it in a way that the class can manipulate it
        and ensure that this is not linked by reference to another class.

        :param: someBoard : List of List of Nodes
        """
        self._b = []
        if self._size != len(someBoard) and self._size != len(someBoard[0]):
            raise SudokuException("Board provided does not match set board size")

        for i,row in enumerate(someBoard):
            temp = []
            for j,val in enumerate(row):
                # if i == 0 and j == 1:
                    # print "board._setBoard..VALs", i,j,val.usedVals()
                    # a = Node(val(), usedList=val.usedVals(), maxSize=self._size, minSize=1)
                    # print "THe a'th node is: ", a
                    # print "It's used vals are:", a.usedVals()
                temp.append(Node(val(), val.usedVals(), self._size, 1))
            self._b.append(temp)



    def _printCurrentBoard(self):
        NineStage = "--0-1-2--3-4-5--6-7-8"
        rowDivider = "----------------------"
        print '\n'
        # print NineStage
        for y,row in enumerate(self._b):
            if y % 3 == 0: print rowDivider
            # pstring = ""+str(y)
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
                    val = str(len(self.getPossibleCheckingSurrounding(y,x, True)))
                except SudokuException, e:
                    val = 'x'
                pstring = pstring+ val + ' '
            pstring = pstring+'|'
            print pstring
        print rowDivider
        return ""

    def show(self):
        print '\n'
        print "This board complete and valid stats: "
        print "Complete", self.isComplete()
        print "Valid", self.isValid()
        self._printCurrentBoard()
        self.printDepthMap()


    def _inbounds(self,val):
        if val > self._size or val < 0:
            raise SudokuException("Value is out of bounds")


    """ ------------------------------------------
        Board Checking Operations
    """
    def isComplete(self):
        """
            Check if the board is complete.
        """
        for i in xrange(self._size):
            if not (len(set(self.getRow(i))) == len(self.getRow(i))) or \
                    not (len(self.getRow(i)) == self._size):
                return False
            if not (len(set(self.getColumn(i))) == len(self.getColumn(i))) or \
                    not (len(self.getColumn(i)) == self._size):
                return False
            if not (len(set(self.getSquare(i))) == len(self.getSquare(i))) or \
                    not (len(self.getSquare(i)) == self._size):
                return False
        return True

    def isValid(self):
        """
        Need to check all non-none elements to see if there is a depth greater than zero
        for all non-filled in squares.

        Collect a list of non items, then run the comparison on all of them.

        """

        for row, r in enumerate(self._b):
            for column,item in enumerate(r):
                try:
                    l = self.getPossible(row, column)
                    if len(l) < 1 and item == Node(None):
                        return False
                except SudokuException,e:
                    continue
        return True







    """ ------------------------------------------
        Getter Functions
    """
    def getSize(self): return self._size
    def getBoard(self): return self._b

    def getRow(self, val):
        """
        This get's all the valid used nodes in a row.
        :param : Val : <int> Integer inside the row space of the sudoku board
        """
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
        """
        This get's all the valid used nodes in a column.
        :param : Val : <int> Integer inside the column space of the sudoku board
        """
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
        """
        This get's all the valid used nodes in a soduku Square.
        :param : Val : <int> Integer inside the square space of the sudoku board
        """

        sq = math.sqrt(self._size)
        row = math.floor(float(val)/sq)
        column = val % sq
        sqResult = []
        for j in xrange(3):
            # sqRow = []
            for i in xrange(3):
                if not (self._b[int(row*sq+j)][int(column*sq+i)] == Node(None)):
                    sqResult.append(self._b[int(row*sq+j)][int(column*sq+i)])
            # sqResult.append(sqRow)
        return sqResult

    def getSquareFromPoint(self, row, column):
        """ Given a point on the board, return the square of which it resides"""
        sq = math.sqrt(self._size)
        cubeRow = math.floor(row/sq)
        cubeColumn = math.floor(column/sq)
        cubeNum = (cubeRow*sq)+cubeColumn

        return int(cubeNum)


    def getPossible(self, row, column):
        """
        :param: row<int>,
        :param: column<int>

        :return: List<Nodes>
        :raise : SudokuException if that node has already been filled.
        """
        if not (self._b[row][column] == Node(None)):
            raise SudokuException("Given node is already filled")

        usedRow = self.getRow(row)
        usedCol = self.getColumn(column)
        usedSq = self.getSquare(self.getSquareFromPoint(row,column))

        totalUsed = set(usedRow)
        for i in usedCol: totalUsed.add(i)
        for i in usedSq: totalUsed.add(i)

        notUsed = list(self._validSet - totalUsed)
        return notUsed

    def getPossibleCheckingSurrounding(self, row, column, checkSurroundings=True):
        """

        :param row: <int>
        :param column: <int>
        :param checkSurroundings: <boolean>
        :return: List of possible Nodes
        """
        sq = math.sqrt(self._size)
        cubeRow = math.floor(row/sq)
        cubeColumn = math.floor(column/sq)

        possibleList = self.getPossible(row, column)
        sim = set([])
        aSurCol, aSurRow, bSurCol, bSurCol = [],[],[],[]

        if checkSurroundings:
            aSurRow, bSurRow = self._getSurRow(cubeRow, row)
            aSurCol, bSurCol = self._getSurCol(cubeColumn, column)

            for item in possibleList:
                if (item in aSurRow) and (item in bSurRow) and (item in aSurCol) and (item in bSurCol):
                    sim.add(item)
        if len(sim) == 1:
            simList = list(sim)
            return simList
        elif len(sim) > 1:
            """
                This is the similarity list check. this means that of the values that are possible, if that
                value is used in all of the surrounding row's and columns, then that value is 'similar' and
                is the ONLY possible value for that locaiton. HOWEVER, if by some reaoson there are more than
                one values being passed through the simList, then it is important to find that out and catch it.
                It should NEVER happen.
            """
            print "Multiple sim Length"
            print " Possible List: ",possibleList
            print " Surrounding Row's ",aSurRow, bSurRow
            print " Surrounding Col's ",aSurCol, bSurCol
            print " Sim List", sim
            raise RuntimeError("SimList has failed by having multiple values.")
        else:
            return possibleList

    def getDepthOf(self,val):
        """
        Return a list of the specific depth of the nodes not yet selected.

        :param: val<int>: depth of square you're looking for
        :return: List<[possible Values],row,column> :: touple

        """
        depthList = []
        for row,r in enumerate(self._b):
            for column,v in enumerate(r):
                try:
                    possibleList = self.getPossibleCheckingSurrounding(row,column, True)
                    if len(possibleList) == val:
                        depthList.append((possibleList,row,column))

                except SudokuException,e:
                    continue
        return depthList

    def getCountOfDepth(self,val):
        """
        :param: val<int> depth of square you're looking for
        :return: <int> number of the depth you were looking for.
        """
        counter = 0
        for row,r in enumerate(self._b):
            for column,v in enumerate(r):
                try:
                    possibleList = self.getPossibleCheckingSurrounding(row,column, True)
                    if len(possibleList) == val:
                        counter = counter + 1
                except SudokuException,e:
                    continue
        return counter

    def getNumUnsolved(self):
        """ Returns the number of unsolved nodes in a puzzle"""
        counter = 0
        for row,r in enumerate(self._b):
            for column,v in enumerate(r):
                try:
                    possibleList = self.getPossibleCheckingSurrounding(row,column)
                    counter = counter + 1
                except SudokuException,e:
                    continue
        return counter

    def _getSurCol(self, cubeCol, col):
        """

        :param cubeCol<int>: The colomn cube that your column is in.
        :param col<int>    : The column that you want surroundings for
        :return AList,BList: List of Nodes representing the two columns surrounding the col passed.
        """
        colMod = (col) % 3
        ASet = set()
        BSet = set()

        if colMod == 0:
            for i in self.getColumn(col+1): ASet.add(i)
            for j in self.getColumn(col+2): BSet.add(j)
        elif colMod == 1:
            for i in self.getColumn(col+1): BSet.add(i)
            for j in self.getColumn(col-1): ASet.add(j)
        elif colMod == 2:
            for i in self.getColumn(col-1): ASet.add(i)
            for j in self.getColumn(col-2): BSet.add(j)

        AList = list(ASet)
        BList = list(BSet)
        return AList,BList

    def _getSurRow(self, cubeRow, row):
        """

        :param cubeRow<int>: The Row cube that your Row is in.
        :param Row<int>    : The Row that you want surroundings for
        :return AList,BList: List of Nodes representing the two Rows surrounding the row passed.
        """
        rowMod = (row) % 3
        ASet = set()
        BSet = set()

        if rowMod == 0:
            for i in self.getRow(row+1): ASet.add(i)
            for j in self.getRow(row+2): BSet.add(j)
        elif rowMod == 1:
            for i in self.getRow(row+1): BSet.add(i)
            for j in self.getRow(row-1): ASet.add(j)
        elif rowMod == 2:
            for i in self.getRow(row-1): ASet.add(i)
            for j in self.getRow(row-2): BSet.add(j)

        AList = list(ASet)
        BList = list(BSet)
        return AList,BList

    """ -----------------------------------
        Setter Function
    """

    def placeNode(self,value, row, column):
        """
        Fills a node with a value.
        :param value: <int> between 1 and self._size (n)
        :param row:   <int> between 0 and self._size-1 (n-1)
        :param column: <int> between 0 and self._size-1 (n-1)
        :return: Boolean : True if the value was placed. False if the value was not ecause it's not possible or
                            was already used.
        """
        try:
            possible = self.getPossible(row,column)
        except SudokuException,e:
            raise SudokuNodeException("There are no possible values for this locaiton")

        if not value in possible:
            return False
        elif value in self._b[row][column].usedVals():
            return False
        else:
            self._b[row][column].setVal(value)
            return True

    def setConstraint(self, value, row, column):
        """
        This set's a node constraint that tells a node it cannot be a specific value. Constraints should
        only be added to nodes that don't have a point already set.
        :param board: List of List of <Node> :: Representation of the sudoku board
        :param value: <int>
        :param row:   <int>
        :param column: <int>
        :return: Boolean : T-it correctly made the constraint, F-the value is not possible
        :raise : SudokuException : the Node you want to get is not reachable.
        """
        try:
            self._b[row][column].addConstraint(value)

        except SudokuException,e:
            raise SudokuNodeException("There are no possible values for this locaiton")



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

class InvalidBoard(Exception):
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