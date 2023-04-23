from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW


class DeveloperPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.prev_page_name="menu_home_page"

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		pressed_button=self.handle_events(screen,curr_events)


		FONT_FEDERATION.render_to(screen, (150, 67), 'Developer', ORANGE,style=0,size=40)
		return self.next_screen_name,{}
