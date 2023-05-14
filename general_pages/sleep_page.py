import pygame as pg
import time
import logging
from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW
from mappings import PIGPIO, MCU_RESET_CODE, MCU_IND_MODE_DISABLE
from paths_and_utils import BACKLIGHT_PIN
from serial_manager import ser, my_flush

class SleepPage(PageTemplate):
	'''A dummy page for low-power sleep mode'''
	def __init__(self,name):
		'''Constructor'''
		super().__init__(name)
		self.event_list=[   pg.FINGERDOWN,
							pg.FINGERMOTION,
							pg.FINGERUP,
							pg.MULTIGESTURE,
							pg.KEYDOWN,
							pg.KEYUP,
							pg.MOUSEBUTTONDOWN,
							# pg.MOUSEMOTION,
							pg.MOUSEBUTTONUP,
							# pg.MOUSEWHEEL,
						]
		self.prev_page_name='menu_home_page'
		self.backlight_restore_level=255		# Set to max PWM value

	def handle_events(self,screen,curr_events):
		for event in curr_events:
			if event.type in self.event_list:
				curr_events.remove(event)
				return True
		return False

	def on_enter(self):
		'''Saves the backlight level before going to sleep. Backlight will be restored to this level at wake up'''
		self.backlight_restore_level=PIGPIO.get_PWM_dutycycle(BACKLIGHT_PIN)

	def wake_from_sleep(self):
		'''Resets backlight level, wakes MCU, flushes serial connection'''
		logging.info("WAKE_FROM_SLEEP")
		PIGPIO.set_PWM_dutycycle(BACKLIGHT_PIN, self.backlight_restore_level)
		ser.write(MCU_RESET_CODE.encode('utf-8'))
		time.sleep(5)
		my_flush()
		ser.write(MCU_IND_MODE_DISABLE.encode('utf-8'))
		ser.flush()

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		if 'prev_page_name' in kwargs.keys():
			self.prev_page_name=kwargs['prev_page_name']

		FONT_FEDERATION.render_to(screen, (150, 67), 'Sleeping...', ORANGE,style=0,size=40)

		time.sleep(1)

		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button==True:
			self.wake_from_sleep()


			self.next_screen_name=self.prev_page_name
			# print ('pressed: sleep->',self.next_screen_name)
			return self.next_screen_name,{}

		return self.next_screen_name,{}
