'''
Implements a generic number pad for other pages, returns text in kwargs
'''

import pygame
from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import FONT_BLUE, WHITE
from buttons import ButtonClass, numpad_button, numpad_button_alt

class NumPadPage(PageTemplate):
	'''Implements a generic number pad for other pages, returns text in kwargs'''
	def __init__(self,name):
		super().__init__(name)
		self.button_list+=self.init_buttons()
		self.curr_text=''
		self.button_text=['1','2','3','4','5','6','7','8','9','E','0','<']
		self.prev_page_name=self.name

	def init_buttons(self):
		width=170
		height=100
		x_start=150
		y_pos=260
		x_spacing=width+5
		y_spacing=height+5

		button_list=[]
		i=1
		for col in range(1,4+1):
			x_pos=x_start
			for row in range(1,3+1):
				button_list.append(ButtonClass(i,numpad_button,numpad_button_alt,x_pos,y_pos,name=str(i)))
				i+=1
				x_pos+=x_spacing
			y_pos+=y_spacing

		return button_list

	def blit_numpad_buttons(self,screen):
		'''Blits simple buttons overlayed with numbers'''
		x_spacing=170
		y_spacing=101
		x_start=225
		y_pos=300
		i=0
		for col in range(1,4+1):
			x_pos=x_start
			for row in range(1,3+1):
				FONT_FEDERATION.render_to(screen, (x_pos, y_pos), self.button_text[i], FONT_BLUE,style=1,size=40)
				x_pos+=x_spacing
				i+=1
			y_pos+=y_spacing

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		if 'prev_page_name' in kwargs.keys():
			self.prev_page_name=kwargs['prev_page_name']

		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		self.blit_numpad_buttons(screen)

		if pressed_button!=None:

			# This is the return button
			if pressed_button.butt_id==10:
				self.next_screen_name=self.prev_page_name
				out=self.curr_text
				self.curr_text=''
				return self.next_screen_name,{'text':out}

			# Print numbers on plain buttons
			for butt in range(1,9+1):
				if pressed_button.butt_id==butt:
					self.curr_text+=str(butt)

			# Button for 0
			if pressed_button.butt_id==11:
				self.curr_text+='0'

			# This is for delete key
			elif pressed_button.butt_id==12:
				l=len(self.curr_text)
				self.curr_text=self.curr_text[0:l-1]

		# Blit current value
		FONT_FEDERATION.render_to(screen, (200, 100), self.curr_text, WHITE,style=1,size=48)

		return self.next_screen_name,{"curr_text":self.curr_text}