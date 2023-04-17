from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg

class BatterySensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Battery', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'LC709203', DARK_YELLOW,style=0,size=34)

        return self.next_screen_name,self.kwargs
