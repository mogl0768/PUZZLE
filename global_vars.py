import pygame
import sys
from pygame.locals import *

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))

#colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

# number representations of game blocks:
ICE = 0
STONE = 1
FLOOR = 2
GOAL = 3
START = 4

pygame.init()

DISPLAY = (640, 480)
setdisplay = pygame.display.set_mode(DISPLAY)
matrix_to_pixel = 40

fps = 30
fpsTime = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", DISPLAY[0] // 20)

CHAR_IMG = pygame.image.load("char.png")
stone_img = pygame.image.load("s.png")
ice_img = pygame.image.load("i.png")
floor_img = pygame.image.load("f.png")
goal_img = pygame.image.load("w.png")
block_to_picture = {ICE : ice_img, 
					STONE : stone_img, FLOOR : 
					floor_img, GOAL : goal_img, 
					START : floor_img}