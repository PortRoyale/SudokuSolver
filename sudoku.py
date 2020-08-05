# Created by: Tyler Casper
# Start date: 7/27/2020
#
# Motivation: To create an implement an algorithm to solve a given sudoku problem. The solution must 
#   be shown to the user to verify it's correctness in a neat and consistent manner. 

import pygame
from pygame.locals import *
import os
import random
import math
import numpy as np
import sys
import time


# a list of 81 numbers separated by spaces. zeroes are blanks in the sudoku
SUDOKU_INPUT = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"




pygame.init() # initialize pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window


# CONSTANTS
WIN_WIDTH = 500
WIN_HEIGHT = 500
NUMBER_FONT = pygame.font.SysFont("Cascadia Code", 50)
X_OFFSET = 42
Y_OFFSET = 36

# COLORS 
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE =(53, 115, 255)
RED = (200,0,0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)



# input_string = input("Enter the string for the starting grid of the sudoku:")




# 9x9 GLOBAL matrix of pixel locations to the center of each square
global grid_locs
grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(9)] for y in range(9)] # these locations are pixel-based and were find via trial and error


clock = pygame.time.Clock()

pygame.display.set_caption("Sudoku Solver")


GRID_IMG = pygame.image.load(os.path.join("grid.png"))


class SudokuWindow:  # this is the sudoku grid of the window
    def __init__(self):
        self.WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.y = 0
        self.x = 0
        self.IMG = GRID_IMG
        self.grid = list(SUDOKU_INPUT) # splits the string into useable list format
        self.possible = ['1','2','3','4','5','6','7','8','9'] # the possible numbers of sudoku

    def draw_initial(self):
        self.WIN.blit(self.IMG, (self.x, self.y))

        for i, num in enumerate(self.grid):
            if num != "0":
                self.draw_number(num, i % 9, math.floor(i / 9), BLACK)

    def draw_number(self, number, i, j, color):
        num = NUMBER_FONT.render(str(number), 1, color)
        self.WIN.blit(num, grid_locs[j][i])
    

    # def draw_window(self): # in this function, we will place all CLASS.draw() fxns
        # sudoku.draw_initial(self.WIN)

        # draw_number(win, 5, 4, 4, GREEN)



class BacktrackingSolver:

    def __init__(self):
        self.grid = list(SUDOKU_INPUT) # splits the string into useable list format
        self.all_ = [1,2,3,4,5,6,7,8,9] # the possible    numbers of sudoku

    def initialize_grid(self):
        row_start = 0
        column_start = 0
        forward = True

        string_list = list(map(int, self.grid)) # convert input to a list of   strings and then change all of those string numbers to ints
        arr_1d = np.array(string_list) # convert to numpy array
        sudoku = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

        solutions = np.zeros((9,9), dtype = object) # create an array of lists to   assign possible solutions to later

        del(string_list, arr_1d) # delete what we don't need ( not sure if this is  necessary, will Google it)

        # assign a label to the numbers that were present at the beginning of the   puzzle aka GRID #'s
        for row_index, row in enumerate(sudoku):
            for column_index, num in enumerate(row):
                if num in self.all_: # find the numbers that are part of the initial grid
                    solutions[row_index, column_index] = ["GRID #"]
                else:
                    solutions[row_index, column_index] = []

        return sudoku, solutions, row_start, column_start, forward


    def move(self, row_index, column_index, forward):
        # GOING FORWARD
        if forward == True: 
            if 0 <= column_index < 8: # increment column index before end of row
                column_index += 1
            elif column_index == 8: # increment row and restart column index
                column_index = 0 
                row_index += 1
            else:
                sys.exit("Within move(forward=True) function, something went wrong.     DEBUG.")
            return row_index, column_index, forward
        # GOING BACKWARD
        elif forward == False:
            if column_index <= 0 and row_index <= 0:
                sys.exit("Went backwards to or past the 0th index. DEBUG.")
            elif 0 < column_index <= 8: # decrement column index before end of row
                column_index -= 1
            elif column_index == 0 and row_index != 0: # decrement row and restart  column index
                column_index = 8 
                row_index -= 1
            else:
                sys.exit("Within move(forward=False) function, something went wrong.    DEBUG.")
            return row_index, column_index, forward
        # SOMETHING ELSE
        else: 
             sys.exit("Wrong parameter, move(forward=???) function. DEBUG.")


    def find_solutions(self, sudoku, row_index, column_index, solutions): # fxn to find   possible sudoku solutions at the current location in the grid

        horz_and_vert = np.append(sudoku[row_index,:], sudoku[:,column_index]) #    combine horizontal and vertical elements into one list
        flattened_box = sudoku[row_index-row_index % 3:row_index-row_index % 3 + 3,     column_index-column_index % 3:column_index-column_index % 3 + 3].flatten() #    flatten the 3x3 local box    
        all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that  can't be solutions to  current index
        sol = [n for n in self.all_ if n not in all_checks] # check for what possible    numbers could be

        return sol


    def backtracking(self):
        sudoku, solutions, row_index, column_index, forward = self.initialize_grid()

        print("Solving...")
        print(sudoku)

        start = time.time()


        solving = True
        while solving == True:

            # print(sudoku[0,:])
            # print(solutions[row_index, :])

            if row_index == 8 and column_index == 8: # SUCCESS
                sudoku[row_index, column_index] = self.find_solutions(sudoku, row_index =    row_index, column_index = column_index, solutions = solutions)[0]
                print(sudoku)
                solving = False
            elif 0 <= row_index <= 8 and 0 <= column_index <= 8:
                sol = self.find_solutions(sudoku, row_index = row_index, column_index =  column_index, solutions = solutions)

                if solutions[row_index, column_index] == ["GRID #"]: # encountered a    GRID #, keep it moving, wherever you were going
                    row_index, column_index, forward = self.move(row_index, column_index,    forward)
                elif sol == []: # no solution, move backwards
                    sudoku[row_index, column_index] = 0
                    row_index, column_index, forward = self.move(row_index, column_index,    forward = False) 
                elif forward == True: # not empty, need to try one and save the others
                    sudoku[row_index, column_index] = sol[-1]
                    sol.pop()
                    solutions[row_index, column_index] = sol
                    row_index, column_index, forward = self.move(row_index, column_index,    forward = True)
                elif forward == False: # not empty, need to try one and save the others
                    if solutions[row_index, column_index] == []: # solution set is  empty, keep going backwards
                        sudoku[row_index, column_index] = 0
                        row_index, column_index, forward = self.move(row_index,  column_index, forward = False)
                    else: # there are still possible solutions to check. try one and go     forward
                        sudoku[row_index, column_index] = solutions[row_index,  column_index][-1]
                        solutions[row_index, column_index].pop()
                        row_index, column_index, forward = self.move(row_index,  column_index, forward = True)
            else:
                sys.exit("BROKEN.")


        time_lapsed = time.time() - start
        print(time_lapsed, "seconds")
            








if __name__ == "__main__":
    SUDOKUWIN = SudokuWindow()
    SUDOKUWIN.draw_initial()

    pygame.display.update()


    BACKTRACK = BacktrackingSolver() # init
    BACKTRACK.backtracking()



    # PUT SOLVING/DRAWING ALGORITHM HERE #


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
