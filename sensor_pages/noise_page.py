from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg

from serial_manager import get_noise

class NoiseSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'
        self.noise_out=0
        self.frame_count=0

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

            self.noise_out=get_noise()
            self.x.append(self.noise_out)

            self.ax.clear()
            self.ax.cla()
            self.ax.plot(self.x,color='r')
            self.ax.set_ylim(bottom=min(self.x),top=max(self.x))
            self.line_surf=plot2img(self.fig,self.ax,self.canvas)


        screen.blit(self.line_surf, (120,150))

        self.frame_count+=1

        return self.next_screen_name,self.kwargs
