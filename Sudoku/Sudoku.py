from Node import *
import csv

class Sudoku():
    def __init__(self, file_name):
        self._board = []
        f = open("test_board.txt","r")
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
                    



a = Sudoku("test_board.txt")
