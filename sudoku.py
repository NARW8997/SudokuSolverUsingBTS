#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"
sub_group_row = {'A':['A','B','C'], 'B': ['A','B','C'], 'C': ['A','B','C'], 'D':['D','E','F'],
                 'E':['D','E','F'], 'F':['D','E','F'], 'G':['G','H','I'], 'H':['G','H','I'], 'I':['G','H','I']}

sub_group_col = {1:[1,2,3], 2: [1,2,3], 3:[1,2,3], 4:[4,5,6], 5:[4,5,6], 6:[4,5,6], 7:[7,8,9],
                 8:[7,8,9], 9:[7,8,9]}

unique_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def is_assignment_complete(board) -> bool:
    for key in board:
        if board[key] == 0:
            return False
    return True


def select_unassigned_variables(board) -> list:
    """
    :param board: board in hash format
    :return: return all unfileld box keys from board
    """
    res = []
    for key in board:
        if board[key] == 0:
            res.append(key)

    return res

def get_legal_domain(var, board) -> list:
    if board[var] != 0:
        RuntimeError("get domain by already filled square")

    res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = var[0] # 'A', 'B', 'C', 'D'
    col = var[1] # 1, 2, 3, 4
    # remove illegal num in whole row
    # from 1 ~ 9
    for i in range(1, 10):
        col_num = board[row + str(i)]
        if col_num in res:
            res.remove(col_num)

    # remove illegal num in whole col
    # from A ~ I
    for i in map(chr, range(65, 74)):
        row_chr = i + str(col)
        if board[row_chr] in res:
            res.remove(board[row_chr])

    # remove illegal num in each block
    row_range = sub_group_row[row]
    col_range = sub_group_col[int(col)]
    for i in row_range:
        for j in col_range:
            key = i + str(j)
            if board[key] in res:
                res.remove(board[key])

    return res


def select_MRV_from_unassigned_val_sorted(board):
    """
    :param board: sudoku baord
    :return: return all the unfiled box keys with possiable values
    ['A1', 'A2', 'A3'] ->
    {'A1':[2,3,4], 'A2':[4,1], 'A3': [8]} ->
    [('A3', [8]), ('A2', [4, 1]), ('A1', [2, 3, 4])]

    ordered_d_1 = dict(sorted(d.items(), key=lambda i: len(i[1])))
    """
    vars_unassigned = select_unassigned_variables(board)
    unordered_dict = {}
    for var in vars_unassigned:
        unordered_dict[var] = get_legal_domain(var, board)

    ordered_dict = dict(sorted(unordered_dict.items(), key=lambda i: len(i[1])))

    return ordered_dict


def check_consistent(var, value, board) -> bool:
    return check_cols_consistent(var, value, board) and\
           check_rows_consistent(var, value, board) and\
           check_blocks_consistent(var, value, board)

def check_rows_consistent(var, value, board):
    row = var[0]
    for i in range(1, 10):
        if value == board[row + str(i)]:
            return False
    return True

def check_cols_consistent(var, value, board):
    col = var[1]
    for i in map(chr, range(65, 74)):
        if value == board[i + str(col)]:
            return False
    return True

def check_blocks_consistent(var, value, board):
    row_range = sub_group_row[var[0]]
    col_range = sub_group_col[int(var[1])]
    for i in row_range:
        for j in col_range:
            if value == board[i + str(j)]:
                return False
    return True

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    if is_assignment_complete(board):
        return board

    # slect all unfilled vars
    ordered_dict = select_MRV_from_unassigned_val_sorted(board)
    var = next(iter(ordered_dict))
    values = ordered_dict[var]
    for value in values:
        if check_consistent(var, value, board):
            board[var] = value
            result = backtracking(board)
            if result != False: return result
            board[var] = 0
    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)
        print(solved_board)
        # print(time.time() - begin_time)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py
        # time_list = []
        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)
            begin_time = time.time()
            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)
            # time_list.append(time.time() - begin_time)
            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
        
        print("Finishing all boards in file.")