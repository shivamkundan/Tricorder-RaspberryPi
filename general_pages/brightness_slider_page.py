'''
Implements functions for backlight control.

:note:
	The project uses a Pimoroni Hyperpixel Square. The brightness is controlled through PWM.

.. note::The project uses a Pimoroni Hyperpixel Square. The brightness is controlled through PWM.
'''

'''! @brief Display backlight brightness adjustment.
@file brightness_slider_page.py Contains definitions for SliderClass and BrightnessSliderPage classes.
'''

import pygame
import math
from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN
from colors import WHITE, DARK_YELLOW, LIGHT_BLUE
from paths_and_utils import BACKLIGHT_PIN
from mappings import PIGPIO
from custom_user_events import SET_BACKLIGHT

class SliderClass():
	'''! A class for implementing slide switches'''
	def __init__(self,start_x,y_pos,button_width,button_height,length=100,min_val=0,max_val=249,start_val=None):
		'''! Constructor'''
		self.start_x=start_x
		self.y_pos=y_pos
		self.length=length
		self.end_x=self.start_x+self.length

		self.button_width=button_width
		self.button_height=button_height
		self.button_surf, self.rectangle=self.initialize_button()

		if start_val!=None:
			self.rectangle.left=self.start_x+start_val-self.button_width//2
		else:
			self.rectangle.left=self.start_x+self.length//2-self.button_width//2
		self.rectangle.top=self.y_pos-self.button_height//2

		self.button_width_half=self.button_width//2

		self.linewidth=5
		padding_x=10
		padding_y=self.button_height
		mid=self.button_height//2
		self.line_rectangle=pygame.Rect(self.start_x-padding_x,self.y_pos-mid-padding_y//2, self.length+padding_x,self.linewidth+mid+padding_y)

		self.min_val=min_val
		self.max_val=max_val

		self.in_min=self.start_x-self.button_width_half
		self.in_max=self.start_x+self.length-self.button_width_half

	def initialize_button(self):
		'''! Initialize the slider control button'''
		# Button image
		w,h=self.button_width, self.button_height
		button_surf=pygame.Surface((w,h))
		r=pygame.Rect(0,0,w,h)
		pygame.draw.rect(button_surf,LIGHT_BLUE,r)
		rectangle=button_surf.get_rect()

		return (button_surf, rectangle)

	def blit_slider(self,screen,dx,scale=1):
		'''! Blit slider to screen'''
		if 0<abs(dx)<200*scale:
			dx*=scale

			if self.start_x-self.button_width_half<=(self.rectangle.left+self.button_width_half+dx)<self.end_x+self.button_width_half-1:
				# print ('yes2 ',dx)
				self.rectangle.left+=dx

		# Blit the line
		lin=pygame.draw.line(screen, DARK_YELLOW, (self.start_x,self.y_pos), (self.end_x,self.y_pos), width=self.linewidth)

		# Blit the button
		screen.blit(self.button_surf,(self.rectangle.left,self.rectangle.top))

	def compute_percentage(self):
		'''! Convert from slider length/pos to percentage'''
		pct=(((self.rectangle.left+self.button_width_half)-self.start_x)/self.length)

		if pct<0:
			pct=0
		if pct>0.99:
			pct=1
		num_val=int(round(pct*255,0))
		pct*=100
		if pct==0:
			log_val=0
		else:
			log_val=int(round(math.log(pct),0))

		return round(pct,2),num_val,log_val

	def map(self,x):
		'''! Standard range mapping function to map slider length/pos to backlight value.'''
		out_min=self.min_val
		out_max=self.max_val
		in_min=self.in_min
		in_max=self.in_max
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class BrightnessSliderPage(PageTemplate):
	'''! This page used for adjustubg screen brightness (i.e. backlight level) through pigpio commands'''
	def __init__(self,name):
		super().__init__(name)

		self.button_dict=self.make_dictionary()
		self.prev_x,self.prev_y=pygame.mouse.get_pos()
		self.limit_low=0
		self.limit_high=255
		self.length=400
		self.x_pos=200
		self.end_pos=self.x_pos+self.length
		self.prev_page_name='menu_home_page'

		self.slider=SliderClass(200,290,20,50,length=320,min_val=7,max_val=250,start_val=200)
		# def __init__(self,start_x,y_pos,button_width,button_height,length=100,min_val=0,max_val=250,start_val=None):
		self.PIN_NUM=BACKLIGHT_PIN
		# self.gpio = pigpio.pi()
		self.gpio = PIGPIO

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		self.kwarg_handler(kwargs)

		self.transition_events(screen,curr_events)

		self.blit_all_buttons(screen)

		x=self.slider.rectangle.left
		y=self.slider.rectangle.top

		pos_string=f"(x,y): {x},{y}"

		FONT_DIN.render_to(screen, (300, 67),pos_string , WHITE,style=0,size=40)

		pressed_button=self.handle_events(screen,curr_events)

		pct,num_val,log_val=self.slider.compute_percentage()

		mp=math.ceil(self.slider.map(self.slider.rectangle.left))

		# ---- Set brightness --- #
		if 63<mp<=255:
			self.set_brightness(mp)
		# print (mp)
		if mp<256:
			self.gpio.set_PWM_dutycycle(BACKLIGHT_PIN, mp)  #0-255, so 64 is 1/4 duty cycle

		FONT_DIN.render_to(screen, (200, 200),f'{pct}% {num_val} /255]'  , WHITE,style=0,size=40)
		FONT_DIN.render_to(screen, (200, 360),f'{self.get_current_brightness()}'  , WHITE,style=0,size=40)
		FONT_DIN.render_to(screen, (200, 420),f'{mp}' , WHITE,style=0,size=40)

		pygame.event.post(SET_BACKLIGHT)

		return self.next_screen_name,self.kwargs

	def transition_events(self,screen,curr_events):
		'''! To handle sliding on slider.'''
		dx=0
		scale=1
		for event in curr_events:

				if (event.type==pygame.MOUSEBUTTONDOWN ):
					curr_x,curr_y=pygame.mouse.get_pos()
					if self.slider.line_rectangle.collidepoint(curr_x,curr_y):
						self.slider.rectangle.left=curr_x-self.slider.button_width//2

				# Dragging with mouse
				if (event.type==pygame.MOUSEMOTION ):
					curr_x,curr_y=pygame.mouse.get_pos()
					if self.slider.line_rectangle.collidepoint(curr_x,curr_y):
						if pygame.mouse.get_pressed()[0]==True:
							dx=event.rel[0]
							scale=5
							# print('collide mouse: ',curr_x,' ',curr_y)

				elif event.type==pygame.FINGERMOTION:
					curr_x,curr_y=event.x*screen.get_width(),event.y*screen.get_height()
					print('collide finger: ',curr_x,' ',curr_y)
					print (self.slider.line_rectangle.collidepoint(int(curr_x),int(curr_y)))

					# dx=curr_x-self.prev_x
					dx=curr_x-self.prev_x
					print ('finger dx: ',dx)
					self.prev_x=curr_x
					self.prev_y=curr_y

		self.slider.blit_slider(screen,dx,scale)

	def get_current_brightness(self):
		'''! Retrieve current backlight level'''
		x=self.gpio.get_PWM_dutycycle(self.PIN_NUM)
		return x

	def set_brightness(self,curr):
		'''! Set backlight level'''
		# self.print_current_brightness(self.gpio)
		self.gpio.set_PWM_dutycycle(self.PIN_NUM, int(curr))  #0-255, so 64 is 1/4 duty cycle
		# self.print_current_brightness(self.gpio)
		pygame.event.post(SET_BACKLIGHT)

	# ==================================================================== #
