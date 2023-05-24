'''! @brief Display weight reading from Force Sensitive Resistor (FSR).
@file weight_page.py Contains definition for WeightSensorPage class.
@todo implement this page
'''

from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

class WeightSensorPage(PageTemplate):
    '''! Display weight reading from Force Sensitive Resistor (FSR).'''
    def __init__(self,name):
        '''! Constructor'''
        super().__init__(name)
        self.prev_page_name='menu_home_page'

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Weight', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'Force Sensitive Resistor', DARK_YELLOW,style=0,size=34)

        return self.next_screen_name,self.kwargs
