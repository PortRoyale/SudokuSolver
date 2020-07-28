import pygame
from pygame.locals import *
import neat
import time
import os
import random

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window


WIN_WIDTH = 500
WIN_HEIGHT = 500
NUM_FONT = pygame.font.SysFont("Cascadia Code", 50)
# END_FONT = pygame.font.SysFont("Cascadia Code", 70)


# Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE =(53, 115, 255)
RED = (200,0,0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)


clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")

GRID_IMG = pygame.image.load(os.path.join("grid.png"))


class Grid:  # this is the sudoku grid of the window
	IMG = GRID_IMG

	def __init__(self):
		self.y = 0
		self.x = 0

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y))


def draw_window(win, grid):
	grid.draw(win)

	pygame.display.update()


if __name__ == "__main__":
	GRID = Grid()

	draw_window(WIN, GRID)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
