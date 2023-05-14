'''
This file contains templates for pages.\n
PageTemplate is the base class which handles blitting the home button\n
and other page-specific buttons, mouse/touch handling, enter and exit.
'''

import pygame
from fonts import FONT_FEDERATION
from colors import FONT_BLUE, WHITE
from buttons import ButtonClass,\
					button_selected_3, button_selected_3_blank, top_button_selected, \
					MINI_BUTTONS, MINI_BUTTON_NAMES, \
					PREF_BUTTON, EDIT_BUTTON, PLAY_BUTTON, PAUSE_BUTTON, SCALE_BUTTON, RESET_BUTTON, \
					NAV_BUTTONS, NAV_BUTTONS_VERTICAL, \
					numpad_button, numpad_button_alt
import matplotlib.pyplot as plt
from plotting_functions import bar_plot,pie_plot,line_plot
import matplotlib.backends.backend_agg as agg
import logging
from paths_and_utils import PERIPHERAL_MODE

# ===============================Page Templates======================= #
class PageTemplate():
	'''This is the base class for all pages'''
	def __init__(self,name):
		self.name=name
		self.next_screen_name=self.name
		self.button_list=self.init_home_button()
		self.COOLDOWN=False
		self.button_dict=self.make_dictionary()
		self.basic_buttons=[self.button_dict['home_button'],self.button_dict['top_button']]
		self.kwargs={'prev_page_name':self.name}  #this is sent to other pages
		self.prev_page_name=self.name             # this takes back to prev page

	def init_home_button(self):
		x=ButtonClass(-1,button_selected_3_blank,button_selected_3,2,462,name='home_button')
		y=ButtonClass(-2,button_selected_3_blank,top_button_selected,0,35,name='top_button')
		return [x,y]

	def blit_all_buttons(self,screen):
		for button in self.button_list:
			button.blit_button(screen)

	def blit_basic_buttons(self,screen):
		for button in self.basic_buttons:
			button.blit_button(screen)

	def blit_some_buttons(self,screen,button_list):
		'''Blit only specific buttons'''
		for button in button_list:
			button.blit_button(screen)

	def make_dictionary(self):
		'''A dictionary of all buttons of a page'''
		butt_dict={}
		for button in self.button_list:
			butt_dict[button.name]=button
		return butt_dict

	def kwarg_handler(self,kwargs):
		# print (kwargs.keys())
		if 'prev_page_name' in kwargs.keys():
			pp=kwargs['prev_page_name']
			if pp!=self.name:
				# print ('now: ',self.name)
				# print ('changing kwargs from ',self.kwargs['prev_page_name'], ' to ',pp)
				self.kwargs['prev_page_name']=kwargs['prev_page_name']

	def on_exit(self):
		pass

	def on_enter(self):
		logging.info(f"entering {self.__class__.__name__}")

	def handle_events(self,screen,curr_events):
		'''Handles basic touch/mouse events'''
		for event in curr_events:
			# ---------------------------- Finger / Mouse Events ---------------------------- #
			if (event.type==pygame.FINGERDOWN or event.type==pygame.MOUSEBUTTONDOWN):
				if (event.type == pygame.FINGERDOWN ):
					pos=(int(event.x*screen.get_width()),int(event.y*screen.get_height()))
				else:
					pos=pygame.mouse.get_pos()
				for butt in self.button_list:
					if butt.rectangle.collidepoint(pos) and (butt.cooldown_val==0):
						butt.press()
						butt.cooldown_val=butt.required_cooldown

			if (event.type == pygame.FINGERUP or event.type==pygame.MOUSEBUTTONUP):
				if (event.type == pygame.FINGERUP):
					pos=(int(event.x*screen.get_width()),int(event.y*screen.get_height()))
				else:
					pos=pygame.mouse.get_pos()
				for butt in self.button_list:
					if butt.rectangle.collidepoint(pos) and (butt.cooldown_val>0):
						# print ('release ',str(butt.butt_id))
						butt.release()
						if butt.name=='top_button':
							print (self.name)
							if self.name=='quick_menu_page':
								self.next_screen_name=self.prev_page_name
								self.kwargs['prev_page_name']=self.name
							else:
								self.next_screen_name='quick_menu_page'
								self.kwargs['prev_page_name']=self.name
						if butt.name=='home_button':
							self.next_screen_name=self.prev_page_name
						return butt
				return None

