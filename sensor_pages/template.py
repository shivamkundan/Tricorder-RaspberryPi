from page_templates import PageTemplate
from fonts import FONT_FEDERATION, ORANGE, DARK_YELLOW

class TemplatePage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='mobile_home_page_1'


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Template', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'page', DARK_YELLOW,style=0,size=34)

        return self.next_screen_name,self.kwargs