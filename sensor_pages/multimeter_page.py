from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, LIGHT_GREY, WHITE
from custom_user_events import REQUEST_CURRENT
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams['font.size'] = 10
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

        # --- graphing stuff --- #
        self.rolling_tics=50
        self.curr_array=[]
        self.fig = plt.figure(figsize=[6,1.3])
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.ax.set_frame_on(False)
        self.current_line_surf=pygame.Surface((1,1))


        self.voltage_array=[]
        self.fig2 = plt.figure(figsize=[6,1.3])
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = agg.FigureCanvasAgg(self.fig2)
        self.ax2.set_frame_on(False)
        self.voltage_line_surf=pygame.Surface((1,1))


    def render_current_graph(self):
        self.ax.clear()
        self.ax.cla()
        self.ax.plot(self.curr_array,color='r')
        self.ax.set_ylim(bottom=min(self.curr_array),top=max(self.curr_array))
        self.current_line_surf=plot2img(self.fig,self.ax,self.canvas)

    def render_voltage_graph(self):
        self.ax2.clear()
        self.ax2.cla()
        self.ax2.plot(self.voltage_array,color='g')
        self.ax2.set_ylim(bottom=min(self.voltage_array),top=max(self.voltage_array))
        self.voltage_line_surf=plot2img(self.fig2,self.ax2,self.canvas2)

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        # FONT_FEDERATION.render_to(screen, (150, 67), 'MULTIMETER', ORANGE,style=0,size=40)
        # FONT_FEDERATION.render_to(screen, (150, 117), 'INA290', DARK_YELLOW,style=0,size=34)

        if self.frame_count%self.num_tics:
            self.current,self.voltage,self.power=get_multimeter()

            if len(self.curr_array)>self.rolling_tics:
                self.curr_array=self.curr_array[1:]
                self.voltage_array=self.voltage_array[1:]

            # self.noise_out=get_noise()
            self.curr_array.append(self.current)
            self.voltage_array.append(self.voltage)

            self.render_current_graph()
            self.render_voltage_graph()


        curr_row=80 #220
        # increment_val=30

        FONT_DIN.render_to           (screen, (155,curr_row),  "Current:",           DARK_YELLOW, style=0,size=30)
        # curr_row+=increment_val
        FONT_HELVETICA_NEUE.render_to(screen, (330,curr_row), f"{self.current} mA", WHITE,       style=0,size=35)
        screen.blit(self.current_line_surf, (120,curr_row+40))

        FONT_DIN.render_to           (screen, (200,380),  "Voltage",           DARK_YELLOW, style=0,size=30)
        FONT_HELVETICA_NEUE.render_to(screen, (200,410), f"{self.voltage} mV", WHITE,       style=0,size=26)
        screen.blit(self.voltage_line_surf, (120,450))


        FONT_DIN.render_to           (screen, (200,550),  "Power",             DARK_YELLOW, style=0,size=30)
        FONT_HELVETICA_NEUE.render_to(screen, (200,580), f"{self.power} mW",   WHITE,       style=0,size=26)



        self.frame_count+=1
        return self.next_screen_name,self.kwargs