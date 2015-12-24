from sudoku.Sudoku import Sudoku ## from folder.file import class


def remove_ones(board):
        depth_d = board.depth_dict()
        tmpB = None
        illegal = False 
        while (1 in depth_d):
            px,py = depth_d[1][0]
            vxy = board[py][px].get_possible()[0] ## Only 1 in list, always 0
            tmpB, legal = board.place_node(vxy[0],px,py)
            if legal:board = tmpB
            else: raise RuntimeError("Illegal move allowed")
            depth_d = board.depth_dict()
        return board

    
def try_val(point,board):
    x,y = point
    print "The point observed is",x,y
    possible_list,error_bool = board[y][x].get_possible()
    if error_bool:
        raise RuntimeError("Got a True back in TryVal")
    if not error_bool and len(possible_list) == 0:
        
        return False,None
    print "Posible List",possible_list
    for pos in possible_list:
        print "Board Value",board[y][x]
        new_board = Sudoku(board,pos,x,y)
        done_b,answer = solve_csp(new_board)
        if done_b is True: return True,answer
        else:continue
    return False,None


def solve_csp(board):
    removed_ones = remove_ones(board)
    if removed_ones.is_solved(): return True, removed_ones
    else:
        depth = removed_ones.depth_dict()
        dkeys = sorted(depth.keys())
        if 0 in dkeys:
            return False,None
        dkeys.reverse()
        for key in dkeys:
            done_b,answer = try_val(depth[key][0],removed_ones)
            if done_b: return True,answer
            else: continue
        return False,None
            


def CSP(file_name):
    starting_board = Sudoku(None)
    starting_board.make_board(file_name)
    print starting_board
    
    removed_ones = remove_ones(starting_board)
    if removed_ones.is_solved(): return True, removed_ones
    else:
        done_bool,answer = solve_csp(removed_ones)
        if not done_bool: raise RuntimeError("Did not finish")
        print answer





solver = CSP("sudoku/Board00.txt")
##solver.solve()

