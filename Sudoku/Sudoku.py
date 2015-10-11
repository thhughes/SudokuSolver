from Node import *
import csv

class Sudoku():
    def __init__(self, board=None):
        if board is None:
            self._board = []
        else:
            if len(board) == 9:
                for row in board:
                    if len(row) != 9: raise RuntimeError("Improper size board passed to Sudoku class")
                    for item in row:
                        val = item.value()
                        if val is None: continue
                        if type(val) is not int: raise RuntimeError("Improper Node value on board")
                        if val < 0 or val > 9: raise RuntimeError("Value out of bounds for Nodes")                        
            self._board = board
            self._populate()
                


    def make_board(self,file_name):
        f = open(file_name,"r")
        file_content = f.read()
        file_content = file_content.split('\n')
        raw_board = []
        for row in file_content:
            raw_board.append(row.split(','))

        for row in raw_board:
            soduku_row = []
            for square in row:
                if square is ' ':
                    soduku_row.append(Node(None))
                else:
                    soduku_row.append(Node(int(square)))
            self._board.append(soduku_row)
            soduku_row = []
        self._populate()

    def _populate(self):
        for y,row in enumerate(self._board):
            for x,item in enumerate(row):
                item.set_p(self._get_possible(x,y))
        
        self._depth = []
        for y,row in enumerate(self._board):
            tmp = []
            for x,item in enumerate(row):
                tmp.append(len(item.get_possible()))
            self._depth.append(tmp)
                
                
    
    def __str__(self):
        ##print self._board
        print "-"*9*2 + "------"
        for j,row in enumerate(self._board):
            if j == 3 or j == 6:
                print "-"*9*2 + "------"
            ##print "String command" + row[0].string()
            s = "||"
            for i,item in enumerate(row):
                if i == 3 or i == 6:
                    s = s+"|"
                
                s = s+item.string()+" "
            s = s+"||"
            print s
        print "-"*9*2 + "----"
        return " "
                    


    def _get_row(self,which_row):
        if which_row > 8 or which_row < 0:
            raise RuntimeError("Error checking Row: Row out of bounds")
        tmprow = self._board[which_row]
        row = []
        for item in tmprow:
            if item.val() is not None:
                row.append(item)
        return row

    def _get_column(self, which_column):
        if which_column > 8 or which_column < 0:
            raise RuntimeError("Error checking column: column out of bounds")
        column = []
        for row in self._board:
            if row[which_column] is not None:
                column.append(row[which_column])
        return column

    def _get_cube(self, which_cube):
        if which_cube > 8 or which_cube < 0:
            raise RuntimeError("Error checking cube: cube out of bounds")
        cube_dict = {0:(0,0,2,2),
                     1:(0,3,2,5),
                     2:(0,6,2,8),
                     3:(3,0,5,2),
                     4:(3,3,5,5),
                     5:(3,6,5,8),
                     6:(6,0,8,2),
                     7:(6,3,8,5),
                     8:(6,6,8,8)}
        ys,xs,ye,xe = cube_dict[which_cube]
        cube = []
        for i,row in enumerate(self._board):
            if i >=ys and i <=ye:                
                for j,item in enumerate(row):
                    if j >= xs and j <= xe:
                        cube.append(item)
        return cube

    def _xyToCube(self,x,y):
        if x > 8 or y > 8 or y < 0 or x < 0:
            raise RuntimeError("xyToCube out of bounds 0 < x < 8; 0 < y< 8")
        if y >= 0 and x >= 0 and y <= 2 and x <= 2: return 0
        elif y >= 0 and x >= 3 and y <= 2 and x <= 5: return 1
        elif y >= 0 and x >= 6 and y <= 2 and x <= 8: return 2
        elif y >= 3 and x >= 0 and y <= 5 and x <= 2: return 3
        elif y >= 3 and x >= 3 and y <= 5 and x <= 5: return 4
        elif y >= 3 and x >= 6 and y <= 5 and x <= 8: return 5
        elif y >= 6 and x >= 0 and y <= 8 and x <= 2: return 6
        elif y >= 6 and x >= 3 and y <= 8 and x <= 5: return 7
        elif y >= 6 and x >= 6 and y <= 8 and x <= 8: return 8
        else: raise RuntimeError("xyToCube: Unspecific Error")
        
        
        


    def _check_valid(self,value,x,y):
        cube = self._xyToCube(x,y)
        if value in self._get_row(y): return False
        elif value in self._get_column(x): return False
        elif value in self._get_cube(cube): return False
        else: return True

    def _get_possible(self,x,y):
        cube = self._xyToCube(x,y)
        npos = []
        npos.extend(self._get_row(y))
        npos.extend(self._get_column(x))
        npos.extend(self._get_cube(cube))

        pos = [1,2,3,4,5,6,7,8,9,"_"]
        for num in set(npos):
            if num in pos:
                pos.remove(num)
        pos.remove("_")
        return pos
                    
        
            
                
                    
            
    
        
a = Sudoku()
a.make_board("Board00.txt")
