from page_templates import PageTemplate
from buttons import QUICK_MENU_BUTTONS
from fonts import FONT_FEDERATION
from colors import ORANGE
from custom_user_events import TOGGLE_SCREEN,GO_TO_SLEEP,SCREENSHOT_EVENT,SET_BACKLIGHT
from pygame import event as ev

class QuickMenuPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.butt_list=QUICK_MENU_BUTTONS
		self.button_list+=self.butt_list
		self.prev_page_name=self.name
		self.backlight_lvl=-1
		self.fullscreen_en=False

		self.screen_dict={'backlight':'brightness_slider_page','device_stats':'device_stats_page',
							'home':'home_page','exit':'exit',
							'sleep':'sleep_page','screenshot':self.prev_page_name,
							'exit_fullscreen':self.prev_page_name,
							'fullscreen':self.prev_page_name
							}
		self.event_dict={'exit_fullscreen':TOGGLE_SCREEN,'fullscreen':TOGGLE_SCREEN,
						 'sleep':GO_TO_SLEEP,'screenshot':SCREENSHOT_EVENT}

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		if 'prev_page_name' in kwargs:
			self.prev_page_name=kwargs['prev_page_name']

		self.blit_basic_buttons(screen)
		self.blit_some_buttons(screen,self.butt_list)

		FONT_FEDERATION.render_to(screen, (534, 140),f'{self.backlight_lvl}' , ORANGE,style=1,size=36)

		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button!=None:
			if pressed_button.name in self.screen_dict.keys():
				self.next_screen_name=self.screen_dict[pressed_button.name]

			if pressed_button.name=='screenshot':
				ev.post(SCREENSHOT_EVENT)
				self.next_screen_name=self.prev_page_name
				return self.next_screen_name,{}

			if pressed_button.name=='fullscreen':
				ev.post(TOGGLE_SCREEN)
				self.next_screen_name=self.prev_page_name
				return self.next_screen_name,{}

			elif pressed_button.name in self.event_dict.keys():
				E=self.event_dict[pressed_button.name]
				ev.post(E)

		ev.post(SET_BACKLIGHT)
		return self.next_screen_name,{}