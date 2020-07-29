# this file is for test scripting relating to the sudoku solver file titled sudoku.py

from numpy import matrix
from numpy import linalg


X_OFFSET = 42
Y_OFFSET = 36


w, h = 9, 9;
global grid_locs 
grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(w)] for y in range(h)] # 9 x 9 matrix of zeros


print(grid_locs[0][0])


SUDOKU_START = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"
start = list(SUDOKU_START)

print(start, "/n", start[0:9])