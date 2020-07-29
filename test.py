# this file is for test scripting relating to the sudoku solver file titled sudoku.py

from numpy import matrix
from numpy import linalg
from math import floor


X_OFFSET = 42
Y_OFFSET = 36


w, h = 9, 9;
global grid_locs 
grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(w)] for y in range(h)] # 9 x 9 matrix of zeros


# print(grid_locs[0][0])


SUDOKU_INPUT = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"
s = list(SUDOKU_INPUT)

print(s)

all_ = ['1','2','3','4','5','6','7','8','9']


for i, num in enumerate(s):
    if num == "0": # we need to implement an algorithm to fill in numbers, here
        k = floor(i / 9) * 9 # the index of the beginning of the row that the i index is in
        verts = [z for z in s[i::9] if z not in s[k:k+9]] # the set of numbers vertically that are not in the horizontal subspace
        maybe = [z for z in all_ if z not in (verts + s[k:k+9])] # the subspace of numbers that can be possible solutions
        print(i, k, verts, maybe)

        # if len(maybe) == 1:
        #     s[i] = maybe
        #     print(i, s)
        #     break
        # else:
        #     for l, num in enumerate(maybe):
        #         s[i] = maybe[l]



print(s, "\n", s[0:9], "\n", s[0::9])
