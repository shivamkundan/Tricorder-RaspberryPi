from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, LIGHT_GREY, WHITE
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
        self.prev_page_name='menu_home_page'
        self.num_tics=3
        self.current=-1
        self.voltage=-1
        self.power=-1

        self.frame_count=0


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'MULTIMETER', ORANGE,style=0,size=50)
        FONT_FEDERATION.render_to(screen, (150, 117), 'INA290', DARK_YELLOW,style=0,size=34)

        # if self.frame_count%self.num_tics:
        self.current,self.voltage,self.power=get_multimeter()
        #     e.post(REQUEST_CURRENT)

        FONT_DIN.render_to           (screen, (200,220),  "Current",           DARK_YELLOW, style=0,size=30)
        FONT_HELVETICA_NEUE.render_to(screen, (200,250), f"{self.current} mA", WHITE,       style=0,size=26)

        FONT_DIN.render_to           (screen, (200,380),  "Voltage",           DARK_YELLOW, style=0,size=30)
        FONT_HELVETICA_NEUE.render_to(screen, (200,410), f"{self.voltage} mV", WHITE,       style=0,size=26)

        FONT_DIN.render_to           (screen, (200,550),  "Power",             DARK_YELLOW, style=0,size=30)
        FONT_HELVETICA_NEUE.render_to(screen, (200,580), f"{self.power} mW",   WHITE,       style=0,size=26)

        self.frame_count+=1
        return self.next_screen_name,self.kwargs