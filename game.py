import pygame
import sys
from pygame.locals import *
import random
from copy import deepcopy
import level
from levelgen import *
from global_vars import *


class Button:
	def __init__(self, text, rect, func=None):
		self.text = text
		self.rect = rect
		self.func = func

	def draw(self):
		pygame.draw.rect(setdisplay, BLUE, self.rect)
		label = myfont.render(self.text, 1, (255,255,0))
		setdisplay.blit(label, (self.rect.topleft[0] + 20, self.rect.topleft[1]))

	def check_collide(self, pos):
		"""tests if mouse collides with Button"""
		return self.rect.collidepoint(pos)
class Menu:
	def __init__(self, *args):
		self.buttons = args

	def main(self):	
		while True:
			setdisplay.fill(BLACK)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == MOUSEBUTTONUP:
					mouse_pos = pygame.mouse.get_pos()
					for button in self.buttons:
						if button.check_collide(mouse_pos):
							button.func()
			self.draw()
			pygame.display.update()
			fpsTime.tick(fps)

	def draw(self):
		for button in self.buttons:
			button.draw()

class Game:
	def __init__(self, mode):
		self.mode = mode
		if self.mode == "campaign":
			self.level = Custom_level()
		else:
			self.level = Monte_carlo_level(1)
		self.char_pos = self.level.start
		self.goal_pos = self.level.goal
		self.playing = True
		self.movement_bank = [0, 0]
		self.difficulty = 1

	def main(self):
		key_to_direction = {K_UP : (0, -1), 
					  		K_DOWN : (0, 1), 
					 		K_LEFT : (-1, 0), 
					 		K_RIGHT : (1, 0)}

		while self.playing:
			self.level.draw()
			setdisplay.blit(CHAR_IMG, (self.char_pos[0] * matrix_to_pixel, 
									   self.char_pos[1] * matrix_to_pixel))
			for event in pygame.event.get():
				if event.type == QUIT:
					quit()
				if event.type == KEYDOWN: 
					if self.movement_bank == [0, 0] and event.key in list(key_to_direction.keys()):
						self.movement_bank = self.level.move(self.char_pos, key_to_direction[event.key])
					elif event.key == K_ESCAPE:
						main_menu.main()
			for dimension in range(2):
				if self.movement_bank[dimension] != 0:
					direction = int (self.movement_bank[dimension] / abs(self.movement_bank[dimension])) # is either 1 or -1
					self.char_pos[dimension] += direction
					self.movement_bank[dimension] -= direction
			if self.char_pos == self.goal_pos:
				self.win()
			pygame.display.update()
			fpsTime.tick(fps)

	def win(self):
		if self.mode == "campaign":
			label = myfont.render(("Level " + str(self.difficulty) + " finished!") , 1, BLACK)
			setdisplay.blit(label, (50, 100))
			pygame.display.update()
			pygame.time.wait(1000)
			if self.difficulty < 10:
				self.difficulty += 1

			if self.difficulty < 5:
				self.level = self.level = Monte_carlo_level(self.difficulty)
			elif self.difficulty <8:
				self.level = Custom_level_generator()
			else:
				self.level = Level("monte_carlo", self.difficulty)
			self.char_pos = self.level.start
			self.goal_pos = self.level.goal
		else:
			main_menu.main()

def quit():
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	# create Rect-Objects on future button positions
	rects= [pygame.Rect(160, 144, 320, 50), pygame.Rect(160, 240, 320, 50), pygame.Rect(160, 336, 320, 50)]
	campaign = Game("campaign")
	level_gen_monte = Game("monte_carlo")
	level_gen_custom = Game("custom")
	#(self, text, rect, func=None)
	button1 = Button("Campaign", rects[0], campaign.main)
	button2 = Button("Level Generator", rects[1])
	button3 = Button("Quit", rects[2], quit)
	main_menu = Menu(button1, button2, button3)

	button4 = Button("Use Monte Carlo", rects[0], level_gen_monte.main)
	button5 = Button("Use Custom",rects[1], level_gen_custom.main)
	button6 = Button("Back", rects[2], main_menu.main)
	sec_menu = Menu(button4, button5, button6)

	button2.func = sec_menu.main
	main_menu.main()

