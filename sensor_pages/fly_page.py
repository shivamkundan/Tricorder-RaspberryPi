from page_templates import PageTemplate
from fonts import FONT_FEDERATION, HELVETICA, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, BLUE,GRID_BLUE,MISTY_BLUE,WHITE,SKY_BLUE,BROWN, BLACK
from paths_and_utils import IMG_PATH,ICONS_PATH
from global_functions import get_text_dimensions, blitRotate2, my_map
import pygame
import pygame.gfxdraw
from serial_manager import get_imu_orientation, get_temp_humid, get_gps, get_pressure, get_vis_ir, get_uv, set_tsl_scl_connect, set_tsl_scl_disconnect
import os
import time
import logging

from images import lcars_bg, ART_HORIZON_MARKINGS, HEADING_INDICATOR, ENT_TOP, WIND_SOCK, \
                    THERMOMETER, HUMIDITY_ICON, PRESSURE_ICON, LIGHT_ICON, \
                    UV_ICON, IR_ICON, SATELLITE, ENT_BACK_TRACE, ROLL_INDICATOR

from fly_page_vars import *

class FlyPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        self.wind_speed=0.1

        self.satellite_count=-1
        self.altitude=50
        self.speed=10
        self.lat=0
        self.long=0

        self.roll=0
        self.pitch=0
        self.heading=0

        self.temperature=-1
        self.humidity=-1

        self.pressure=-1
        self.bmp_alt=0

        self.vis=-1
        self.uv=-1
        self.uvi=-1
        self.ir=-1

        self.vis_ir_tics=17
        self.uv_tics=13
        self.imu_tics=3
        self.gps_tics=5
        self.temp_humid_tics=29
        self.pressure_tics=37


        self.frame_count=0

    def get_data(self):
        if self.frame_count%self.imu_tics==0:
            self.heading,self.roll,self.pitch=get_imu_orientation()

        if self.frame_count%self.temp_humid_tics==0:
            self.temperature,self.humidity,_,_=get_temp_humid()

        if self.frame_count%self.gps_tics==0:
            self.lat,self.long,self.altitude,self.speed,self.satellite_count=get_gps()

        if self.frame_count%self.pressure_tics==0:
            self.bmp_alt,self.pressure,_,_,_=get_pressure()

        if self.frame_count%self.uv_tics==0:
            self.uv,_,_,_,_,_,_,_=get_uv()

        if self.frame_count%self.vis_ir_tics==0:
            set_tsl_scl_connect()
            time.sleep(1)
            self.vis,self.ir,_,_,_ = get_vis_ir()
            set_tsl_scl_disconnect()


    def blit_altitude_column(self,screen):
        FONT_FEDERATION.render_to(screen, ALTITUDE_TXT_POS, f"{self.altitude}", WHITE,style=0,size=24)
        FONT_FEDERATION.render_to(screen, (x1,h1), f"{self.altitude-40}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h2), f"{self.altitude-30}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h3), f"{self.altitude-20}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h4), f"{self.altitude-10}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h5), f"{self.altitude+20}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h6), f"{self.altitude+30}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h7), f"{self.altitude+40}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        return screen

    def blit_speed_column(self,screen):

        # blit current speed
        FONT_FEDERATION.render_to(screen, SPEED_TXT_POS, f"{self.speed}", WHITE,style=0,size=24)

        # blit other speeds
        FONT_FEDERATION.render_to(screen, (x0,h1), f"{int(self.speed-40)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h2), f"{int(self.speed-30)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h3), f"{int(self.speed-20)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h4), f"{int(self.speed-10)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h5), f"{int(self.speed+20)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h6), f"{int(self.speed+30)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h7), f"{int(self.speed+40)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        return screen

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        try:
            self.get_data()
        except Exception as e:
            logging.error(e)


        FONT_FEDERATION.render_to(screen, (150, 76), 'Fly', ORANGE,style=0,size=42)
        self.uvi=self.uv


        # ----- artificial horizon ----- #
        m=my_map(self.roll,0,45,START_Y,440)
        left_height=int(m)
        right_height=START_Y

        pygame.draw.rect(screen, SKY_BLUE, pygame.Rect(START_X, START_Y, WIDTH, HEIGHT))
        pygame.draw.polygon(screen, BROWN, ((START_X,START_Y+left_height),(START_X,START_Y+HEIGHT),(START_X+WIDTH,START_Y+HEIGHT),(START_X+WIDTH,START_Y+right_height)))
        screen.blit(ART_HORIZON_MARKINGS,ART_HORIZON_MARKINGS_POS)
        screen.blit(ENT_BACK_TRACE,ENT_BACK_POS)

        blitRotate2(screen, ROLL_INDICATOR, ART_HORIZON_MARKINGS_POS, int(self.roll))


        blitRotate2(screen, HEADING_INDICATOR, HEADING_INDICATOR_POS, int(round(float(self.heading),0)))


        # ----- altitude indicator ----- #
        pygame.gfxdraw.box(screen, pygame.Rect(ALTITUDE_RECT_X_POS, ALTITUDE_RECT_Y_POS, ALTITUDE_RECT_WIDTH, ALTITUDE_RECT_HEIGHT), INDICATOR_RECTS_COLOR)
        surf,w,h=get_text_dimensions(text=str(self.altitude),font_style=FONT_FEDERATION,font_color=WHITE,style=0,font_size=24)
        border_size=6
        ALTITUDE_TXT_POS=(ALTITUDE_RECT_X_POS+ALTITUDE_RECT_WIDTH-w-border_size,MID_TXT_Y_POS)
        pygame.draw.rect(screen, BLACK, pygame.Rect(ALTITUDE_TXT_POS[0]-border_size, ALTITUDE_TXT_POS[1]-border_size, w+border_size*2, h+border_size*2))

        screen=self.blit_altitude_column(screen)


        # ----- speed indicator ----- #
        pygame.gfxdraw.box(screen, pygame.Rect(SPEED_RECT_X_POS, SPEED_RECT_Y_POS, SPEED_RECT_WIDTH, SPEED_RECT_HEIGHT), INDICATOR_RECTS_COLOR)
        surf,w,h=get_text_dimensions(text=str(self.speed),font_style=FONT_FEDERATION,font_color=WHITE,style=0,font_size=24)
        SPEED_TXT_POS=(SPEED_RECT_X_POS+border_size,MID_TXT_Y_POS)
        pygame.draw.rect(screen, BLACK, pygame.Rect(SPEED_RECT_X_POS, SPEED_TXT_POS[1]-border_size, w+border_size*2, h+border_size*2))

        screen=self.blit_speed_column(screen)





        # ----- extras  ----- #
        screen.blit(WIND_SOCK,WIND_SOCK_POS)
        FONT_HELVETICA_NEUE.render_to(screen, WIND_TXT_POS, f"{self.wind_speed}mph", WHITE,style=0,size=INFO_FONT_SIZE-2)
        screen.blit(THERMOMETER,THERM_POS)
        FONT_HELVETICA_NEUE.render_to(screen, TEMP_TXT_POS, f"{self.temperature}°C", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(SATELLITE,SATELLITE_POS)
        FONT_HELVETICA_NEUE.render_to(screen, SATELLITE_TXT_POS, f"{self.satellite_count}", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(HUMIDITY_ICON,HUMID_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, HUMID_TXT_POS, f"{self.humidity}%", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(PRESSURE_ICON,PRESSURE_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, PRESSURE_TXT_POS, f"{self.pressure}hPa", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(LIGHT_ICON,LIGHT_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, LIGHT_TXT_POS, f"{self.vis}lux", WHITE,style=0,size=INFO_FONT_SIZE)


        screen.blit(UV_ICON,UV_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, UV_TXT_POS, f"{self.uvi}", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(IR_ICON,IR_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, IR_TXT_POS, f"{self.ir}", WHITE,style=0,size=INFO_FONT_SIZE)


        screen.blit(ENT_TOP,ENT_TOP_POS)

        FONT_HELVETICA_NEUE.render_to(screen, (380,150), f"{self.roll},{self.pitch},{self.heading}", WHITE,style=0,size=INFO_FONT_SIZE)

        FONT_HELVETICA_NEUE.render_to(screen,LAT_TXT_POS , f"{self.lat}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)
        FONT_HELVETICA_NEUE.render_to(screen, LONG_TXT_POS, f"{self.long}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)


        self.frame_count+=1

        # if self.frame_count%3==0:
        #     self.roll+=1


        return self.next_screen_name,self.kwargs
