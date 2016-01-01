__author__ = 'troyhughes'
from Sudoku import board
from Sudoku.board import InvalidBoard

class SudokuCSP:
    def __init__(self, board):
        self.b = board
        self.bold = self.b



    def solve(self):
        print "Starting to solve:"
        self.b.show()
        print "Go."
        for i in xrange(20):
            if self._solveOne() is None:
                print "It found one that is not valid!", "I is :",i
                break
            self.b.show()
        self.b.show()

    def archive(self): self.bold = self.b
    def revert(self): self.b = self.bold

    """
    stack = []
    while not self.b.isComplete():
        self.currentB = self.getBoard()
        while self.currentB.isValid() and not self.currentB.isComplete():
            newBoard = self._iterate(self.currentB, self._solveOne)
            self.archive(newBoard) ## also mutates currentB
        if not self.currentB.isValid():
            self.popInvalid() ## Remove the invalid item from the list.
                              ##

    """


    def _getOne(self):
        if self.b.isComplete(): return (True,None,None,None)

        for i in xrange(self.b.getSize()):
            changeList = self.b.getDepthOf(i+1)
            if len(changeList) > 0:
                n,r,c = changeList[0]
                return (False, n,r,c)

        return (True,None,None,None)


    def _solveOne(self):
        self.archive()

        f,n,r,c = self._getOne()
        if f: return True

        if len(n) == 0: raise RuntimeError("Zero should have been caughe earlier")
        elif len(n) == 1:
            self.b.placeNode(n[0](),r,c)
            if self.b.isValid() and self.b.isComplete(): return True
            elif self.b.isValid(): return False
            else: return None
        elif len(n) > 1:
            print "Checking for a state that is greater than 1"
            for i in xrange(len(n)):
                self.revert()
                self.b.placeNode(n[i](),r,c)
                if self.b.isValid() and self.b.isComplete(): return True
                elif self.b.isValid(): return False
            return None
        else:
            raise RuntimeError("Not sure how we got here....")

























print "Starting"
s = board.Sudoku(9,board.makeSudokuBoard('Sudoku/Board00.txt'))
solver = SudokuCSP(s)
solver.solve()