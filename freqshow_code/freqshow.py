#!/usr/bin/python3

# FreqShow main application and configuration.
# Author: Tony DiCola (tony@tonydicola.com)
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import time

import pygame

import controller
import model
import ui


# Application configuration.
## Number of samples to grab from the radio.
SDR_SAMPLE_SIZE = 1024	# Number of samples to grab from the radio.  Should be
						# larger than the maximum display width.

# Font size configuration.
MAIN_FONT = 33
NUM_FONT  = 50

# Color configuration (RGB tuples, 0 to 255).
MAIN_BG        = (  0,   0,   0) # Black
INPUT_BG       = ( 60, 255, 255) # Cyan-ish
INPUT_FG       = (  0,   0,   0) # Black
CANCEL_BG      = (128,  45,  45) # Dark red
ACCEPT_BG      = ( 45, 128,  45) # Dark green
BUTTON_BG      = ( 60,  60,  60) # Dark gray
BUTTON_FG      = (255, 255, 255) # White
BUTTON_BORDER  = (200, 200, 200) # White/light gray
INSTANT_LINE   = (  0, 255, 128) # Bright yellow green.
# INSTANT_LINE   = (178, 107, 0) #orange

# Define gradient of colors for the waterfall graph.  Gradient goes from blue to
# yellow to cyan to red.
WATERFALL_GRAD = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]

# Configure default UI and button values.
ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color     = BUTTON_FG
ui.Button.bg_color     = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px   = 2
ui.Button.border_px    = 2



# 24 - 1766 MHz



if __name__ == '__main__':

	pygame.display.init()
	pygame.font.init()
	pygame.mouse.set_visible(True)

	size=(720,680)
	screen=pygame.display.set_mode(size, pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT)
	pygame.mouse.set_cursor(*pygame.cursors.tri_left)

	print((pygame.display.get_window_size()))
	
	# Create model and controller.
	fsmodel = model.FreqShowModel(size[0], size[1])
	fscontroller = controller.FreqShowController(fsmodel)

	# Main loop to process events and render current view.
	lastclick = 0
	while True:
		# Process any events (only mouse events for now).
		for event in pygame.event.get():
			# if event.type==pygame.VIDEOEXPOSE:
			# 	break
			# if event.type==pygame.MOUSEMOTION:
			# 	break
			# if event.type==pygame.WINDOWEVENT:
			# 	break


			if (event.type == pygame.FINGERUP or event.type==pygame.MOUSEBUTTONUP):
				if (event.type == pygame.FINGERUP):
					mouse_pos=(int(event.x*screen.get_width()),int(event.y*screen.get_height()))
				else:
					mouse_pos=pygame.mouse.get_pos()
				fscontroller.current().click(mouse_pos)
			#
			if event.type == pygame.KEYUP:
				if (event.key == pygame.K_ESCAPE or event.key==ord('q')):
					exit()
			if event.type == pygame.QUIT:
				exit()
		# Update and render the current view.
		fscontroller.current().render(screen)
		pygame.display.update()