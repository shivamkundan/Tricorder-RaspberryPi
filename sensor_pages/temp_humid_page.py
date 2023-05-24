'''!
@brief Display temperature and relative humidity readings from HTU31D sensor.
@file temp_humid_page.py Contains definition for TempHumidPage class.
'''

import pygame.event as e
import logging
from buttons import ButtonClass, slide_switch_blank,simple_button_short,simple_button_short_alt
from aa_arc_gauge import AA_Gauge
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE, FONT_DIN
from colors import SLATE, ORANGE, WHITE, DARK_GREY, DARK_YELLOW, YELLOW
from page_templates import PageTemplate

import time
from serial_manager import get_temp_humid, ser

class TempHumidPage(PageTemplate):
    '''! Display temperature and relative humidity readings from HTU31D sensor.'''
    def __init__(self,name):
        '''! Constructor'''
        super().__init__(name)
        self.prev_page_name='menu_home_page'
        self.bluetooth_connected=False
        self.c_temp=-1
        self.humid=-1
        self.heater='False'
        self.t_res='-1'
        self.h_res='-1'
        self.send_val=''
        self.frame_count=0
        self.num_tics=10
        self.init_gauges()

        self.humidity_resolution_list=["0.020%","0.014%","0.010%","0.007%"]
        self.temp_resolution_list=["0.040","0.025","0.016","0.012"]

        self.menu_title_buttons, self.menu_buttons, settings_button=self.init_buttons()
        self.button_list+=self.menu_title_buttons+ self.menu_buttons+ [settings_button]

        self.button_dict=self.make_dictionary()
        self.basic_buttons.append(settings_button)
        self.button_dict['temperature'].selected=True
        self.show_menu=False

    
    def init_buttons(self):
        '''! Init buttons for this page.'''
        menu_title_buttons=[]
        menu_buttons=[]

        button_w=165 #short button
        x_spacing=button_w+20
        button_h=83
        row,col=360,150

        f_size=26

        menu_title_buttons.append(ButtonClass(3,slide_switch_blank,slide_switch_blank,col,row,text='Temperature',font_size=30,style=0,font_color=DARK_GREY,selected_color=ORANGE,name='temperature',selected_img=slide_switch_blank))
        menu_title_buttons.append(ButtonClass(4,slide_switch_blank,slide_switch_blank,col+255,row,text='Humidity',font_size=26,style=0,font_color=DARK_GREY,selected_color=ORANGE,name='humidity',selected_img=slide_switch_blank))

        row,col=(450,150)
        i=0
        for name in self.humidity_resolution_list:
            menu_buttons.append(ButtonClass(i+1,simple_button_short,simple_button_short_alt,col,row,text=name,font_size=f_size,style=1,font_color=ORANGE,name=name))
            col+=x_spacing
            i+=1
            if (i%3==0):
                row+=button_h+15
                col=150

        col,row=(552-(button_w//2)-10,595)
        settings_button=ButtonClass(11,simple_button_short,simple_button_short_alt,col,row,text='Settings',font_size=f_size,style=0,font_color=ORANGE,name='settings')

        return menu_title_buttons, menu_buttons, settings_button

    def init_gauges(self):
        '''! Init gauges for this page.'''
        gauge_radius=100
        gauges_spacing=48
        weight=8
        arc_h=160
        font=FONT_HELVETICA_NEUE
        f_color=WHITE
        curr_col=250-gauge_radius
        main_font_size=50
        self.temp_gauge_origin=(curr_col,arc_h)
        self.temp_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=10,in_max=40,origin=self.temp_gauge_origin, radius=gauge_radius,weight=weight,color=YELLOW,suffix='°C',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='TEMP',title_font_size=20)

        self.humid_gauge_origin=(curr_col+(2.5*gauge_radius)+gauges_spacing,arc_h)
        self.humid_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=100,origin=self.humid_gauge_origin, radius=gauge_radius,weight=weight,color=YELLOW,suffix='%',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='RH%',title_font_size=20)

    def blit_menu(self,screen):
        '''! Show settings options for HTU31D sensor.'''
        self.button_dict['settings'].text='Back'
        self.blit_all_buttons(screen)

        if self.button_dict['temperature'].selected:
            curr=self.temp_resolution_list
        if self.button_dict['humidity'].selected:
            curr=self.humidity_resolution_list

        res_names=[self.t_res,self.h_res]

        i=0
        for name in curr:
            self.menu_buttons[i].text=name
            if name in res_names:
                self.menu_buttons[i].selected=True
            else:
                self.menu_buttons[i].selected=False
            self.menu_buttons[i].blit_button(screen)
            i+=1

    def blit_current_settings(self,screen):
        '''! Show settings for HTU31D sensor.'''
        '''Show settings'''
        # x_pos,y_pos=138,440
        # txt_surf,w,h=get_text_dimensions(text='RESOLUTION',font_style=FONT_FEDERATION,font_color=ORANGE,style=1,font_size=28)
        # screen.blit(txt_surf,(120+290-w//2,y_pos))
        # y_pos+=60
        # FONT_DIN.render_to(screen, (x_pos, y_pos),'Temperature: ', ORANGE, size=28)
        # y_pos+=35
        # FONT_DIN.render_to(screen, (x_pos+20, y_pos),str(self.t_res)+'C', SLATE, size=34)
        # x_pos,y_pos=440,440+60
        # FONT_DIN.render_to(screen, (x_pos, y_pos),'Humidity: ', ORANGE, size=28)
        # FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),str(self.h_res), SLATE, size=34)
        x_pos,y_pos=138,595
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Heater: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+40, y_pos+35),self.heater, SLATE, size=34)

    def flip_selection(self,pressed_button):
        '''! Invert button selection'''
        if pressed_button.name=='humidity':
            self.button_dict['humidity'].selected=True
            self.button_dict['temperature'].selected=False
            self.button_dict['humidity'].font_size=30
            self.button_dict['temperature'].font_size=24

        if pressed_button.name=='temperature':
            self.button_dict['humidity'].selected=False
            self.button_dict['temperature'].selected=True
            self.button_dict['humidity'].font_size=24
            self.button_dict['temperature'].font_size=30

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)


        # if self.show_menu:
        #     self.blit_menu(screen)
        # else:
        #     self.button_dict['settings'].text='Settings'
        #     self.blit_basic_buttons(screen)
        #     if self.bluetooth_connected:
        #         self.blit_current_settings(screen)
        #     else:
        #         x_pos=138
        #         y_pos=375
        #         y_pos+=110
        #         FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'NO BLUETOOTH', WHITE, size=28)

        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'Temp/Humid Sensor', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'HTU31D', DARK_YELLOW,style=0,size=34)

        # read sensor values
        if self.frame_count%self.num_tics==0:
            self.c_temp,self.humid,_,_=get_temp_humid()

        f_temp=str(round(32+(float(self.c_temp)*1.8),2))+"°F"
        FONT_FEDERATION.render_to(screen, (200, 320), f_temp, SLATE,style=0,size=30)

        try:
            self.temp_gauge_img=self.temp_gauge.blit_gauge(self.c_temp)
            self.humid_gauge_img=self.humid_gauge.blit_gauge(self.humid)
            self.temp_gauge_img.set_colorkey((0,0,0))
            self.humid_gauge_img.set_colorkey((0,0,0))
            screen.blit(self.temp_gauge_img,self.temp_gauge_origin)
            screen.blit(self.humid_gauge_img,self.humid_gauge_origin)
        except Exception as e:
            logging.error (f"aa_arc_gauge error: {e}")


        self.frame_count+=1

        return self.next_screen_name,self.kwargs
