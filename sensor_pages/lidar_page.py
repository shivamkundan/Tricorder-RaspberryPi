from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

class LidarSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        self.lat=420
        self.long=420
        self.alt=420
        self.num_sats=420


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'LiDAR', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'Garmin LiDAR Lite V3', DARK_YELLOW,style=0,size=34)

        return self.next_screen_name,self.kwargs
