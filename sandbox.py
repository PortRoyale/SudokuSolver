# this file is for test scripting relating to the sudoku solver file titled sudoku.py

import numpy as np
import sys
import time
import pygame


SUDOKU_INPUT = "000080000270000090065930020040000000007801200520000004002307060310000405750000000"



def initialize_grid(sudoku_input):
    all_ = [1,2,3,4,5,6,7,8,9]

    string_list = list(map(int, list(sudoku_input))) # convert input to a list of strings and then change all of those string numbers to ints
    arr_1d = np.array(string_list) # convert to numpy array
    sudoku = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

    solutions = np.zeros((9,9), dtype = object) # create an array of lists to assign possible solutions to later

    del(string_list, arr_1d) # delete what we don't need ( not sure if this is necessary, will Google it)

    # assign a label to the numbers that were present at the beginning of the puzzle aka GRID #'s
    for row_index, row in enumerate(sudoku):
        for column_index, num in enumerate(row):
            if num in all_: # find the numbers that are part of the initial grid
                solutions[row_index, column_index] = ["GRID #"]
            else:
                solutions[row_index, column_index] = []

    row_start = 0
    column_start = 0
    forward = True

    return sudoku, solutions, row_start, column_start, forward


def move(row_index, column_index, forward):
    # GOING FORWARD
    if forward == True: 
        if 0 <= column_index < 8: # increment column index before end of row
            column_index += 1
        elif column_index == 8: # increment row and restart column index
            column_index = 0 
            row_index += 1
        else:
            sys.exit("Within move(forward=True) function, something went wrong. DEBUG.")
        return row_index, column_index, forward
    # GOING BACKWARD
    elif forward == False:
        if column_index <= 0 and row_index <= 0:
            sys.exit("Went backwards to or past the 0th index. DEBUG.")
        elif 0 < column_index <= 8: # decrement column index before end of row
            column_index -= 1
        elif column_index == 0 and row_index != 0: # decrement row and restart column index
            column_index = 8 
            row_index -= 1
        else:
            sys.exit("Within move(forward=False) function, something went wrong. DEBUG.")
        return row_index, column_index, forward
    # SOMETHING ELSE
    else: 
         sys.exit("Wrong parameter, move(forward=???) function. DEBUG.")


def find_solutions(sudoku, row_index, column_index, solutions): # fxn to find possible sudoku solutions at the current location in the grid
    all_ = [1,2,3,4,5,6,7,8,9]
    
    horz_and_vert = np.append(sudoku[row_index,:], sudoku[:,column_index]) # combine horizontal and vertical elements into one list
    flattened_box = sudoku[row_index-row_index % 3:row_index-row_index % 3 + 3, column_index-column_index % 3:column_index-column_index % 3 + 3].flatten() # flatten the 3x3 local box    
    all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that can't be solutions to  current index
    sol = [n for n in all_ if n not in all_checks] # check for what possible numbers could be

    return sol


def backtracking(sudoku_grid, row_index, column_index, solutions):
    print("Solving...")
    print(sudoku_grid)

    solving = True

    forward = True

    sudoku = sudoku_grid

    start = time.time()

    while solving == True:

        # print(sudoku[0,:])
        # print(solutions[row_index, :])

        if row_index == 8 and column_index == 8: # SUCCESS
            sudoku[row_index, column_index] = find_solutions(sudoku, row_index = row_index, column_index = column_index, solutions = solutions)[0]
            print(sudoku)
            solving = False
        elif 0 <= row_index <= 8 and 0 <= column_index <= 8:
            sol = find_solutions(sudoku, row_index = row_index, column_index = column_index, solutions = solutions)
            
            if solutions[row_index, column_index] == ["GRID #"]: # encountered a GRID #, keep it moving, wherever you were going
                row_index, column_index, forward = move(row_index, column_index, forward)
            elif sol == []: # no solution, move backwards
                sudoku[row_index, column_index] = 0
                row_index, column_index, forward = move(row_index, column_index, forward = False) 
            elif forward == True: # not empty, need to try one and save the others
                sudoku[row_index, column_index] = sol[-1]
                sol.pop()
                solutions[row_index, column_index] = sol
                row_index, column_index, forward = move(row_index, column_index, forward = True)
            elif forward == False: # not empty, need to try one and save the others
                if solutions[row_index, column_index] == []: # solution set is empty, keep going backwards
                    sudoku[row_index, column_index] = 0
                    row_index, column_index, forward = move(row_index, column_index, forward = False)
                else: # there are still possible solutions to check. try one and go forward
                    sudoku[row_index, column_index] = solutions[row_index, column_index][-1]
                    solutions[row_index, column_index].pop()
                    row_index, column_index, forward = move(row_index, column_index, forward = True)
        else:
            sys.exit("BROKEN.")


    time_lapsed = time.time() - start
    print(time_lapsed, "seconds")
            


if __name__ == "__main__":
    
    s, sols, r_i, c_i, forward = initialize_grid(sudoku_input = SUDOKU_INPUT)
    
    backtracking(s, r_i, c_i, sols)