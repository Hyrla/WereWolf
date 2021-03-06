# -*- coding: utf-8 -*-

#####################################################################################
#   ______             _               _          ______             _            	#
#  |  ____|           | |             | |        |  ____|           (_)           	#
#  | |__ _ __ ___  ___| |_ _ __  _   _| |_ ___   | |__   _ __   __ _ _ _ __   ___ 	#
#  |  __| '__/ _ \/ __| __| '_ \| | | | __/ _ \  |  __| | '_ \ / _` | | '_ \ / _ \	#
#  | |  | | | (_) \__ \ |_| |_) | |_| | ||  __/  | |____| | | | (_| | | | | |  __/	#
#  |_|  |_|  \___/|___/\__| .__/ \__, |\__\___|  |______|_| |_|\__, |_|_| |_|\___|	#
#                         | |     __/ |                         __/ |             	#
#                         |_|    |___/                         |___/              	#
#																					#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#	Created by	:																	#
#		ALESSANDRI Julien															#
#		HEISS Gauthier																#
#																					#
#	Version :  Alpha 0.1 - April, 13th 2016											#
#																					#
#####################################################################################

import pygame
from threading import Thread
from pygame.locals import *
from math import sqrt
from Constantes import *

# Camera
class Camera:
	def __init__(self, position_x = 0, position_y = 0):
		self.position_x = position_x
		self.position_y = position_y

# Graphical Object Class
class GrObject:
	def __init__(self, image, position_x, position_y, layer, can_cross = True, must_refresh = True):
		self.image = pygame.image.load(image)
		self.position_x = position_x
		self.position_y = position_y
		self.layer = layer
		self.must_refresh = must_refresh
		self.can_cross = can_cross

# Sprite Class
class Sprite:
	def __init__(self, sprite, position_x, position_y, orientation = "down", float_position = 32, speed = 2, refresh_freq = 0.125, refresh_count = 0, move_buffer = [], sprite_height = 64):
		self.sprite = sprite
		self.position_x = position_x
		self.position_y = position_y
		self.orientation = orientation
		self.float_position = float_position
		self.speed = speed
		self.refresh_freq = refresh_freq
		self.refresh_count = refresh_count
		self.move_buffer = move_buffer
		sprite_conv = pygame.image.load(sprite + "/up.png").convert()
		self.sprite_height = sprite_conv.get_height()
		
	def draw(self):
		if (self.float_position >= 32 and self.move_buffer != []):
			self.move(self.move_buffer[0])
			self.move_buffer.remove(self.move_buffer[0])
		if (self.float_position < 32):
			if (self.orientation == "down"):
				pos_x = self.position_x * 32
				pos_y = self.position_y * 32 - 32 + self.float_position - (64 - self.sprite_height)
			elif (self.orientation == "up"):
				pos_x = self.position_x * 32
				pos_y = self.position_y * 32 + 32 - self.float_position - (64 - self.sprite_height)
			elif (self.orientation == "left"):
				pos_x = self.position_x * 32 + 32 - self.float_position
				pos_y = self.position_y * 32 - (64 - self.sprite_height)
			elif (self.orientation == "right"):
				pos_x = self.position_x * 32 - 32 + self.float_position
				pos_y = self.position_y * 32 - (64 - self.sprite_height)
			
			if (self.refresh_count <= 1):
				window.blit(pygame.image.load(self.sprite + "/" + self.orientation + ".png"), (pos_x + cam.position_x, pos_y + cam.position_y))
				self.refresh_count += self.refresh_freq
			elif (self.refresh_count <= 2):
				window.blit(pygame.image.load(self.sprite + "/" + self.orientation + "_m1.png"), (pos_x + cam.position_x, pos_y + cam.position_y))
				self.refresh_count += self.refresh_freq
			elif (self.refresh_count <= 3):
				window.blit(pygame.image.load(self.sprite + "/" + self.orientation + ".png"), (pos_x + cam.position_x, pos_y + cam.position_y))
				self.refresh_count += self.refresh_freq
			elif (self.refresh_count <= 4):
				window.blit(pygame.image.load(self.sprite + "/" + self.orientation + "_m2.png"), (pos_x + cam.position_x, pos_y + cam.position_y))
				self.refresh_count += self.refresh_freq
			else:
				self.refresh_count = 0
			
			self.float_position += 1 * self.speed
		else:
			window.blit(pygame.image.load(self.sprite + "/" + self.orientation + ".png"), (self.position_x * 32 + cam.position_x, self.position_y * 32 - (64 - self.sprite_height) + cam.position_y))

	def move(self, direction):
		can_go = True
		if (direction == "right"):
			for obj in getObjects(self.position_x + 1, self.position_y):
				if (obj.can_cross == False):
					can_go = False
			if (self.float_position >= 32):
				self.orientation = "right"
				if (can_go == True):
					self.float_position = 0
					self.position_x += 1
					
		elif (direction == "left"):
			for obj in getObjects(self.position_x - 1, self.position_y):
				if (obj.can_cross == False):
					can_go = False
			if (self.float_position >= 32):
				self.orientation = "left"
				if (can_go == True):
					self.float_position = 0
					self.position_x -= 1
				
		elif (direction == "up"):
			for obj in getObjects(self.position_x, self.position_y - 1):
				if (obj.can_cross == False):
					can_go = False
			if (self.float_position >= 32):
				self.orientation = "up"
				if (can_go == True):
					self.float_position = 0
					self.position_y -= 1
				
		elif (direction == "down"):
			for obj in getObjects(self.position_x, self.position_y + 1):
				if (obj.can_cross == False):
					can_go = False
			if (self.float_position >= 32):
				self.orientation = "down"
				if (can_go == True):
					self.float_position = 0
					self.position_y += 1

