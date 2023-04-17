from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg

import pandas as pd
import logging

BATT_HIST_FILE="batt_history.csv"

class BatterySensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'
        self.fig = plt.figure(figsize=[5,4])
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.ax.set_frame_on(False)
        self.line_surf=pygame.Surface((1,1))

    def on_enter(self):
        logging.info(f"entering {self.__class__.__name__}")
        self.make_plot()

    def make_plot(self):
        df = pd.read_csv(BATT_HIST_FILE)#, usecols=columns)

        batt_voltage=df.iloc[:, 2]
        times=df.iloc[:, 1]

        self.ax.clear()
        self.ax.cla()
        self.ax.plot(batt_voltage,color='g')
        self.ax.set_xticklabels(times)
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        self.ax.set_ylim(bottom=3.7,top=4.3)
        self.line_surf=plot2img(self.fig,self.ax,self.canvas)







    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Battery', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'LC709203', DARK_YELLOW,style=0,size=34)

        screen.blit(self.line_surf, (120,150))

        return self.next_screen_name,self.kwargs
