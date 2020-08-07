# Created by: Tyler Casper
# Start date: 7/27/2020
#
# Motivation: To create an implement an algorithm to solve a given sudoku problem. The solution must 
#   be shown to the user to verify it's correctness in a neat and consistent manner. 
# Methods: I have implemented a backtracking algorithm to solve a given Sudoku. I am not sure if this is the exact backtracking algorithm,
#   because I thought it through and implemented myself, but it seems to work for any given Sudoku.

import pygame
from pygame.locals import *
import os
import math
import numpy as np
import sys
import time
from time import sleep



# a list of 81 numbers separated by spaces. zeroes are blanks in the sudoku
SUDOKU_INPUT = "900704002060000910087000054008000790600009003000270000706900820040000106020005000"






class SudokuSolver():

    def __init__(self):
        # PYGAME
        pygame.init()

        self.NUMBER_FONT = pygame.font.SysFont("Cascadia Code", 60) # set desired font characteristics in pygame
        self.WIN_WIDTH = 640
        self.WIN_HEIGHT = 640 

        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT)) # set the desired pixel width and height in pygame
        self.GRID_IMG = pygame.image.load(os.path.join("gridDL.png")) # load the grid image I made in microsoft paint
        self.BLANK_IMG = pygame.image.load(os.path.join("blank.png")) # load the blank image I made in microsoft paint
        self.ICON_IMG = pygame.image.load(os.path.join("icon.png"))
        pygame.display.set_icon(self.ICON_IMG)
        pygame.display.set_caption("Sudoku Solver") # label the pygame window
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen
        self.clock = pygame.time.Clock() # initialize a clock instance in pygame

        # COLORS 
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.BLUE =(53, 115, 255)
        self.RED = (200,0,0)
        self.GREEN = (0, 200, 0)

        self.y = 20 # Y direction offset of grid in window
        self.x = 20 # X direction offset of grid in window
        self.X_OFFSET = 41 # X offset of numbers in window
        self.Y_OFFSET = 38 # y offset of numbers in window
        self.grid_locs = [[(x*67 + self.X_OFFSET, y*67 + self.Y_OFFSET) for x in range(9)] for y in range(9)] # 9x9 matrix of (x,y) locations to print the numbers on the grid

        # SUDOKU
        self.grid = list(SUDOKU_INPUT) # splits the string into useable list format
        self.all_ = [1,2,3,4,5,6,7,8,9] # the possible    numbers of sudoku

        self.draw_grid()



    def draw_number(self, number, row_index, column_index, color):
        num = self.NUMBER_FONT.render(str(number), 1, color)
        self.draw_blank(row_index, column_index)
        self.WIN.blit(num, self.grid_locs[row_index][column_index])
        pygame.display.update()
        # self.clock.tick(2) # used to control FPS of program


    def draw_blank(self, row_index, column_index):
        self.WIN.blit(self.BLANK_IMG, self.grid_locs[row_index][column_index])
        pygame.display.update()


    def draw_grid(self):
        self.WIN.fill(self.BLUE)
        self.WIN.blit(self.GRID_IMG, (self.x, self.y))

        for i, num in enumerate(self.grid):
            if num != "0":
                self.draw_number(num, math.floor(i / 9), i % 9, self.BLACK)

                self.if_you_want_to_quit()


    def success(self, sudoku, solutions):
        self.draw_grid()

        for row_index, row in enumerate(sudoku):
            for column_index, num in enumerate(row):
                if solutions[row_index, column_index] != ["GRID #"]:
                    self.draw_number(sudoku[row_index, column_index], row_index, column_index, self.GREEN)


    def if_you_want_to_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

       
    def load_grid(self):
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
        sudoku, solutions, row_index, column_index, forward = self.load_grid()

        print("Solving...")
        print(sudoku)

        solving = True
        start = time.time()


        while solving:

            self.if_you_want_to_quit()


            if row_index == 8 and column_index == 8: # SUCCESS
                if solutions[row_index, column_index] == ["GRID #"]: # encountered a    GRID #, keep it moving, wherever you were going
                    self.success(sudoku, solutions)
                    solving = False
                else:
                    sudoku[row_index, column_index] = self.find_solutions(sudoku, row_index = row_index, column_index = column_index, solutions = solutions)[0]
                    ### DRAW sudoku[row_index, column_index]
                    self.draw_number(sudoku[row_index, column_index], row_index, column_index, self.RED)
                    self.success(sudoku, solutions)
                    solving = False
            elif 0 <= row_index <= 8 and 0 <= column_index <= 8:
                sol = self.find_solutions(sudoku, row_index = row_index, column_index =  column_index, solutions = solutions)

                if solutions[row_index, column_index] == ["GRID #"]: # encountered a    GRID #, keep it moving, wherever you were going
                    row_index, column_index, forward = self.move(row_index, column_index, forward)
                elif sol == []: # no solution, move backwards
                    sudoku[row_index, column_index] = 0
                    ### DRAW BLANK SPACE
                    self.draw_blank(row_index, column_index)
                    row_index, column_index, forward = self.move(row_index, column_index, forward = False) 
                elif forward == True: # not empty, need to try one and save the others
                    sudoku[row_index, column_index] = sol[-1]
                    ### DRAW sudoku[row_index, column_index]
                    self.draw_number(sudoku[row_index, column_index], row_index, column_index, self.RED)
                    sol.pop()
                    solutions[row_index, column_index] = sol
                    row_index, column_index, forward = self.move(row_index, column_index, forward = True)
                elif forward == False: # not empty, need to try one and save the others
                    if solutions[row_index, column_index] == []: # solution set is  empty, keep going backwards
                        sudoku[row_index, column_index] = 0
                        ### DRAW BLANK SPACE
                        self.draw_blank(row_index, column_index)
                        row_index, column_index, forward = self.move(row_index,  column_index, forward = False)
                    else: # there are still possible solutions to check. try one and go     forward
                        sudoku[row_index, column_index] = solutions[row_index,  column_index][-1]
                        #### DRAW sudoku[row_index, column_index]
                        self.draw_number(sudoku[row_index, column_index], row_index, column_index, self.RED)
                        solutions[row_index, column_index].pop()
                        row_index, column_index, forward = self.move(row_index,  column_index, forward = True)
            else:
                sys.exit("BROKEN.")


                    
        time_lapsed = time.time() - start

        print("\n","Solved in", time_lapsed, "seconds.", "\n", sudoku)

        
        while True:
            self.if_you_want_to_quit()

            


if __name__ == "__main__":

    SUDOKU = SudokuSolver()
    SUDOKU.backtracking()
