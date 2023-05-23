'''! For visualizing data from the RTL2832 w/R820T Software Defined Radio (SDR) dongle.
Two modes of visualizing: line plot and waterfall.
Reverse-engineered from Adafruit's FreqShow project.
@file sdr_page.py Contains definition for SoftwareDefinedRadioPage class.
'''

import pygame
from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE
from buttons import NAV_BUTTONS, BLANK_BTN, NUMPAD_BTN

# -------------- Freqshow code -------------- #
import controller
import model
import ui
import logging

## Starting frequency
INIT_FREQ=433.0
## Leave some top & bottom border for text and buttons
WIN_SIZE=(680,720)

class SoftwareDefinedRadioPage(PageTemplate):
	'''! For visualizing data from RTL2832 SDR dongle'''
	def __init__(self,name):
		super().__init__(name)
		## Next page name
		self.next_screen_name=self.name
		## Return page name
		self.prev_page_name='menu_home_page'
		## List of navigation buttons
		self.button_list+=NAV_BUTTONS
		## List of all buttons for this page
		self.button_list+=[BLANK_BTN,NUMPAD_BTN]
		## Starting frequency
		self.init_freq=INIT_FREQ
		## Main model
		fsc,self.fsmodel=self.init_sdr()
		## Main controller
		self.fscontroller=fsc
		try:
			self.fsmodel.set_center_freq(self.init_freq)
		except:
			logging.error ('could not set freq')

	def init_sdr(self):
		'''! Initialize the RTL2832 SDR lib'''
		try:
			fsmodel = model.FreqShowModel(WIN_SIZE[0],WIN_SIZE[1])
			fscontroller = controller.FreqShowController(fsmodel)
		except Exception as e:
			logging.error ('SDR not connected')
			fsmodel=None
			fscontroller =None

		return fscontroller, fsmodel

	def set_freq_manual(self,new_freq):
		'''! Manually set a specific frequency'''
		try:
			# For some reason it is off by 1.2MHz
			self.fsmodel.set_center_freq(float(new_freq)+1.2)
		except ValueError:
			logging.error(f"error tried to set: {new_freq}")

	def blit_title(self,screen):
		'''! Display page title'''
		FONT_FEDERATION.render_to(screen, (150, 67), 'Software Defined Radio', ORANGE,style=0,size=34)
		FONT_FEDERATION.render_to(screen, (150, 67+34+10), '24 - 1766 MHz', ORANGE,style=0,size=26)

	def next_frame(self,screen,curr_events,**kwargs):

		if ("text" in kwargs.keys()):
			print (kwargs)
			self.set_freq_manual(kwargs["text"])

		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:
			if pressed_button.name=='blank':
				self.fscontroller.toggle_main()
			if pressed_button.name=='numpad':
				self.next_screen_name='numpad_page'
				self.kwargs['prev_page_name']=self.name

		if self.fscontroller==None:
			self.init_sdr()

		if self.fscontroller!=None:
			self.fscontroller.current().render(screen)

		self.blit_title(screen)


		return self.next_screen_name,self.kwargs