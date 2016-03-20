import pygame
import sys
from pygame.locals import *

pygame.init()
DISPLAY = (640, 480)
setdisplay = pygame.display.set_mode(DISPLAY)
matrix_to_pixel = 40

char = pygame.image.load("char.png")
fps = 30
fpsTime = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", DISPLAY[0] // 20)

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

stone_img = pygame.image.load("s.png")
ice_img = pygame.image.load("i.png")
floor_img = pygame.image.load("f.png")
block_to_picture = {ICE : ice_img, STONE : stone_img, FLOOR : floor_img, GOAL : floor_img, START : floor_img}

class Menu:
	def __init__(self):
		self.start = pygame.Rect(DISPLAY[0] / 3, 1.5 * DISPLAY[1] / 5, 250, 50)
		self.leveledit = pygame.Rect(DISPLAY[0] / 3, 2.5 * DISPLAY[1] / 5, 250, 50)
		self.quit = pygame.Rect(DISPLAY[0] / 3, 3.5 * DISPLAY[1] / 5, 250, 50)
		self.buttons = [(self.start, "Start"), (self.leveledit, "Level Editor"), (self.quit, "Quit")]
		self.rect_to_func = {"Start": game.main, "Level Editor": leveledit.main, "Quit" : self.quit_func}
		self.selecting = True
		self.next_scene = game.main
		pygame.init()

	def main(self):	
		while self.selecting:
		    for event in pygame.event.get():
		        if event.type == QUIT:
		            pygame.quit()
		            sys.exit()
		        if event.type == MOUSEBUTTONUP:
		        	for rect, text in self.buttons:
		        		if rect.collidepoint(pygame.mouse.get_pos()):
		        			self.selecting = False
		        			self.next_scene = self.rect_to_func[text]
		    self.draw()
		    pygame.display.update()
		    fpsTime.tick(fps)
		self.next_scene()
	def draw(self):
		for button, text in self.buttons:
			pygame.draw.rect(setdisplay, BLUE, button)
			self.write_rect(button, text)
	def quit_func(self):
		pygame.quit()
		sys.exit()
	def write_rect(self, rect, string):
		"""writes string into rect on the screen"""
		label = myfont.render(string, 1, (255,255,0))
		setdisplay.blit(label, (rect.topleft[0] + 20, rect.topleft[1]))
class Game:
	def __init__(self):
		self.playing = True
		self.key_to_dir = {K_UP : (0, -1), K_DOWN : (0, 1), K_LEFT : (-1, 0), K_RIGHT : (1, 0)}
		self.matrix = load_level("1.txt")

	def main(self):
		while self.playing:
			self.draw_matrix(self.matrix)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN and event.key in list(game.key_to_dir.keys()):
					self.move(self.key_to_dir[event.key])
			pygame.display.update()
			fpsTime.tick(fps)
	def draw_matrix(self, matrix):
		for row_counter in range(len(matrix)):
			for col_counter in range(len(matrix[0])):
				setdisplay.blit(block_to_picture[matrix[row_counter][col_counter]], (col_counter * matrix_to_pixel, row_counter * matrix_to_pixel))
	def move(self, dir):
		pass
class Leveledit:
	def main(self):
		pass
def load_level(level_file):
	"""takes level file, returns game Matrix"""
	matrix = []
	with open(level_file) as file:
		for line in file:
			matrix.append([int(block) for block in line.split()])
	return matrix

def save_level(matrix, filename):
	"""writes game-matrix in file"""
	with open(filename, "w") as file:
		for line in matrix:
			for block in line:
				file.write(str(block) + " ")
			file.write("\n")

if __name__ == '__main__':
	game = Game()
	leveledit = Leveledit()
	menu = Menu()
	#leveledit = Leveledit()
	menu.main()
