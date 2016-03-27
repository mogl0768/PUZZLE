import pygame
import sys
from pygame.locals import *
import random
from copy import deepcopy

pygame.init()
DISPLAY = (640, 480)
setdisplay = pygame.display.set_mode(DISPLAY)
matrix_to_pixel = 40

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))
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


CHAR_IMG = pygame.image.load("char.png")
stone_img = pygame.image.load("s.png")
ice_img = pygame.image.load("i.png")
floor_img = pygame.image.load("f.png")
goal_img = pygame.image.load("w.png")
block_to_picture = {ICE : ice_img, STONE : stone_img, FLOOR : floor_img, GOAL : goal_img, START : floor_img}

class Menu:
	def __init__(self):
		self.button1_rect = pygame.Rect(DISPLAY[0] / 4, 1.5 * DISPLAY[1] / 5, 320, 50)
		self.button2_rect = pygame.Rect(DISPLAY[0] / 4, 2.5 * DISPLAY[1] / 5, 320, 50)
		self.button3_rect = pygame.Rect(DISPLAY[0] / 4, 3.5 * DISPLAY[1] / 5, 320, 50)
		# each button is stored as [Rect-Object, Text, Handler]
		self.button1 = [self.button1_rect, "Campaign", self.button1_handler]
		self.button2 = [self.button2_rect, "Level Generator", self.button2_handler]
		self.button3 = [self.button3_rect, "Quit", self.button3_handler]
		self.buttons = [self.button1, self.button2, self.button3]
		self.selecting = True
		pygame.init()

	def main(self):	
		while self.selecting:
			setdisplay.fill(BLACK)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == MOUSEBUTTONUP:
					for button in self.buttons:
						if button[0].collidepoint(pygame.mouse.get_pos()):
							self.selecting = False
							button[2]()
			self.draw()
			pygame.display.update()
			fpsTime.tick(fps)

	def draw(self):
		for button in self.buttons:
			pygame.draw.rect(setdisplay, BLUE, button[0])
			self.write_rect(button[0], button[1])

	def button1_handler(self):
		next_scene = Game()
		next_scene.main()

	def button2_handler(self):
		next_menu = Second_Menu()
		next_menu.main()

	def button3_handler(self):
		pygame.quit()
		sys.exit()

	def write_rect(self, rect, string):
		"""writes string into rect on the screen"""
		label = myfont.render(string, 1, (255,255,0))
		setdisplay.blit(label, (rect.topleft[0] + 20, rect.topleft[1]))

class Second_Menu(Menu):
	def __init__(self):
		self.button1_rect = pygame.Rect(DISPLAY[0] / 4, 1.5 * DISPLAY[1] / 5, 320, 50)
		self.button2_rect = pygame.Rect(DISPLAY[0] / 4, 2.5 * DISPLAY[1] / 5, 320, 50)
		self.button3_rect = pygame.Rect(DISPLAY[0] / 4, 3.5 * DISPLAY[1] / 5, 320, 50)
		# each button is stored as [Rect-Object, Text, Handler]
		self.button1 = [self.button1_rect, "Use Monte Carlo", self.button1_handler]
		self.button2 = [self.button2_rect, "Use Custom", self.button2_handler]
		self.button3 = [self.button3_rect, "Back", self.button3_handler]
		self.buttons = [self.button1, self.button2, self.button3]
		self.selecting = True
		pygame.init()

	def button1_handler(self):
		next_scene = Generate_Levels(True)
		next_scene.main()

	def button2_handler(self):
		next_scene = Generate_Levels(False)
		next_scene.main()

	def button3_handler(self):
		next_menu = Menu()
		next_menu.main()


