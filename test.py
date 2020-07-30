# this file is for test scripting relating to the sudoku solver file titled sudoku.py

from numpy import matrix
from numpy import linalg
from math import floor
import numpy as np


X_OFFSET = 42
Y_OFFSET = 36


w, h = 9, 9;
global grid_locs 
grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(w)] for y in range(h)] # 9 x 9 matrix of zeros





SUDOKU_INPUT = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"

input_ = list(SUDOKU_INPUT)

string_list = list(map(int, input_)) # change all numbers from strings to ints

arr_1d = np.array(string_list) # convert to numpy array

s = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

print(s)

all_ = [1,2,3,4,5,6,7,8,9]

sols = np.zeros((9,9), dtype = list) # create an array of lists to assign possible solutions to later


for r_i, row in enumerate(s):
    for c_i, num in enumerate(row):
        print(r_i, c_i, row, num)
    
        row_start = r_i * 9 # the index of the beginning of the row that the i index is in



        if num == 0: # we need to implement an algorithm to fill in numbers, here
            horz_and_vert = np.append(row, s[:,c_i]) # combine horizontal and vertical elements into one list
            flattened_box = s[r_i-r_i%3:r_i-r_i%3+3, c_i-c_i%3:c_i-c_i-c_i%3+3].flatten() # flatten the 3x3 local box
            all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that can't be solutions to current index

            sols[r_i, c_i] = [n for n in all_ if n not in all_checks] # assign list of possible solutions to an array of lists

            for num in sols[r_i, c_i]:
                if len(sols[r_i, c_i]) == 1: # this is the only solution 
                    s[r_i, c_i] = sols[r_i, c_i] # assign new value to the sudoku grid solution
                    sols[r_i, c_i] = [] # replace sols entry with empty list
                    # UPDATE UI/UX HERE
                else: # there is more than one solution...hmmm
                    
                    print(num, len(sols[r_i,c_i]))
       
            # if len(maybe[-1]) == 1: # this must be the correct answer if only one choice
            #     s[i] = maybe[-1][0] # assign the only possible answer to the square
            #     # maybe[-1].pop() # delete that because we know it has to be true
            #     print("len == 1:", i, s, maybe)
            #     pass
            # else:
            #     for m, n in enumerate(maybe): # we must keep these maybe's around incase we backtrack
            #         print(maybe, i, m, n)
            #         s[i] = maybe[-1][m]



# # # print(s, "\n", s[0:9], "\n", s[0::9])
