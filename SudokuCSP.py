__author__ = 'troyhughes'
from Sudoku import board
from Sudoku.board import SudokuException

class SudokuCSP:
    def __init__(self, board):
        self.b = board



    def solve(self):
        self.b.show()
        self._removeOnes()
        self.b.show()





    def _removeOnes(self):
        while self.b.getCountOfDepth(1) > 0:
            board = self.b.getBoard()
            changeList = self.b.getDepthOf(1)
            # print "Remove ones list: ", len(changeList)
            for i in changeList:
                n,r,c = i
                self.b.placeNode(n(),r,c)





























print "Starting"
s = board.Sudoku(9,board.makeSudokuBoard('Sudoku/Board00.txt'))
solver = SudokuCSP(s)
solver.solve()