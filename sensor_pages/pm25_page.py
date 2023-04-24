from fonts import FONT_FEDERATION, FONT_DIN, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, WHITE
from page_templates import PageWithoutGauge
from global_functions import get_text_dimensions
import pygame.event as e
from math import log
from serial_manager import get_pm25,set_pm25_power_off,set_pm25_power_on
import logging

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.backends.backend_agg as agg
mpl.use("Agg")
mpl.rcParams['font.size'] = 10
COLOR = (0.75,0.75,0.75)
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
from plotting_functions import *


class PM25Page(PageWithoutGauge):
    def __init__(self,name):
        self.aqdata=[1, 1, 1, 1, 1, 1]
        names_list=['>0.3μm','>0.5μm','>1.0μm','>2.5μm','>5.0μm','>10μm']
        color_list=['#471337','#b13254','#ff5349','#ff7249','#ff9248','orange']
        # self.aqdata=[0,0,0,0,0,0]

        super().__init__(name,color_list,names_list)
        self.aqdata=[1, 1, 1, 1, 1, 1]
        self.bluetooth_connected=False
        # self.names_list=['>0.3μm','>0.5μm','>1.0μm','>2.5μm','>5.0μm','>10μm']

    def blit_title(self,screen):
        FONT_FEDERATION.render_to(screen, (150, 67), 'Particulate Matter', ORANGE,style=0,size=44)
        FONT_FEDERATION.render_to(screen, (150, 117), 'PMSA003I', DARK_YELLOW,style=0,size=34)

    def info_subpage(self,screen,curr_vals):
        col1=170
        col2=265
        row=200
        y_spacing=20

        if len(curr_vals)>0:
            uuu=0
            for name,val in zip(reversed(self.names_list),reversed(curr_vals)):

                if uuu==4:
                    row=200
                    col1=col1+240
                    col2=col2+240

                txt_surf,w,h1=get_text_dimensions(text=name+':',font_style=FONT_HELVETICA_NEUE,font_color=ORANGE,style=1,font_size=26)
                screen.blit(txt_surf,(col1,row))
                row+=h1+y_spacing

                txt_surf,w,h2=get_text_dimensions(text=f'{int(val):,}',font_style=FONT_HELVETICA_NEUE,font_color=WHITE,style=0,font_size=30)
                screen.blit(txt_surf,(col2,row))
                row+=h2+1.4*y_spacing

                uuu+=1

    def on_exit(self):
        set_pm25_power_off()

    def on_enter(self):
        logging.info(f"entering {self.__class__.__name__}")
        set_pm25_power_on()

    def next_frame(self,screen,curr_events,**kwargs):


        if self.frame_count%5==0:
            self.aqdata=get_pm25()
            # print (x)
            # self.i+=1
            # self.x.append(self.i)
            # channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
            # for color_name,channel in zip(self.names_list,channels):
            #     val=x[channel]
            #     self.array_dict[color_name].append(int(float(val)))

        curr_vals=[]
        aqd=[]
        for val in self.aqdata:
            try:
                val=int(val)
                aqd.append(val)
                if val!=0:
                    log_val=int(round(log(val),0))
                    curr_vals.append(log_val)
                else:
                    curr_vals.append(0)
            except ValueError:
                print ('err val: ',val)

        self.next_frame_base(screen,curr_events,curr_vals,**kwargs)

        FONT_DIN.render_to(screen, (370, 117), str(self.i), WHITE,style=0,size=26)
        FONT_DIN.render_to(screen, (430, 117), str(self.frame_count), WHITE,style=0,size=26)
        FONT_DIN.render_to(screen, (430, 137), f'total: {sum(aqd):,}', WHITE,style=0,size=26)

        y_pos=525
        x_pos=138
        FONT_DIN.render_to(screen, (x_pos,y_pos+30),str(self.aqdata), WHITE, size=24)

        self.blit_title(screen)

        if self.button_dict['info'].selected:
            if (self.frame_count%5==0) and (not self.pause):
                e.post(self.EVENT)
            self.info_subpage(screen,aqd)

        return self.next_screen_name,self.kwargs
