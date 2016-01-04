# SudokuSolver

This is a Sudoku Solver utilizing Constraint Satisfaction. The constraints used are listed below
and the method of 'heuristic' search is doccumented as well.


The program uses the following constraints:
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