class Game:
	def __init__(self):
		self.playing = True
		self.key_to_dir = {K_UP : (0, -1), 
						   K_DOWN : (0, 1), 
						   K_LEFT : (-1, 0), 
						   K_RIGHT : (1, 0)}
		self.difficulty = 1
		self.matrix = self.generate_level(self.difficulty)
		self.char_pos = self.find_block(self.matrix, START)
		self.goal_pos = self.find_block(self.matrix, GOAL)
		self.movement_bank = [0, 0] # stores distance the player has yet to move
		self.matrix_height = len(self.matrix)
		self.matrix_width = len(self.matrix[0])
		self.myfont = pygame.font.SysFont("monospace", 50)

	def main(self):
		while self.playing:
			self.draw_matrix(self.matrix)
			setdisplay.blit(CHAR_IMG, (self.char_pos[0] * matrix_to_pixel, 
									   self.char_pos[1] * matrix_to_pixel)) 
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN: 
					if self.movement_bank == [0, 0] and event.key in list(self.key_to_dir.keys()):
						self.movement_bank = self.move(self.matrix, self.char_pos, self.key_to_dir[event.key])
					elif event.key == K_ESCAPE:
						menu = Menu()
						menu.main()
			for dimension in range(2):
				if self.movement_bank[dimension] != 0:
					direction = int (self.movement_bank[dimension] / abs(self.movement_bank[dimension])) # is either 1 or -1
					self.char_pos[dimension] += direction
					self.movement_bank[dimension] -= direction
			if self.char_pos == self.goal_pos:
				self.win()
			pygame.display.update()
			fpsTime.tick(fps)
	def draw_matrix(self, matrix):
		"""draw game-matrix on the screen"""
		for row_counter in range(len(matrix)):
			for col_counter in range(len(matrix[0])):
				setdisplay.blit(block_to_picture[matrix[row_counter][col_counter]], 
							   (col_counter * matrix_to_pixel, row_counter * matrix_to_pixel))

	def find_block(self, matrix, block):
		"""finds block in matrix, returns position of the block"""
		for line_counter in range(len(matrix)):
			if block in matrix[line_counter]:
				return [matrix[line_counter].index(block), line_counter]

	def move(self, matrix, char, direction):
		"""return a movement vector for the given direction"""
		next_block = [char[0] + direction[0], char[1] + direction[1]]
		counter = 0
		matrix_width = len(matrix[0])
		matrix_height = len(matrix)
		while (next_block[0] < matrix_width and 
			   next_block[1] < matrix_height and 
			   matrix[next_block[1]][next_block[0]] == ICE):
			counter += 1
			next_block = [next_block[0] + direction[0], next_block[1] + direction[1]]
		if not (next_block[0] < matrix_width and next_block[1] < matrix_height):
			return [direction[0] * counter, direction[1] * counter]
		if  matrix[next_block[1]][next_block[0]] in [FLOOR, GOAL, START]:
			counter += 1
		return [direction[0] * counter, direction[1] * counter]

	def generate_level(self, difficulty):
		"""
		generates solveable gamematrix using a monte carlo player
		difficulty is an int from 1 to 10. 10 is the hardest, 1 the easiest
		"""
		assert 0 < difficulty < 11 , "difficulty not valid"
		matrix = load_level("template1.txt")
		matrix_height = len(matrix)
		matrix_width = len(matrix[0])
		blocks_changed = 0
		start_pos = self.find_block(matrix, START)
		goal_pos = self.find_block(matrix, GOAL)
		max_tries = 11 - difficulty #maximum succesful attempts for the level allowed
		number_of_tests = 10
		matrix_copy = deepcopy(matrix) # for resseting

		while True:
			if blocks_changed < 20:
				rand_x = random.randrange(1, matrix_width - 1)
				rand_y = random.randrange(1, matrix_height - 1)
				if matrix[rand_y][rand_x] < 3: # changed block shouldn't be a start or goal block
					matrix[rand_y][rand_x] = random.randrange(3)
					blocks_changed += 1
			elif blocks_changed < 50: #enough blocks have been changed, but not too many
				succesful_tries = 0
				tests = 0
				while tests <= number_of_tests: # test level ten times
					if self.test_level(matrix, list(start_pos), goal_pos):
						succesful_tries += 1 
					if succesful_tries > max_tries:
						# level is too easy, reset everything
						matrix = deepcopy(matrix_copy)
						blocks_changed = 0
					tests += 1
				if 0 < succesful_tries <= max_tries:
					# level is solveable and hard enough
					return matrix
				if succesful_tries == 0:
					# level is probably unsolveable, change more blocks
					for dummy in range(5):
						rand_x = random.randrange(1, matrix_width - 1)
						rand_y = random.randrange(1, matrix_height - 1)
						if matrix[rand_y][rand_x] < 3: # changed block shouldn't be a start or goal block
							matrix[rand_y][rand_x] = random.randrange(3)
							blocks_changed += 1
			else:
				matrix = deepcopy(matrix_copy)
				blocks_changed = 0



	def test_level(self, matrix, start_pos, goal_pos):
		"""tests level by letting a virtual character make 200 random moves in it"""
		pos = start_pos
		for dummy in range(200): 
			movement = self.move(matrix, pos, random.choice(DIRECTIONS))
			pos[0] += movement[0]
			pos[1] += movement[1]
			if pos == goal_pos:
				return True
		return False

	def generate_level2(self):
		"""different approch to generating a level"""
		matrix = load_level("template2.txt")
		matrix_height = len(matrix)
		matrix_width = len(matrix[0])
		#generate start point:
		start = (random.randrange(2, matrix_width - 2), random.randrange(2, matrix_height - 2))
		return_value = self.generate_path(matrix, [start])

		while len(return_value[0]) < 15:
			matrix = load_level("template2.txt")
			start = (random.randrange(2, matrix_width - 2), random.randrange(2, matrix_height - 2))
			matrix[start[1]][start[0]] = START
			return_value = self.generate_path(matrix, [start])
		matrix = return_value[1]
		stop_points = return_value[0]
		goal = stop_points[-1]
		blocks_passed = return_value[2]
		matrix[goal[1]][goal[0]] = GOAL
		self.gen_access(matrix, start, stone=True)
		self.generate_distractions(matrix, stop_points, blocks_passed)
		matrix[1][1] = START
		return matrix


	def generate_path(self, matrix, stop_points, blocks_passed = [], incoming_direction = (0, 0), stone = False, main_path = True, max_lenght = 100):
		"""generates a long path starting from the given start points into an empty template"""
		char_pos = stop_points[-1]

		# find connecting points that aren't connected to any other stops on the way
		same_y = [(x, char_pos[1]) for x in range(2, len(matrix[0]) - 2) 
			      if self.one_block(matrix, (x, char_pos[1]), stone) 
			      and not (x, char_pos[1]) in stop_points]
		same_x = [(char_pos[0], y) for y in range(2, len(matrix) - 2) 
				  if self.one_block(matrix, (char_pos[0], y), stone) 
				  and not  (char_pos[0], y)  in stop_points]

		# filter list to not include points next to the characters position
		same_y = [coord for coord in same_y if abs(coord[0] - char_pos[0]) != 1 and abs(coord[1] - char_pos[1]) != 1]
		same_x = [coord for coord in same_x if abs(coord[0] - char_pos[0]) != 1 and abs(coord[1] - char_pos[1]) != 1]

		# filter points that would make the char move back to where they came from:
		if incoming_direction[0]:
			same_y = [coord for coord in same_y if char_pos[0] * incoming_direction[0]  < coord[0] * incoming_direction[0]]
		elif incoming_direction[1]:
			same_x = [coord for coord in same_x if char_pos[1] * incoming_direction[1]  < coord[1] * incoming_direction[1]]

		if stone:
			#filter points that lie behind the stone:
			if incoming_direction[0]:
				same_y = [coord for coord in same_y if char_pos[0] * incoming_direction[0]  > coord[0] * incoming_direction[0]]
			else:
				same_x = [coord for coord in same_x if char_pos[1] * incoming_direction[1]  > coord[1] * incoming_direction[1]]
		#filter points that are placed upon already
		same_y = [coord for coord in same_y if coord not in stop_points]
		same_x = [coord for coord in same_x if coord not in stop_points]

		# check for base cases:
		# path longer than specified
		if len(stop_points) > max_lenght:
			if stone:
				stop_points.append((char_pos[0] + incoming_direction[0], char_pos[1] + incoming_direction[1]))
			else:
				stop_points.append(char_pos)
			return stop_points, matrix, blocks_passed
		# no more blocks to place:
		if not (same_y or same_x):
			if stone:
				stop_points.append((char_pos[0] + incoming_direction[0], char_pos[1] + incoming_direction[1]))
			else:
				stop_points.append(char_pos)
			return stop_points, matrix, blocks_passed

		# place a random block out of the given possibilities:
		direction, is_stone = self.place_block(matrix, same_x, same_y, random.choice([STONE, FLOOR]), stop_points, blocks_passed)
		return self.generate_path(matrix, stop_points, blocks_passed, direction, stone = is_stone)

	def place_block(self, matrix, x_list, y_list, block_type, stop_points, blocks_passed):
		"""helper function for generatelevel2, places block from the lists on the matrix, modifies relevant lists and returns direction"""
		char_pos = stop_points[-1]
		# choose a list
		if x_list and y_list:
			list_choice = random.choice([x_list, y_list])
		else:
			list_choice = x_list if x_list else y_list
		# choose a block and place it
		block_choice = random.choice(list_choice)
		matrix[block_choice[1]][block_choice[0]] = block_type
		direction = self.find_direction(char_pos, block_choice)
		stop_points.append(block_choice)

		if block_type == STONE:
			stop_points.append((block_choice[0] - direction[0], block_choice[1] - direction[1]))

		blocks_passed += self.get_blocks_passed(char_pos, block_choice)
		return direction, block_type == STONE

	def one_block(self, matrix, block, stone):
		"""
		tests if block only connects to exactly one other block by testing if a character would move to the boarder of the matrix
		helper function for generate_path
		"""
		matrix_height = len(matrix)
		matrix_width = len(matrix[0])
		right_positions = 0
		move_direction = self.move(matrix, block, (0, -1))
		if block[1] + move_direction[1] == 1:
			right_positions += 1
		move_direction = self.move(matrix, block, (0, 1))
		if block[1] + move_direction[1] == matrix_height - 2:
			right_positions += 1

		move_direction = self.move(matrix, block, (-1, 0))
		if block[0] + move_direction[0] == 1:
			right_positions += 1

		move_direction = self.move(matrix, block, (1, 0))
		if block[0] + move_direction[0] == matrix_width - 2:
			right_positions += 1

		return (right_positions == 3 and not stone) or (right_positions == 4 and stone)

	def generate_distractions(self, matrix, stop_points, blocks_passed):
		"""places meaningless blocks to make the win-path less obvious"""
		#generate all blocks in the matrix (except blocks on the boarder)
		all_positions = set([])
		for y in range(2, len(matrix) - 2):
			for x in range(2, len(matrix[0]) - 2):
				all_positions.add((x, y))

		blocks_placed = []
		# positions that are not part of the win path and not already placed upon:
		free_positions = list(all_positions.difference(set(blocks_passed)).difference(set(stop_points)))


		for block in free_positions:
			valid_block = True
			for block2 in blocks_placed:
				if self.is_connecting(block, block2):			
					valid_block = False
			if valid_block:
				connecting = self.get_connecting_blocks(matrix, block)
				intersection = list(set(stop_points).intersection(connecting))
				if len(intersection) == 2: # blocks connecting 2 points of the win-path
					first = intersection[0] if stop_points.index(intersection[0]) < stop_points.index(intersection[1]) else intersection[1]
					second = intersection[1] if first == intersection[0] else intersection[0]
					# it should be possible to go back in the win-path, but not forward
					direction = self.find_direction(second, block)
					new_block = (block[0] + direction[0], block[1] + direction[1])
					if new_block in free_positions:
						matrix[new_block[1]][new_block[0]] = STONE
						blocks_placed.append(new_block)
						blocks_placed.append(block)
				elif len(intersection) == 1: # block just connected with one point of the win path
					matrix[block[1]][block[0]] = FLOOR
					blocks_placed.append(block)
				elif len(intersection) == 0:
					valid = True
					for block3 in stop_points:
						if self.is_connecting(block, block3):
							valid = False
					if valid:
						matrix[block[1]][block[0]] = FLOOR
						blocks_placed.append(block)
						self.gen_access(matrix, block)

				

	def not_in_boarder(self, matrix, block):
		"""return true if the block is not on the boarder of the matrix"""
		return 1 < block[0] < len(matrix[0]) and 1 < block[1] < len(matrix)
	def is_connecting(self, block1, block2):
		return block1[0] == block2[0] or block1[1] == block2[1] 
	def get_connecting_blocks(self, matrix, block):
		"""returns connecting blocks that arent on the boarder"""
		matrix_height = len(matrix)
		matrix_width = len(matrix[0])
		output = []
		movement = self.move(matrix, block, (0, -1))
		if block[1] + movement[1] != 1:
			output.append((block[0] + movement[0], block[1] + movement[1]))
		movement = self.move(matrix, block, (0, 1))
		if block[1] + movement[1] != matrix_height - 2:
			output.append((block[0] + movement[0], block[1] + movement[1]))
		movement = self.move(matrix, block, (-1, 0))
		if block[0] + movement[0] != 1:
			output.append((block[0] + movement[0], block[1] + movement[1]))
		movement = self.move(matrix, block, (1, 0))
		if block[0] + movement[0] != matrix_width - 2:
			output.append((block[0] + movement[0], block[1] + movement[1]))
		return output

	def gen_access(self, matrix, block, stone=False):
		"""generates a random access-point to the block on the boarder of the matrix, modifies matrix and returns placed block"""
		matrix_width = len(matrix[0])
		matrix_height = len(matrix)
		possibilities = [] 
		choice = (0, 0)
		alt_possibilities = [] # stores alternatives for floor blocks if there are no possibilities for stone blocks
		vert_directions = ((0, -1), (0, 1))
		hor_directions = ((-1, 0), (1, 0))
		relevant_number = {(0, -1) : matrix_height,  (0, 1) : matrix_height,
						   (-1, 0) : matrix_width, (1, 0) : matrix_width}
		other_dimension = {(0, -1) : hor_directions,  (0, 1) : hor_directions,
						   (-1, 0) : vert_directions, (1, 0) : vert_directions}

		for direction in DIRECTIONS:
			# move in direction
			movement = self.move(matrix, block, direction)
			new_pos = (block[0] + movement[0], block[1] + movement[1])
			#check if block is on boarder
			if (new_pos[0] in [1, matrix_width - 2]) != (new_pos[1] in [1, matrix_height - 2]): # only true if one of them is true (XOR), filters corners
				alt_possibilities.append(new_pos)

				if stone:
					for other_dir in other_dimension[direction]:
						# hitting stone block from the other side shouldn't connect to a block:
						if self.get_connecting_blocks(matrix, (new_pos[0] + 2 * other_dir[0], new_pos[1] + 2 * other_dir[1])) == []:
							possibilities.append((new_pos[0] + other_dir[0], new_pos[1] + other_dir[1]))
				else:
					possibilities.append(new_pos)

		if possibilities:
			choice = random.choice(possibilities)
			matrix[choice[1]][choice[0]] = STONE if stone else FLOOR
		elif alt_possibilities:
			choice = random.choice(alt_possibilities)
			matrix[choice[1]][choice[0]] = FLOOR
		return choice

	def get_blocks_passed(self, start, goal):
		"""returns blocks a character passes when moving from start to goal"""
		if start[0] < goal[0]:
			return [(x, start[1]) for x in range(start[0], goal[0])]
		elif start[0] > goal[0]:
			return [(x, start[1]) for x in range(goal[0], start[0])]
		elif start[1] < goal[1]:
			return [(start[0], y) for y in range(start[1], goal[1])]
		else:
			return [(start[0], y) for y in range(goal[1], start[1])]


	def find_direction(self, start, goal):
		"""returns direction the characters moves to when he goes from start to goal"""
		x = abs(goal[0] - start[0]) / (goal[0] - start[0]) if goal[0] - start[0] != 0 else 0 # fix zero division error
		y = abs(goal[1] - start[1]) / (goal[1] - start[1]) if goal[1] - start[1] != 0 else 0
		return (int(x), int(y))

	def win (self):
		"""generates new level based on how many levels were already solved"""
		label = self.myfont.render(("Level " + str(self.difficulty) + " finished!") , 1, BLACK)
		setdisplay.blit(label, (50, 100))
		pygame.display.update()
		pygame.time.wait(1000)
		if self.difficulty < 10:
			self.difficulty += 1
		if self.difficulty < 5:
			self.matrix = self.generate_level(self.difficulty)
		elif self.difficulty <8:
			self.matrix = self.generate_level2()
		else:
			self.matrix = self.generate_level(self.difficulty)
		self.char_pos = self.find_block(self.matrix, START)
		self.goal_pos = self.find_block(self.matrix, GOAL)

class Generate_Levels(Game):
	def __init__(self, monte_carlo = True, difficulty = 10):
		self.playing = True
		self.key_to_dir = {K_UP : (0, -1), K_DOWN : (0, 1), K_LEFT : (-1, 0), K_RIGHT : (1, 0)}
		self.difficulty = difficulty
		self.matrix = self.generate_level(self.difficulty) if monte_carlo else self.generate_level2()
		self.char_pos = self.find_block(self.matrix, START)
		self.goal_pos = self.find_block(self.matrix, GOAL)
		self.movement_bank = [0, 0] # stores distance the player has yet to move
		self.matrix_height = len(self.matrix)
		self.matrix_width = len(self.matrix[0])
		self.myfont = pygame.font.SysFont("monospace", 70)
	def win(self):
		"""return to menu after level is completed"""
		menu = Second_Menu()
		menu.main()

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
	menu = Menu()
	menu.main()
