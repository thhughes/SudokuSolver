__author__ = 'troyhughes'
from Sudoku import Sudoku
from Sudoku.Sudoku import InvalidBoard
from Sudoku.Node import NodeException

class SudokuCSP:
    """
    This class uses Constraint Satisfaction to solve Sudoku puzzles.

    The class uses the following constraints:
        - Each row must contian a set of numbers from 1 to n
        - Each column must contain a set of numbers from 1 to n
        - There are n, sqrt(n) by sqrt(n) cubes, creating a board that is n by n
            of which the whole board was sqrt(n) by sqrt(n) boards.
        - Each square contains a set of numbers from 1 to n
        - Because each row and column must be a set of numbers from 1 to n,
            a given set of sqrt(n) rows/columns within a square must contain
            only sqrt(n) copies of a given number.

    The current version of this program (Jan 4, 2016, 10:08:00 AM) does not use
        heuristic search. It is a depth first search algorithm that prioritizes nodes with
        one numeric option, then prioritizes the nodes with the largest number of numeric
        options next.

    Future Updates: The future update is to add a huristic function that evaluates the
        'influence' of filling a node and rates them based off their influence. This means that
        if filling a node will reduce the number of options for 3n-2sqrt(n) (the maximum number
        of nodes impactable if only observing a row, column, and square) then that node should
        be a very high priority. Conversly, if filling a node reduces 0 neighboring nodes, than
        it should be a very low priority.

    Internal Parameters:
        _stack        :: list of Sudoku Boards
                    - This data structure provides the class the ability to dig into the search
                      tree and then back out if a dead end is found. The maximum length of this
                      is m, or the number of empty cells that are presented at the start of the
                      puzzle.
        archiveRecipt :: Integer
                    - This int is used to track the depth of the _stack. Whenever something is
                      Put on the stack this item is incremented. If something is popped from the
                      stack it is decremented.
        currentB      :: Sudoku Board
                    - This is the current sudoku board object being worked with.


    """
    def __init__(self, board):
        """

        :param board: Sudoku Board Object
        :return:
        """
        self._stack = [board]
        self.archiveRecipt = 0



    def solve(self, DEBUG = False):
        """
        This function uses Constraint Satisfaction to solve the sudoku board that is passed
        during the constructor
        :return: Solved Sudoku Board
        """
        print "Solving, please wait..."

        self.currentB = self.getBoard()
        while not self.currentB.isComplete():
            if DEBUG:
                print "DEBUG:"
                print '\t'+"Is current valid", self.currentB.isValid()
                print '\t'+"The number squares to solve", self.currentB.getNumUnsolved()
                print '\t'+"The number of boards stored", self.archiveRecipt
                print '\t'+"The stack contents are"+'\n', self._stack
            try:
                """
                    This section is the general search function. It is the algorithm to find the solution
                    and '_iterate()' will error out with a 'DeadEndError' to be caught in the except.
                """
                while self.currentB.isValid() and not self.currentB.isComplete():
                    oldBoard, newBoard = self._iterate(self.currentB, self._SmallestToLargetList)
                    self._archive(oldBoard, newBoard)
                if not self.currentB.isValid():
                    self._popInvalid()
                self.currentB = self.getBoard()
            except DeadEndError,e:
                """
                    This section happens when the above section finds a dead end. Dead ends happen
                    when there are (y) options where 0 of them are valid. This part get's out of a
                    dead end as opposed to an invalid decision.
                """
                if DEBUG: print "Dead end found, try another route"
                self._popInvalid()
                self.currentB = self.getBoard()
        self.currentB.show()
        return self.currentB

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
        :raise: DeadEndError :: If there are 0 nodes that can be filled in that have not been tried out
                This catches a special case where a valid board exists but none of the soltions from that
                branch of the search tree are valid. THe main portion of the algorithm does not catch
                this so the exception allows it to be caught.
        """

        priorityList = solveAlg(oldBoard)
        nodeList, row, column = priorityList[0]
        newBoard = Sudoku.Sudoku(oldBoard.getSize(), oldBoard.getBoard())
        placedNode = False

        for node in nodeList:
            if newBoard.placeNode(node(), row, column):
                oldBoard.setConstraint(node(), row, column)
                return oldBoard, newBoard

        raise DeadEndError("None of the nodes found are viable, this is a dead end.")



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


    def _SinglesThenLargeNodeLists(self, oldSudoku):
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

    def _SmallestToLargetList(self, oldSudoku):
        totalList = []
        for i in xrange(oldSudoku.getSize()+1):
            totalList.extend(oldSudoku.getDepthOf(i))
        return totalList


class DeadEndError(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)





print "Starting"
s = Sudoku.Sudoku(9,Sudoku.makeSudokuBoard('Sudoku/Board01.txt'))
solver = SudokuCSP(s)
solver.solve()