# Tileset Class
class Tileset:
	def __init__(self, image, rect_x1, rect_y1, rect_x2, rect_y2, layer = 0, can_cross = True):
		self.image = image + "/image.png"
		self.rect_x1 = rect_x1
		self.rect_y1 = rect_y1
		self.rect_x2 = rect_x2
		self.rect_y2 = rect_y2
		self.layer = layer
		self.can_cross = can_cross

# Player class
class Player:
	def __init__(self, name, sprite, position_x, position_y, orientation = "down", float_position = 32, speed = 2, refresh_freq = 0.125, refresh_count = 0, sprite_height = 64):
		self.name = name
		self.sprite = sprite
		self.position_x = position_x
		self.position_y = position_y
		self.orientation = orientation
		self.float_position = float_position
		self.speed = speed
		self.refresh_freq = refresh_freq
		self.refresh_count = refresh_count
		self.sprite_height = sprite_height

# Drawing function
def drawObject(grobj):
	objects_list[grobj.layer].append(grobj)
	
# Sprite drawing function
def drawSprite(spr):
	sprites_list.append(spr)

# Terrain drawing function
def drawTileset(tiles):
	for xi in range(tiles.rect_x1, tiles.rect_x2):
		for yi in range (tiles.rect_y1, tiles.rect_y2):
			objects_list[tiles.layer].append(GrObject(tiles.image, xi, yi, tiles.layer, tiles.can_cross, True))

# Get distance function
def getDistance(spr1, spr2):
	x1 = spr1.position_x
	y1 = spr1.position_y
	x2 = spr2.position_x
	y2 = spr2.position_y
	return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Get objects function
def getObjects(x, y):
	templist = []
	for lay in range(0, len(objects_list) - 1):
		for obj in objects_list[lay]:
			if (obj.position_x == x and obj.position_y == y):
				templist.append(obj)
	return templist
			

# Initial function
def init(x, y, player, title, icon, frame_rate):
	global window
	
	global objects_list
	objects_list = [[], [], [], [], []]
	
	global sprites_list
	sprites_list = []

	global MainPlayer
	MainPlayer = player

	global FPS
	FPS = frame_rate

	global cam
	cam = Camera()
	
	pygame.init()
	window = pygame.display.set_mode((x, y))
	pygame.display.set_caption(title)
	pygame.display.set_icon(pygame.image.load(icon))
	pygame.key.set_repeat(1,1)
	pygame.display.flip()

	sprite_conv = pygame.image.load(MainPlayer.sprite + "/up.png").convert()
	MainPlayer.sprite_height = sprite_conv.get_height()
	
