# Created by: Tyler Casper
# Start date: 7/27/2020
#
# Motivation: To create an implement an algorithm to solve a given sudoku problem. The solution must 
#   be shown to the user to verify it's correctness in a neat and consistent manner. 


import pygame
from pygame.locals import *
import os
import random
import numpy as np


pygame.init() # initialize pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window


# CONSTANTS
WIN_WIDTH = 500
WIN_HEIGHT = 500
NUM_FONT = pygame.font.SysFont("Cascadia Code", 50)
# Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE =(53, 115, 255)
RED = (200,0,0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
X_OFFSET = 42
Y_OFFSET = 36


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


class Grid:  # this is the sudoku grid of the window
    IMG = GRID_IMG

    def __init__(self):
        self.y = 0
        self.x = 0
        self.locs = [] # this is a 9x9 matrix of grid square center points

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


def draw_num(win, num, i, j, color):
    number = NUM_FONT.render(str(num), 1, color)
    win.blit(number, grid_locs[i][j])
    



def draw_window(win, grid): # in this function, we will place all CLASS.draw() fxns
    grid.draw(win)

    draw_num(win, 5, 4, 4, GREEN)

    # x = 50
    # y = 50
    # loc = (42, 36)
    # number = NUM_FONT.render(str(9), 1, RED)
    # win.blit(number, loc)

    pygame.display.update()


if __name__ == "__main__":
    GRID = Grid()

    draw_window(WIN, GRID)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
