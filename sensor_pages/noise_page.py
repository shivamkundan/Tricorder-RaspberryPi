# from page_templates import PageTemplate
# from fonts import FONT_FEDERATION, ORANGE, DARK_YELLOW

# class NoiseSensorPage(PageTemplate):
#     def __init__(self,name):
#         super().__init__(name)
#         self.prev_page_name='MenuHomePage'

#     def next_frame(self,screen,curr_events,**kwargs):
#         self.next_screen_name=self.name
#         self.kwarg_handler(kwargs)
#         self.blit_all_buttons(screen)
#         pressed_button=self.handle_events(screen,curr_events)

#         FONT_FEDERATION.render_to(screen, (150, 67), 'Electret Mic', ORANGE,style=0,size=40)
#         FONT_FEDERATION.render_to(screen, (150, 117), 'PCF8591 <- mic', DARK_YELLOW,style=0,size=34)

#         return self.next_screen_name,self.kwargs

from page_templates import PageTemplate
from fonts import FONT_FEDERATION, ORANGE, DARK_YELLOW
import pygame.event as e
from custom_user_events import REQUEST_NOISE
import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg
from pygame import gfxdraw
from serial_manager import get_noise

import numpy as np

class NoiseSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='MenuHomePage'
        self.noise_out=0
        self.frame_count=0
        self.color_list=['noise']
        self.color_labels=['noise']


        self.rolling_tics=50
        self.x=[]

        # ---
        self.fig = plt.figure(figsize=[5,4])
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.ax.set_frame_on(False)
        self.line_surf=pygame.Surface((1,1))

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)


        FONT_FEDERATION.render_to(screen, (150, 67), 'Noise', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), (str(self.noise_out)), DARK_YELLOW,style=0,size=34)


        if (self.frame_count%3==0):

            if len(self.x)>self.rolling_tics:
                self.x=self.x[1:]

            # if self.frame_count%5==0:
            # e.post(REQUEST_NOISE)
            self.noise_out=get_noise()
            self.x.append(self.noise_out)
            # self.line_surf = line_plot(self.fig3,self.ax3,self.canvas3,self.color_list,self.x,self.array_dict)

            self.ax.clear()
            self.ax.cla()
            self.ax.plot(self.x,color='r')
            self.ax.set_ylim(bottom=min(self.x),top=max(self.x))
            self.line_surf=plot2img(self.fig,self.ax,self.canvas)


        screen.blit(self.line_surf, (120,150))

        self.frame_count+=1

        return self.next_screen_name,self.kwargs
