from page_templates import PageTemplate
from fonts import FONT_FEDERATION, HELVETICA, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, BLUE,GRID_BLUE,MISTY_BLUE,WHITE,SKY_BLUE,BROWN, BLACK
from images import IMG_PATH,ICONS_PATH,lcars_bg
from global_functions import get_text_dimensions, blitRotate2, my_map
import pygame
import pygame.gfxdraw
from serial_manager import *
import os
import time

# ------ horizon params ------ #
START_Y=130
START_X=150
WIDTH=530
HEIGHT=450

MID_TXT_Y_POS=START_Y+HEIGHT//2




INDICATOR_RECTS_COLOR=(0,0,0,127)
ALTITUDE_RECT_X_POS=START_X+475
ALTITUDE_RECT_Y_POS=180
ALTITUDE_TXT_POS=(ALTITUDE_RECT_X_POS-5,MID_TXT_Y_POS)
ALTITUDE_RECT_WIDTH=40
ALTITUDE_RECT_HEIGHT=300


SPEED_RECT_X_POS=START_X+5
SPEED_RECT_Y_POS=ALTITUDE_RECT_Y_POS
SPEED_TXT_POS=(SPEED_RECT_X_POS-5,MID_TXT_Y_POS)
SPEED_RECT_WIDTH=ALTITUDE_RECT_WIDTH
SPEED_RECT_HEIGHT=ALTITUDE_RECT_HEIGHT


INDICATOR_SMALL_FONT_SIZE=15
INDICATOR_Y_DIFF=25

h1=ALTITUDE_RECT_Y_POS+4
h2=h1+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE
h3=h2+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE
h4=h3+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE

h7=ALTITUDE_RECT_Y_POS+ALTITUDE_RECT_HEIGHT-INDICATOR_SMALL_FONT_SIZE-4
h6=h7-(INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE)
h5=h6-(INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE)

x0=SPEED_RECT_X_POS
x1=ALTITUDE_RECT_X_POS