# Main function/class
class MainRun(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		keep = 1
		global spriteTopBuffer
		spriteTopBuffer = []
		global debug_draw_position_refresh
		debug_draw_position_refresh = True
		
		while keep: # Main while
			pygame.time.Clock().tick(FPS)
			can_go = True
			
			#----------------#
			# 	  EVENTS	 #
			#----------------#
			for event in pygame.event.get():	
				if event.type == QUIT:
					keep = 0
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keep = 0
					elif event.key == K_RIGHT:
						for obj in getObjects(MainPlayer.position_x + 1, MainPlayer.position_y):
							if (obj.can_cross == False):
								can_go = False
						if (MainPlayer.float_position >= 32):
							MainPlayer.orientation = "right"
							if (can_go == True):
								MainPlayer.float_position = 0
								MainPlayer.position_x += 1
								debug_draw_position_refresh = True
							
					elif event.key == K_LEFT:
						for obj in getObjects(MainPlayer.position_x - 1, MainPlayer.position_y):
							if (obj.can_cross == False):
								can_go = False
						if (MainPlayer.float_position >= 32):
							MainPlayer.orientation = "left"
							if (can_go == True):
								MainPlayer.float_position = 0
								MainPlayer.position_x -= 1
								debug_draw_position_refresh = True
								
					elif event.key == K_UP:
						for obj in getObjects(MainPlayer.position_x, MainPlayer.position_y - 1):
							if (obj.can_cross == False):
								can_go = False
						if (MainPlayer.float_position >= 32):
							MainPlayer.orientation = "up"
							if (can_go == True):
								MainPlayer.float_position = 0
								MainPlayer.position_y -= 1
								debug_draw_position_refresh = True
								
					elif event.key == K_DOWN:
						for obj in getObjects(MainPlayer.position_x, MainPlayer.position_y + 1):
							if (obj.can_cross == False):
								can_go = False
						if (MainPlayer.float_position >= 32):
							MainPlayer.orientation = "down"
							if (can_go == True):
								MainPlayer.float_position = 0
								MainPlayer.position_y += 1
								debug_draw_position_refresh = True
		
			#----------------#
			#	 OBJECTS	 #
			#----------------#
			#window.fill((0,0,0)) # Clear Screen

			# First layers
			for lay in range(0, len(objects_list) - 2):
				for obj in objects_list[lay]:
					if (obj.must_refresh == True):
						window.blit(obj.image, (obj.position_x * 32 + cam.position_x, obj.position_y * 32 + cam.position_y))
						obj.must_refresh = False
					elif (getDistance(obj, MainPlayer) < 16): #and MainPlayer.float_position <= 32):
						window.blit(obj.image, (obj.position_x * 32 + cam.position_x, obj.position_y * 32 + cam.position_y))
					else:
						for spri in sprites_list:
							if (getDistance(spri, obj) < 3): #and spri.float_position <= 32):
								window.blit(obj.image, (obj.position_x * 32 + cam.position_x, obj.position_y * 32 + cam.position_y))
					if (debug_draw_position == True and debug_draw_position_refresh == True):
						if (obj.position_x + cam.position_x <= 5 or obj.position_y + cam.position_y <= 1):
							window.blit(obj.image, (obj.position_x * 32 + cam.position_x, obj.position_y * 32 + cam.position_y))

			# Sprites
			for spr in sprites_list:
				if not(getDistance(spr, MainPlayer) <= 2 and spr.position_y > MainPlayer.position_y):
					spr.draw()
				else:
					spriteTopBuffer.append(spr)

			# Main player
			if (MainPlayer.float_position < 32):
				if (MainPlayer.orientation == "down"):
					pos_x = MainPlayer.position_x * 32
					pos_y = MainPlayer.position_y * 32 - 32 + MainPlayer.float_position - (64 - MainPlayer.sprite_height)
					cam.position_y -= MainPlayer.speed
				elif (MainPlayer.orientation == "up"):
					pos_x = MainPlayer.position_x * 32
					pos_y = MainPlayer.position_y * 32 + 32 - MainPlayer.float_position - (64 - MainPlayer.sprite_height)
					cam.position_y += MainPlayer.speed
				elif (MainPlayer.orientation == "left"):
					pos_x = MainPlayer.position_x * 32 + 32 - MainPlayer.float_position
					pos_y = MainPlayer.position_y * 32 - (64 - MainPlayer.sprite_height)
					cam.position_x += MainPlayer.speed
				elif (MainPlayer.orientation == "right"):
					pos_x = MainPlayer.position_x * 32 - 32 + MainPlayer.float_position
					pos_y = MainPlayer.position_y * 32 - (64 - MainPlayer.sprite_height)
					cam.position_x -= MainPlayer.speed

				"""
				if ((frame_size * pos_x) - cam.position_x > frame_size * nbr_frame_x):
					cam.position_x += 1
				if ((frame_size * pos_x) + cam.position_x > frame_size * nbr_frame_x):
					cam.position_x -= 1
				if ((frame_size * pos_y) - cam.position_y > frame_size * nbr_frame_y):
					cam.position_y += 1
				if ((frame_size * pos_y) + cam.position_y > frame_size * nbr_frame_y):
					cam.position_y -= 1
				"""
			
				if (MainPlayer.refresh_count <= 1):
					window.blit(pygame.image.load(MainPlayer.sprite + "/" + MainPlayer.orientation + ".png"), (pos_x + cam.position_x, pos_y + cam.position_y))
					MainPlayer.refresh_count += MainPlayer.refresh_freq
				elif (MainPlayer.refresh_count <= 2):
					window.blit(pygame.image.load(MainPlayer.sprite + "/" + MainPlayer.orientation + "_m1.png"), (pos_x + cam.position_x, pos_y + cam.position_y))
					MainPlayer.refresh_count += MainPlayer.refresh_freq
				elif (MainPlayer.refresh_count <= 3):
					window.blit(pygame.image.load(MainPlayer.sprite + "/" + MainPlayer.orientation + ".png"), (pos_x + cam.position_x, pos_y + cam.position_y))
					MainPlayer.refresh_count += MainPlayer.refresh_freq
				elif (MainPlayer.refresh_count <= 4):
					window.blit(pygame.image.load(MainPlayer.sprite + "/" + MainPlayer.orientation + "_m2.png"), (pos_x + cam.position_x, pos_y + cam.position_y))
					MainPlayer.refresh_count += MainPlayer.refresh_freq
				else:
					MainPlayer.refresh_count = 0
					
				MainPlayer.float_position += 1 * MainPlayer.speed
			else:
				window.blit(pygame.image.load(MainPlayer.sprite + "/" + MainPlayer.orientation + ".png"), (MainPlayer.position_x * 32 + cam.position_x, MainPlayer.position_y * 32 - (64 - MainPlayer.sprite_height) + cam.position_y))

			# Top sprite
			for spri in spriteTopBuffer:
				spri.draw()
				spriteTopBuffer.remove(spri)

			# Last layer (on top)
			for obj in objects_list[len(objects_list) - 1]:
				window.blit(obj.image, (obj.position_x * 32 + cam.position_x, obj.position_y * 32 + cam.position_y))

			# Debug
			if (debug_draw_hitbox == True):
				for x in range(MainPlayer.position_x * frame_size, (MainPlayer.position_x + 1) * frame_size + 1, 4):
					pygame.draw.line(window, (255, 0, 0), (x + cam.position_x, MainPlayer.position_y * frame_size + cam.position_y), (x + cam.position_x, (MainPlayer.position_y + 1) * frame_size + cam.position_y), 1)
				for y in range(MainPlayer.position_y * frame_size, (MainPlayer.position_y + 1) * frame_size + 1, 4):
					pygame.draw.line(window, (255, 0, 0), (MainPlayer.position_x * frame_size + cam.position_x, y + cam.position_y), ((MainPlayer.position_x + 1) * frame_size  + cam.position_x, y + cam.position_y), 1)
			if (debug_draw_frame == True):	
				for x in range(0, nbr_frame_x * frame_size, frame_size):
					pygame.draw.line(window, (255, 255, 255), (x, 0), (x, nbr_frame_y * frame_size), 1)
				for y in range(0, nbr_frame_y * frame_size, frame_size):
					pygame.draw.line(window, (255, 255, 255), (0, y), (nbr_frame_x * frame_size, y), 1)
			if (debug_draw_position == True): #and debug_draw_position_refresh == True):
				myfont = pygame.font.SysFont("Arial", 12)
				debug_to_draw = "PX:" + str(MainPlayer.position_x) + " PY:" + str(MainPlayer.position_y) + "  CX:" + str(cam.position_x) + " CY:" + str(cam.position_y)
				label = myfont.render(debug_to_draw, 1, (255,255,255))
				pygame.draw.rect(window, (0,0,0), pygame.Rect(0, 0, len(debug_to_draw) * 6 + 2, 15))
				window.blit(label, (1, 1))
				debug_draw_position_refresh = False
			
			
			pygame.display.flip()
