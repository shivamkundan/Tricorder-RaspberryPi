import pygame
from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE
from buttons import NAV_BUTTONS, BLANK_BTN, BLANK_SQUARE_BTN

# -------------- Freqshow code -------------- #
import controller
import model
import ui
import logging

INIT_FREQ=433.0
WIN_SIZE=(680,720)

class SoftwareDefinedRadioPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.prev_page_name='menu_home_page'

		self.button_list+=NAV_BUTTONS
		self.button_list+=[BLANK_BTN,BLANK_SQUARE_BTN]
		self.init_freq=INIT_FREQ
		self.fscontroller,self.fsmodel=self.init_sdr()

		try:
			self.fsmodel.set_center_freq(self.init_freq)
		except:
			logging.error ('could not set freq')


	def init_sdr(self):
		try:
			fsmodel = model.FreqShowModel(WIN_SIZE[0],WIN_SIZE[1])
			fscontroller = controller.FreqShowController(fsmodel)
		except Exception as e:
			logging.error ('SDR not connected')
			fsmodel=None
			fscontroller =None

		return fscontroller, fsmodel



	def next_frame(self,screen,curr_events,**kwargs):

		if ("text" in kwargs.keys()):
			print (kwargs)
			self.fsmodel.set_center_freq(float(kwargs["text"])+1.2)  # For some reason it is off by 1.2MHz

		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)

		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:
			if pressed_button.name=='blank':
				self.fscontroller.toggle_main()
		if pressed_button!=None:
			if pressed_button.name=='blank_square':
				self.next_screen_name='numpad_page'
				self.kwargs['prev_page_name']=self.name

		if self.fscontroller==None:
			self.init_sdr()

		if self.fscontroller!=None:
			for event in pygame.event.get():

				if (event.type == pygame.FINGERUP or event.type==pygame.MOUSEBUTTONUP):
					if (event.type == pygame.FINGERUP):
						mouse_pos=(int(event.x*screen.get_width()),int(event.y*screen.get_height()))
					else:
						mouse_pos=pygame.mouse.get_pos()
					self.fscontroller.current().click(mouse_pos)
			self.fscontroller.current().render(screen)



		FONT_FEDERATION.render_to(screen, (150, 67), 'Software Defined Radio', ORANGE,style=0,size=34)
		FONT_FEDERATION.render_to(screen, (150, 67+34+10), '24 - 1766 MHz', ORANGE,style=0,size=26)
		# FONT_FEDERATION.render_to(screen, (150, 67+34+10), 'SDR RTL2832 w/R820T', ORANGE,style=0,size=40)


		return self.next_screen_name,self.kwargs