# ------ horizon icon ------ #
art_horizon=pygame.image.load(os.path.join(ICONS_PATH+'artificial-horizon.png'))
art_horizon_markings=pygame.image.load(os.path.join(IMG_PATH+'artificial-horizon_markings.png'))
ART_HORIZON_MARKINGS_POS=(START_X+WIDTH//2-art_horizon_markings.get_rect().size[0]//2,START_Y+HEIGHT//2-art_horizon_markings.get_rect().size[1]//2)



# ------ compass/heading ------ #
heading_indicator=pygame.image.load(os.path.join(IMG_PATH+'compass_avionic.png'))
ent_top=pygame.image.load(os.path.join(IMG_PATH+'enterprise_top2.png'))
HEADING_INDICATOR_POS=(340,445)
ENT_TOP_POS=(400,500)

# ------ wind icon ------ #
wind_sock=pygame.image.load(os.path.join(IMG_PATH+'wind_sock.png'))
wind_sock=pygame.transform.scale(wind_sock, (50, 50))
WIND_SOCK_POS=(550,66)
WIND_TXT_POS=(WIND_SOCK_POS[0]+50+5,WIND_SOCK_POS[1]+20)

# ------ satellite icon ------ #
satellite=pygame.image.load(os.path.join(IMG_PATH+'satellite.png'))
satellite=pygame.transform.scale(satellite, (40, 40))
SATELLITE_POS=(450,WIND_SOCK_POS[1])
SATELLITE_TXT_POS=(SATELLITE_POS[0]+50+5,SATELLITE_POS[1]+20)



INFO_FONT_SIZE=20
info_row1_title=590
row_spacing=55

info_row1_value=info_row1_title+10

info_row2_title=info_row1_title+row_spacing
info_row2_value=info_row2_title+10

info_col1=170
col_increment=170
info_col2=info_col1+col_increment
info_col3=info_col2+col_increment

# ------ thermometer icon ------ #
thermometer=pygame.image.load(os.path.join(IMG_PATH+'thermometer_plain.png'))
THERM_POS=(info_col1,info_row1_title)
TEMP_TXT_POS=(info_col1+30,info_row1_value)


# ------ humidity icon ------ #
humidity_icon=pygame.image.load(os.path.join(IMG_PATH+'humidity_icon.png'))
HUMID_ICON_POS=(info_col2,info_row1_title)
HUMID_TXT_POS=(info_col2+30,info_row1_value)

# ------ pressure icon ------ #
pressure_icon=pygame.image.load(os.path.join(IMG_PATH+'pressure_icon2.png'))
PRESSURE_ICON_POS=(info_col3,info_row1_title)
PRESSURE_TXT_POS=(info_col3+30,info_row1_value)

# ------ light icon ------ #
# light_icon=pygame.image.load(os.path.join(IMG_PATH+'light_icon2.png'))
light_icon=pygame.image.load(os.path.join(IMG_PATH+'vis_icon.png'))
LIGHT_ICON_POS=(info_col1-2,info_row2_title)
LIGHT_TXT_POS=(info_col1+38,info_row2_value)


# ------ UV icon ------ #
uv_icon=pygame.image.load(os.path.join(IMG_PATH+'uvi_icon.png'))
UV_ICON_POS=(info_col2-2,info_row2_title)
UV_TXT_POS=(info_col2+38,info_row2_value)


# ------ IR icon ------ #
ir_icon=pygame.image.load(os.path.join(IMG_PATH+'ir_icon.png'))
IR_ICON_POS=(info_col3-2,info_row2_title)
IR_TXT_POS=(info_col3+38,info_row2_value)




ent_back=pygame.image.load(
os.path.join(IMG_PATH+'ent_back_trace.png'))

ent_size_x=ent_back.get_rect().size[0]
ent_size_y=ent_back.get_rect().size[1]
ent_back=pygame.transform.scale(ent_back, (int(round(ent_size_x*0.8,0)), int(round(ent_size_y*0.8,0))))


ENT_BACK_POS=(START_X+WIDTH//2-ent_back.get_rect().size[0]//2,START_Y+HEIGHT//2-ent_back.get_rect().size[1]//2+23)


LAT_LNG_TXT_SIZE=18
LAT_TXT_POS=(390,WIND_SOCK_POS[1])
LONG_TXT_POS=(390,WIND_SOCK_POS[1]+5+LAT_LNG_TXT_SIZE)





roll_indicator=pygame.image.load(os.path.join(IMG_PATH+'roll_indicator.png'))


class FlyPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='MenuHomePage'

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

    # def draw_artitficial_horizon(self):


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


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        # e.post(REQUEST_FLY_DATA)


        self.get_data()


        FONT_FEDERATION.render_to(screen, (150, 76), 'Fly', ORANGE,style=0,size=42)
        # FONT_FEDERATION.render_to(screen, (150, 117), 'page', DARK_YELLOW,style=0,size=34)

        # pygame.draw.polygon(screen, ORANGE, ((25,75),(76,125),(250,375),(400,25),(60,540)))

        # screen.blit(art_horizon,(215,195))

        self.uvi=self.uv


        # ----- artificial horizon ----- #
        m=my_map(self.roll,0,45,START_Y,440)
        left_height=int(m)
        # print ("left_height,map:",left_height,m)
        # left_height=300
        right_height=START_Y


         # my_map(x,in_min,in_max,out_min,out_max)



        pygame.draw.rect(screen, SKY_BLUE, pygame.Rect(START_X, START_Y, WIDTH, HEIGHT))
        pygame.draw.polygon(screen, BROWN, ((START_X,START_Y+left_height),(START_X,START_Y+HEIGHT),(START_X+WIDTH,START_Y+HEIGHT),(START_X+WIDTH,START_Y+right_height)))
        screen.blit(art_horizon_markings,ART_HORIZON_MARKINGS_POS)
        screen.blit(ent_back,ENT_BACK_POS)

        blitRotate2(screen, roll_indicator, ART_HORIZON_MARKINGS_POS, int(self.roll))


        blitRotate2(screen, heading_indicator, HEADING_INDICATOR_POS, int(round(float(self.heading),0)))
        # screen.blit(roll_indicator,ART_HORIZON_MARKINGS_POS)


        # ----- altitude indicator ----- #
        pygame.gfxdraw.box(screen, pygame.Rect(ALTITUDE_RECT_X_POS, ALTITUDE_RECT_Y_POS, ALTITUDE_RECT_WIDTH, ALTITUDE_RECT_HEIGHT), INDICATOR_RECTS_COLOR)
        surf,w,h=get_text_dimensions(text=str(self.altitude),font_style=FONT_FEDERATION,font_color=WHITE,style=0,font_size=24)

        border_size=6
        ALTITUDE_TXT_POS=(ALTITUDE_RECT_X_POS+ALTITUDE_RECT_WIDTH-w-border_size,MID_TXT_Y_POS)
        pygame.draw.rect(screen, BLACK, pygame.Rect(ALTITUDE_TXT_POS[0]-border_size, ALTITUDE_TXT_POS[1]-border_size, w+border_size*2, h+border_size*2))
        FONT_FEDERATION.render_to(screen, ALTITUDE_TXT_POS, f"{self.altitude}", WHITE,style=0,size=24)

        FONT_FEDERATION.render_to(screen, (x1,h1), f"{self.altitude-40}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h2), f"{self.altitude-30}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h3), f"{self.altitude-20}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h4), f"{self.altitude-10}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h5), f"{self.altitude+20}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h6), f"{self.altitude+30}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x1,h7), f"{self.altitude+40}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)


        # ----- speed indicator ----- #
        pygame.gfxdraw.box(screen, pygame.Rect(SPEED_RECT_X_POS, SPEED_RECT_Y_POS, SPEED_RECT_WIDTH, SPEED_RECT_HEIGHT), INDICATOR_RECTS_COLOR)

        surf,w,h=get_text_dimensions(text=str(self.speed),font_style=FONT_FEDERATION,font_color=WHITE,style=0,font_size=24)
        SPEED_TXT_POS=(SPEED_RECT_X_POS+border_size,MID_TXT_Y_POS)

        pygame.draw.rect(screen, BLACK, pygame.Rect(SPEED_RECT_X_POS, SPEED_TXT_POS[1]-border_size, w+border_size*2, h+border_size*2))

        FONT_FEDERATION.render_to(screen, SPEED_TXT_POS, f"{self.speed}", WHITE,style=0,size=24)

        FONT_FEDERATION.render_to(screen, (x0,h1), f"{int(self.speed-40)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h2), f"{int(self.speed-30)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h3), f"{int(self.speed-20)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h4), f"{int(self.speed-10)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)


        # FONT_FEDERATION.render_to(screen, (x0,h5), f"{self.speed+10}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h5), f"{int(self.speed+20)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h6), f"{int(self.speed+30)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)
        FONT_FEDERATION.render_to(screen, (x0,h7), f"{int(self.speed+40)}", WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)




        # ----- extras  ----- #
        screen.blit(wind_sock,WIND_SOCK_POS)
        FONT_HELVETICA_NEUE.render_to(screen, WIND_TXT_POS, f"{self.wind_speed}mph", WHITE,style=0,size=INFO_FONT_SIZE-2)
        screen.blit(thermometer,THERM_POS)
        FONT_HELVETICA_NEUE.render_to(screen, TEMP_TXT_POS, f"{self.temperature}°C", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(satellite,SATELLITE_POS)
        FONT_HELVETICA_NEUE.render_to(screen, SATELLITE_TXT_POS, f"{self.satellite_count}", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(humidity_icon,HUMID_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, HUMID_TXT_POS, f"{self.humidity}%", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(pressure_icon,PRESSURE_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, PRESSURE_TXT_POS, f"{self.pressure}hPa", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(light_icon,LIGHT_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, LIGHT_TXT_POS, f"{self.vis}lux", WHITE,style=0,size=INFO_FONT_SIZE)


        screen.blit(uv_icon,UV_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, UV_TXT_POS, f"{self.uvi}", WHITE,style=0,size=INFO_FONT_SIZE)

        screen.blit(ir_icon,IR_ICON_POS)
        FONT_HELVETICA_NEUE.render_to(screen, IR_TXT_POS, f"{self.ir}", WHITE,style=0,size=INFO_FONT_SIZE)


        screen.blit(ent_top,ENT_TOP_POS)

        FONT_HELVETICA_NEUE.render_to(screen, (380,150), f"{self.roll},{self.pitch},{self.heading}", WHITE,style=0,size=INFO_FONT_SIZE)

        FONT_HELVETICA_NEUE.render_to(screen,LAT_TXT_POS , f"{self.lat}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)
        FONT_HELVETICA_NEUE.render_to(screen, LONG_TXT_POS, f"{self.long}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)

        # FONT_HELVETICA_NEUE.render_to(screen, LIGHT_ICON_POS, f"VIS", ORANGE,style=1,size=16)


        # screen.blit(lcars_bg,(0,0))

        # if self.roll>45:
        #     self.roll=0

        self.frame_count+=1

        # if self.frame_count%3==0:
        #     self.roll+=1


        return self.next_screen_name,self.kwargs
