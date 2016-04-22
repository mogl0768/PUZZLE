from copy import deepcopy
from global_vars import *

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))

class Level:
	def __init__(self, matrix):
		self.matrix = matrix
		self.start = self.find_block(START)
		self.goal = self.find_block(GOAL)
		self.height = len(self.matrix)
		self.width = len(self.matrix[0])

	def draw(self):
		for row_counter in range(self.height):
			for col_counter in range(self.width):
				setdisplay.blit(block_to_picture[self.matrix[row_counter][col_counter]], 
							   (col_counter * matrix_to_pixel, row_counter * matrix_to_pixel))

	def find_block(self, block):
		"""finds block in matrix, returns position of the block"""
		for line_counter in range(self.height):
			if block in self.matrix[line_counter]:
				return [self.matrix[line_counter].index(block), line_counter]

	def move(self, char, direction):
		"""return a movement vector for the given direction"""
		next_block = [char[0] + direction[0], char[1] + direction[1]]
		counter = 0
		while self.matrix[next_block[1]][next_block[0]] == ICE:
			counter += 1
			next_block = [next_block[0] + direction[0], next_block[1] + direction[1]]

		if  self.matrix[next_block[1]][next_block[0]] in [FLOOR, GOAL, START]:
			counter += 1
		return [direction[0] * counter, direction[1] * counter]

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


