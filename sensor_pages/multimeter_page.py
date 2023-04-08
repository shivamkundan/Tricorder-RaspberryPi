from page_templates import PageTemplate
from fonts import FONT_FEDERATION, ORANGE, DARK_YELLOW, LIGHT_GREY, WHITE
from custom_user_events import REQUEST_CURRENT
import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg
from pygame import gfxdraw
import pygame.event as e
# from tricorder import ser
from serial_manager import get_multimeter

class MultimeterPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='MenuHomePage'

        self.selected_font_size=24
        self.selected_font=FONT_FEDERATION
        self.selected_font_color=WHITE

        self.num_tics=3
        self.current=420
        self.voltage=420
        self.power=420

        self.frame_count=0


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Multimeter', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'INA290', DARK_YELLOW,style=0,size=34)

        # if self.frame_count%self.num_tics:
        self.current,self.voltage,self.power=get_multimeter()
        #     e.post(REQUEST_CURRENT)

        self.selected_font.render_to(screen, (200, 320), f"I:{self.current}", self.selected_font_color,style=1,size=self.selected_font_size)
        self.selected_font.render_to(screen, (200, 350), f"V:{self.voltage}", self.selected_font_color,style=1,size=self.selected_font_size)
        self.selected_font.render_to(screen, (200, 380), f"P:{self.power}", self.selected_font_color,style=1,size=self.selected_font_size)

        self.frame_count+=1

        return self.next_screen_name,self.kwargs
