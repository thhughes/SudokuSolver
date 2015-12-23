__author__ = 'troyhughes'
from Node import Node

class Sudoku:
    def __init__(self, size, populatedBoard):
        self._size = size
        self._b = [[]]
        self._setBoard(populatedBoard)



    def __call__(self): return self._b
    def __str__(self):  return self._print()
    def __repr__(self): return self._print()


    def _setBoard(self, someBoard):
        self._b = [[]]
        if self._size != len(someBoard) and self._size != len(someBoard[0]):
            raise SudokuException("Board provided does not match set board size")



    def _print(self):
        for row in self._b:
            print row





class SudokuException(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)



def boardMaker(fileName):
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


print "Starting"
boardMaker('Board00.txt')