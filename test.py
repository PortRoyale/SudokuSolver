# this file is for test scripting relating to the sudoku solver file titled sudoku.py

from numpy import matrix
from numpy import linalg
from math import floor
import numpy as np
import sys


# X_OFFSET = 42
# Y_OFFSET = 36


# global grid_locs 
# grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(9)] for y in range(9)] # 9 x 9 matrix of zeros





SUDOKU_INPUT = "000607095809000207006009300600020409100000020000006000010000940000830000002900150"

input_ = list(SUDOKU_INPUT)

string_list = list(map(int, input_)) # change all numbers from strings to ints

arr_1d = np.array(string_list) # convert to numpy array

s = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

ref = s

del(input_, string_list, arr_1d)

# print(s)

all_ = [1,2,3,4,5,6,7,8,9]

sols = np.zeros((9,9), dtype = object) # create an array of lists to assign possible solutions to later


def move(row_index, column_index, forward):
    # GOING FORWARD
    if forward == True: 
        if column_index == 8 and row_index == 8:
            pass # SUCCESS, I think
        elif 0 <= column_index < 8: # increment column index before end of row
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

# Initialize Variables
r_i = 0
c_i = 0
back_trigger = False


def find_solutions(sudoku, row_index, column_index):
    pass



while True:
    num = s[r_i, c_i]
    
    print(r_i, c_i, num)
    print(s)


    horz_and_vert = np.append(s[r_i,:], s[:,c_i]) # combine horizontal and vertical elements into one list
    flattened_box = s[r_i-r_i % 3:r_i-r_i % 3 + 3, c_i-c_i % 3:c_i-c_i % 3 + 3].flatten() # flatten the 3x3 local box    
    all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that can't be solutions to  current index


    if back_trigger == False and (sols[r_i, c_i] == ["GRID #"] or sols[r_i, c_i] == ["FILLED"]): # skip forward over numbers already filled
        pass
    elif back_trigger == True and sols[r_i, c_i] == ["GRID #"]: # skip backwards over filled numbers
        r_i, c_i, back_trigger = backtrack(r_i, c_i)
    elif back_trigger == True and sols[r_i, c_i] == ["FILLED"]: # go back but remove number from location
        s[r_i, c_i] = 0
        sols[r_i, c_i] = 0
        r_i, c_i, back_trigger = backtrack(r_i, c_i)
    elif back_trigger == True and type(sols[r_i, c_i]) == list and len(sols[r_i,c_i]) > 0: # go back but remove number from location
            for num in sols[r_i, c_i]:
                if len(sols[r_i, c_i]) == 1: # this is the only solution 
                    s[r_i, c_i] = sols[r_i, c_i][0] # assign new value to the sudoku grid solution
                    sols[r_i, c_i] = ["FILLED"]
                    # UPDATE UI/UX HERE
                else: # there is more than one solution...hmmm
                    for sol in sols[r_i, c_i]: # iterate through list of solutions
                        s[r_i, c_i] = sols[r_i, c_i][-1]
                        sols[r_i, c_i].pop()
                        break
    elif num != 0 and sols[r_i, c_i] == 0: # find the numbers that are part of the initial grid
        sols[r_i, c_i] = ["GRID #"]
    elif r_i == 8 and c_i == 8:
        print("SOLUTION FOUND:")
        sols[r_i, c_i] = [n for n in all_ if n not in all_checks]
        s[r_i, c_i] = sols[r_i, c_i][0]
        print(s)
        sys.exit()
    else: # there are solutions to be found or applied
        sols[r_i, c_i] = [n for n in all_ if n not in all_checks] # assign list of possible solutions to a numpy 9x9 array of lists
        # print(sols[r_i, c_i])

        if num == 0 and len(sols[r_i, c_i]) == 0: # BACKTRACK: no possible solutions found so correct solution must be behind us
                r_i, c_i, back_trigger = backtrack(r_i, c_i)
        elif num == 0 or (num != 0 and len(sols[r_i, c_i]) > 0):  # 1) have't gotten here yet or 2)we have backtracked to get here and need to apply a new
            for num in sols[r_i, c_i]:
                if len(sols[r_i, c_i]) == 1: # this is the only solution 
                    s[r_i, c_i] = sols[r_i, c_i][0] # assign new value to the sudoku grid solution
                    sols[r_i, c_i] = ["FILLED"]
                    # UPDATE UI/UX HERE
                else: # there is more than one solution...hmmm
                    for sol in sols[r_i, c_i]: # iterate through list of solutions
                        s[r_i, c_i] = sols[r_i, c_i][-1]
                        sols[r_i, c_i].pop()
                        break
                    break
                break
            back_trigger = False
        else:
            pass


    r_i, c_i, back_trigger = go_forward(r_i, c_i, back_trigger)