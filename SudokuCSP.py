__author__ = 'troyhughes'
from Sudoku import board
from Sudoku.board import InvalidBoard
from Sudoku.Node import NodeException

class SudokuCSP:
    def __init__(self, board):
        self._stack = [board]
        self.archiveRecipt = 0



    def solve(self):
        self.currentB = self.getBoard()
        while not self.currentB.isComplete():
            # print "DEBUG:"
            # print '\t'+"Is current valid", self.currentB.isValid()
            # print '\t'+"The number squares to solve", self.currentB.getNumUnsolved()
            # print '\t'+"The number of boards stored...", len(self._stack)
            # print '\t'+"The stack contents are"+'\n', self._stack
            try:
                while self.currentB.isValid() and not self.currentB.isComplete():
                    oldBoard, newBoard = self._iterate(self.currentB, self._solveOne)
                    self._archive(oldBoard, newBoard)
                if not self.currentB.isValid():
                    self._popInvalid()
                self.currentB = self.getBoard()
            except DeadEndError,e:
                print e
                self._popInvalid()
                self.currentB = self.getBoard()
        self.currentB.show()

    ## ------------------------------------------------------------------------

    def _iterate(self, oldBoard, solveAlg):
        """
        The iterate function should:
            Execute a solving alrogithm (passed in args?)
            Have a way to catch the algorithm if it executes a previosly run node placement
            Inform the old board of the new board's decision.

        :param board: this is the sudoku board to run the algorithm on
        :param solveAlg: this is the solving algorithm that takes in a board and a decision function
        :return: newBoard, oldBoard :: each Board is a Sudoku Board
        """

        priorityList = solveAlg(oldBoard)
        nodeList, row, column = priorityList[0]
        newBoard = board.Sudoku(oldBoard.getSize(), oldBoard.getBoard())
        placedNode = False

        for node in nodeList:
            if newBoard.placeNode(node(), row, column):
                oldBoard.setConstraint(node(), row, column)
                placedNode = True
                break

        if placedNode == False:
            raise DeadEndError("None of the nodes found are viable, this is a dead end.")
        return oldBoard, newBoard



    def _archive(self, oldBoard, newBoard):
        """
        The archive function should:
            Archive the past board into the cache
            Mutate the current 'currentB' to fit the current board

        :param newBoard: to be archived
        :return: None
        """
        self.archiveRecipt = self.archiveRecipt + 1
        # print "ARCHIVE: \t\t ", self.archiveRecipt

        self._stack[-1] = oldBoard
        self._stack.append(newBoard)
        self.currentB = self.getBoard()


    def _popInvalid(self):
        """
        This function should remove the old incorrect board from the chache
        :return:
        """
        # print "DELETE: \t\t ", self.archiveRecipt
        self.archiveRecipt = self.archiveRecipt - 1
        if self.archiveRecipt < 0:
            raise RuntimeError("Popped too many boards")
        return self._stack.pop()


    def getBoard(self):
        """
        :return: The most recent board pushed to the cache
        """
        return self._stack[-1]  ## Last item on the stack is the -1'th item, aka the last item added.


    def setConstraint(self, board, value, row, column):
        """
        This set's a node constraint that tells a node it cannot be a specific value
        :param board: List of List of <Node> :: Representation of the sudoku board
        :param value: <int>
        :param row:   <int>
        :param column: <int>
        :return: Boolean : T-it correctly made the constraint, F-the value is not possible
        :raise : SudokuException : the Node you want to get is not reachable.
        """
        board.setConstraint(value, row, column)


    ## ------------------------------------------------------------------------


    def _solveOne(self, oldSudoku):
        """
        This function takes in a board and an evaluation function. From those it returns a priority list of
        node solutions to try.

        :param sudokuBoard:  sudoku Board
        :return: priority list of (([list of node solutions],row<int>,column<int>))
        """
        onesList = oldSudoku.getDepthOf(1)
        totalList = []
        totalList.extend(onesList)
        for i in list(range(1+1,oldSudoku.getSize()+1)):
            totalList.extend(oldSudoku.getDepthOf(i))
        return totalList


class DeadEndError(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)





print "Starting"
s = board.Sudoku(9,board.makeSudokuBoard('Sudoku/Board01.txt'))
solver = SudokuCSP(s)
solver.solve()