class PageWithoutGauge(PageTemplate):
	'''For more complex pages'''
	def __init__(self,name,color_list=[],names_list=[]):
		'''Constructor'''
		super().__init__(name)
		self.names_list=names_list
		self.color_list=color_list
		self.prev_page_name='menu_home_page'
		self.rolling_tics=30
		self.array_dict={}
		self.bluetooth_connected=False
		self.pause=False
		self.b_names=MINI_BUTTON_NAMES
		self.PERIPHERAL_MODE=PERIPHERAL_MODE

		self.menu_buttons=MINI_BUTTONS
		self.button_list+=self.menu_buttons+ [PREF_BUTTON,EDIT_BUTTON,PLAY_BUTTON,PAUSE_BUTTON,SCALE_BUTTON,RESET_BUTTON]
		self.some_buttons=self.menu_buttons+ [PREF_BUTTON,PLAY_BUTTON,PAUSE_BUTTON,SCALE_BUTTON,RESET_BUTTON]
		self.button_dict=self.make_dictionary()

		PLAY_BUTTON.selected=True
		self.button_dict['bar_chart'].selected=True
		self.prev_subpage_name='info'  #when exiting preferences pane

		rolling_tics=self.rolling_tics
		for curr_name in self.names_list:
			self.array_dict[curr_name]=[-1 for i in range(self.rolling_tics)]
			# print (curr_name,self.array_dict[curr_name])

		self.i=0
		self.x=[i for i in range(-self.rolling_tics,0)]
		self.frame_count=0

		# # ---
		# Plotting stuff
		self.fig = plt.figure(figsize=[5,4])
		self.ax = self.fig.add_subplot(111)
		self.canvas = agg.FigureCanvasAgg(self.fig)

		# ---
		self.fig2 = plt.figure(figsize=(6.4/1.2,4.8/1.2))
		self.ax2 = self.fig2.add_subplot(111)
		self.canvas2 = agg.FigureCanvasAgg(self.fig2)

		# ---
		self.fig3 = plt.figure(figsize=[5,4])
		self.ax3 = self.fig3.add_subplot(111)
		self.canvas3 = agg.FigureCanvasAgg(self.fig3)
		self.ax3.set_frame_on(False)

		# ---
		self.bar_surf=pygame.Surface((1,1))
		self.pie_surf=pygame.Surface((1,1))
		self.line_surf=pygame.Surface((1,1))

	def flip_button(self,pressed_button):
		'''For releasing/unselecting the non-selected buttons'''
		if pressed_button.selected:
			return
		else:
			pressed_button.selected=not pressed_button.selected

		for b_name in self.b_names:
			button= self.button_dict[b_name]
			if button!=pressed_button:
				button.selected=not pressed_button.selected

		if self.button_dict['preferences'].selected:
			self.button_dict['preferences'].selected=False
			self.pause=False

	def next_frame_base(self,screen,curr_events,curr_vals,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		if 'text' in kwargs.keys():
			print ('text: ',kwargs['text'])
			try:
				self.rolling_tics=int(kwargs['text'])
			except ValueError:
				print ('invalid new tics')

		self.blit_some_buttons(screen,self.some_buttons)
		pressed_button=self.handle_events(screen,curr_events)

		# ----- Button handling ----- #
		if pressed_button!=None:
			if pressed_button.name=='preferences':
				if pressed_button.selected:
					pressed_button.selected=False
					self.pause=False
					self.button_dict[self.prev_subpage_name].selected=True
				else:
					pressed_button.selected=True
					self.pause=True
					for item in self.menu_buttons:
						if item.selected:
							self.prev_subpage_name=item.name
						item.selected=False

			if pressed_button.name=='play':
				self.button_dict['play'].selected=True
				self.button_dict['pause'].selected=False
				self.pause=False

			if pressed_button.name=='pause':
				self.button_dict['play'].selected=False
				self.button_dict['pause'].selected=True
				self.pause=True

			if pressed_button.name=='edit' and self.pause:
				self.next_screen_name='numpad_page'
				return self.next_screen_name,{'prev_page_name':self.name}

			if pressed_button.name in self.b_names:
				self.flip_button(pressed_button)

		x_pos=120
		y_pos=375

		# Handle both bluetooth and usb connections
		if (self.bluetooth_connected or self.PERIPHERAL_MODE=='serial'):
			# trim arrays to rolling_tics size
			if self.i>self.rolling_tics:
				self.x=self.x[len(self.x)-self.rolling_tics:]
				for name,_ in self.array_dict.items():
					self.array_dict[name]=self.array_dict[name][len(self.array_dict[name])-self.rolling_tics:]

			try:
				if self.button_dict['bar_chart'].selected:
					if not self.pause: #and self.frame_count%15==0:
						self.bar_surf = bar_plot(self.fig,self.ax,self.canvas,self.names_list,self.color_list,curr_vals)
					screen.blit(self.bar_surf, (120,150))

				elif self.button_dict['pie_chart'].selected:
					# if (self.frame_count%15==0) and (not self.pause):
					if not self.pause:
						self.pie_surf=(pie_plot(self.fig2,self.ax2,self.canvas2,self.color_list,self.names_list,curr_vals)).convert()
					screen.blit(self.pie_surf, (80, 170))

				elif self.button_dict['line_plot'].selected:
					if not self.pause:# and self.frame_count%15==0:
						self.line_surf = line_plot(self.fig3,self.ax3,self.canvas3,self.color_list,self.x,self.array_dict)
					screen.blit(self.line_surf, (120,150))
			except Exception as e:
				raise (e)
				logging.error ('PageWithoutGauge.next_frame_base error:'+str(e))

		else:
				y_pos+=110
				FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'NO BLUETOOTH', WHITE, size=28)
		self.frame_count+=1

class DeviceStatsPageTemplate(PageTemplate):
	'''For viewing RPi stats'''
	def __init__(self,name):
		super().__init__(name)
		self.button_list+=NAV_BUTTONS+NAV_BUTTONS_VERTICAL