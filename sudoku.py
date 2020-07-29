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


# a list of 81 numbers separated by spaces. zeroes are blanks in the sudoku
SUDOKU_START = "040509108710004500030007940965070231070000080103960000000050700300006000650801300"


# 9x9 GLOBAL matrix of pixel locations to the center of each square
global grid_locs
w = 9
h = 9
grid_locs = [[(x*50 + X_OFFSET, y*50 + Y_OFFSET) for x in range(w)] for y in range(h)] 

print(grid_locs[0][0])


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("Sudoku Solver")


GRID_IMG = pygame.image.load(os.path.join("grid.png"))


class Sudoku:  # this is the sudoku grid of the window
    IMG = GRID_IMG

    def __init__(self):
        self.y = 0
        self.x = 0
        self.start = list(SUDOKU_START) # splits the string into useable list format
        self.possible = ['1','2','3','4','5','6','7','8','9'] # the possible numbers of sudoku

    def draw_initial(self, win):
        win.blit(self.IMG, (self.x, self.y))

        for i, num in enumerate(self.start):
            if num != "0":
                draw_number(win, num, i % 9, math.floor(i / 9), BLACK)


    def solver(self):
        s = self.start # save the initial sudoku value for backtracking
        s2 = self.start

        # for i, num in enumerate(s):
        #     if num == "0": # we need to implement an algorithm to fill in numbers, here
        #         filter(lambda x: x not in Z, item)


def draw_number(win, number, i, j, color):
    num = NUMBER_FONT.render(str(number), 1, color)
    win.blit(num, grid_locs[j][i])
    

def draw_window(win, sudoku): # in this function, we will place all CLASS.draw() fxns
    sudoku.draw_initial(win)
    sudoku.solver()

    # draw_number(win, 5, 4, 4, GREEN)



if __name__ == "__main__":
    SUDOKU = Sudoku()

    draw_window(WIN, SUDOKU)

    pygame.display.update()


    # PUT SOLVING/DRAWING ALGORITHM HERE #


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
