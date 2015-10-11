from sudoku.Sudoku import Sudoku ## from folder.file import class


a = Sudoku(None)
a.make_board("sudoku/Board00.txt")
print a
a.p_depth()
b = a.depth_dict()
for i in b:
    print i,b[i]
