'''! @brief Display TVOC and eCO2 readings from SGP30 sensor.
@file voc_page.py Contains definition for VOCSensorPage class.
@bug fix on ESP32 end
@todo fix sensor read
'''

import pygame.event as e
from buttons import ButtonClass
from aa_arc_gauge import AA_Gauge
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE, FONT_DIN
from colors import DARK_GREY, ORANGE, SLATE, DARK_YELLOW, WHITE,GREEN
from page_templates import PageTemplate
from serial_manager import get_tvoc_eco2

class VOCSensorPage(PageTemplate):
    '''! Display TVOC and eCO2 readings from SGP30 sensor.'''
    def __init__(self,name):
        '''! Constructor'''
        super().__init__(name)
        self.prev_page_name='menu_home_page'
        self.bluetooth_connected=False
        self.init_gauges()

        self.eCO2='-2'
        self.TVOC='-2'
        self.baseline_eCO2='-2'
        self.baseline_TVOC='-2'
        self.send_code=''

    def blit_title(self,screen):
        '''! Display title'''
        FONT_FEDERATION.render_to(screen, (150, 67), 'VOC/eCO2 Sensor', ORANGE,style=0,size=44)
        FONT_FEDERATION.render_to(screen, (150, 117), 'SGP30', DARK_YELLOW,style=0,size=34)

    def init_gauges(self):
        '''! Init gauges for this page.'''
        self.gauge_radius=100
        gauges_spacing=48
        weight=8
        arc_h=165
        font=FONT_HELVETICA_NEUE
        f_color=WHITE
        main_font_size=60
        curr_col=250-self.gauge_radius
        self.tvoc_gauge_origin=(curr_col,arc_h)
        self.tvoc_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=1000,origin=self.tvoc_gauge_origin, radius=self.gauge_radius,weight=weight,color=GREEN,suffix='ppb',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='TVOC',title_font_size=20)

        self.eco2_gauge_origin=(curr_col+(2.5*self.gauge_radius)+gauges_spacing,arc_h)
        self.eco2_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=1000,origin=self.eco2_gauge_origin, radius=self.gauge_radius,weight=weight,color=GREEN,suffix='ppm',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='CO2',title_font_size=20)

    def blit_current_settings(self,screen):
        '''! Show settings for SGP30 sensor.'''
        x_pos=138
        y_pos=440
        FONT_FEDERATION.render_to(screen, (256, y_pos),'BASELINE ', ORANGE, size=28,style=1)
        y_pos+=60
        FONT_DIN.render_to(screen, (x_pos, y_pos),'TVOC: ', ORANGE, size=28)
        y_pos+=35
        FONT_DIN.render_to(screen, (x_pos+20, y_pos),str(self.baseline_TVOC), SLATE, size=34)
        y_pos=440+60
        x_pos=440
        FONT_DIN.render_to(screen, (x_pos, y_pos),'eCO2: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),str(self.baseline_eCO2), SLATE, size=34)

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name

        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)

        self.blit_title(screen)

        pressed_button=self.handle_events(screen,curr_events)

        self.eCO2,self.TVOC,self.baseline_eCO2,self.baseline_TVOC=get_tvoc_eco2()

        self.blit_current_settings(screen)
        # if (self.bluetooth_connected):
            # print ('updating tvoc/eco2')
        tvoc_gauge_img=self.eco2_gauge.blit_gauge(self.eCO2)
        eco2Gauge_img=self.tvoc_gauge.blit_gauge(self.TVOC)
        tvoc_gauge_img.set_colorkey((0,0,0))
        eco2Gauge_img.set_colorkey((0,0,0))
        screen.blit(eco2Gauge_img,self.eco2_gauge_origin)
        screen.blit(tvoc_gauge_img,self.tvoc_gauge_origin)

        return self.next_screen_name,self.kwargs
