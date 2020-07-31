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





SUDOKU_INPUT = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"

input_ = list(SUDOKU_INPUT)

string_list = list(map(int, input_)) # change all numbers from strings to ints

arr_1d = np.array(string_list) # convert to numpy array

s = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

ref = s

del(input_, string_list, arr_1d)

print(s)

all_ = [1,2,3,4,5,6,7,8,9]

sols = np.zeros((9,9), dtype = list) # create an array of lists to assign possible solutions to later


for r_i, row in enumerate(s):
    for c_i, n in enumerate(row):

        while True:
            num = s[r_i, c_i]
            
            print(r_i, c_i, num)

            horz_and_vert = np.append(s[r_i,:], s[:,c_i]) # combine horizontal and vertical elements into one list
            flattened_box = s[r_i-r_i % 3:r_i-r_i % 3 + 3, c_i-c_i % 3:c_i-c_i % 3 + 3].flatten() # flatten the 3x3 local     box
            all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that can't be solutions to    current index
            sols[r_i, c_i] = [n for n in all_ if n not in all_checks] # assign list of possible solutions to an     array of lists

            if num == 0 and len(sols[r_i, c_i]) == 0:
                print("BACKTRACKING from r_i: ", r_i, " c_i: ", c_i)

                if 0 < c_i <= 8: # decrement column index before end of row
                    c_i -= 1
                elif c_i == 0: # decrement row and restart column index
                    c_i = 8 
                    r_i -= 1
                elif c_i == 0 and r_i == 0:
                    sys.exit("Went backwards to zero. Uh oh!!!")
                else:
                    sys.exit("Don't know how this happened. DEBUG.")

                break

            elif num == 0:
                for num in sols[r_i, c_i]:
                    if len(sols[r_i, c_i]) == 1: # this is the only solution 
                        s[r_i, c_i] = sols[r_i, c_i][0] # assign new value to the sudoku grid solution
                        sols[r_i, c_i] = [] # replace sols entry with empty list
                        # UPDATE UI/UX HERE
                    else: # there is more than one solution...hmmm
                        for sol in sols[r_i, c_i]: # iterate through list of solutions
                            # print(sols)
                            s[r_i, c_i] = sols[r_i, c_i][-1]
                            sols[r_i, c_i].pop()
                            # print("popped:", sols[r_i, c_i])
            else:
                pass
            

            if 0 <= c_i < 8: # increment column index before end of row
                c_i += 1
            elif c_i == 8: # increment row and restart column index
                c_i = 0 
                r_i += 1
            elif c_i == 8 and r_i == 8:
                    print(s)
                    sys.exit("FOUND A SOLUTION!!!!")
            else:
                sys.exit("Don't know how this happened. DEBUG.")