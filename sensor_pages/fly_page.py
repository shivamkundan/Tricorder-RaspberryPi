'''
This page mimics the avionics displays used in airplanes.
Eg: garmin-xxxx
'''

import os
import time
import logging

from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE
from colors import ORANGE, WHITE, SKY_BLUE, BROWN, BLACK
from paths_and_utils import IMG_PATH,ICONS_PATH
from global_functions import get_text_dimensions, blitRotate2, my_map
import pygame
import pygame.gfxdraw
from serial_manager import get_imu_orientation, get_temp_humid, get_gps, \
							get_pressure, get_vis_ir, get_uv, \
							set_tsl_scl_connect, set_tsl_scl_disconnect

# in roughly clockwise display order
from images import  SATELLITE, WIND_SOCK, \
					ART_HORIZON_MARKINGS, ROLL_INDICATOR, \
					HEADING_INDICATOR, ENT_TOP, ENT_BACK_TRACE, \
					THERMOMETER, HUMIDITY_ICON, PRESSURE_ICON, \
					LIGHT_ICON, UV_ICON, IR_ICON

# pre-computed variables
from fly_page_vars import *

R_ALT=pygame.Rect(ALTITUDE_RECT_X_POS, ALTITUDE_RECT_Y_POS, \
						ALTITUDE_RECT_WIDTH, ALTITUDE_RECT_HEIGHT)
R_SPD=pygame.Rect(SPEED_RECT_X_POS, SPEED_RECT_Y_POS, \
						SPEED_RECT_WIDTH, SPEED_RECT_HEIGHT)

def txt_dims(txt):
# wrapper fn
	_,w,h=get_text_dimensions(text=str(txt), font_style=FONT_FEDERATION, font_color=WHITE, style=0, font_size=24)
	return w,h

def compute_positions(x_val,curr_val):
	return [((x_val,h1), f"{curr_val-40}"),
			((x_val,h2), f"{curr_val-30}"),
			((x_val,h3), f"{curr_val-20}"),
			((x_val,h4), f"{curr_val-10}"),
			((x_val,h5), f"{curr_val+20}"),
			((x_val,h6), f"{curr_val+30}"),
			((x_val,h7), f"{curr_val+40}")]

def blit_column_txt(screen,x_val,curr_val):
	l=compute_positions(x_val,curr_val)
	for pos in l:
		FONT_FEDERATION.render_to(screen, pos[0], pos[1], WHITE,style=0,size=INDICATOR_SMALL_FONT_SIZE)

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

	def get_sensor_data(self):
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

	def blit_vertical_column(self, screen, rectangle, curr_val, txt_pos, x_val):
		pygame.gfxdraw.box(screen, rectangle, INDICATOR_RECTS_COLOR)

		w,h=txt_dims(curr_val)

		r2=pygame.Rect(txt_pos[0]-border_size, txt_pos[1]-border_size, w+border_size*2, h+border_size*2)
		pygame.draw.rect(screen, BLACK, r2)

		# blit current altitude
		FONT_FEDERATION.render_to(screen, txt_pos, f"{curr_val}", WHITE,style=0,size=24)

		# blit other altitudes
		blit_column_txt(screen,x_val,curr_val)

		return screen

	def blit_art_horizon(self,screen):
		m=my_map(self.roll,0,45,START_Y,440)  # for 0 to 45 degrees
		left_height=int(m)
		right_height=START_Y

		pygame.draw.rect(screen, SKY_BLUE, pygame.Rect(START_X, START_Y, WIDTH, HEIGHT))
		pygame.draw.polygon(screen, BROWN, ((START_X,START_Y+left_height),(START_X,START_Y+HEIGHT),(START_X+WIDTH,START_Y+HEIGHT),(START_X+WIDTH,START_Y+right_height)))
		screen.blit(ART_HORIZON_MARKINGS,ART_HORIZON_MARKINGS_POS)
		screen.blit(ENT_BACK_TRACE,ENT_BACK_POS)

		blitRotate2(screen, ROLL_INDICATOR,    ART_HORIZON_MARKINGS_POS, int(self.roll))
		blitRotate2(screen, HEADING_INDICATOR, HEADING_INDICATOR_POS,    int(round(float(self.heading),0)))
		return screen

	def blit_env_data(self, screen, icon, icon_pos, txt_pos, txt, font_size=INFO_FONT_SIZE):
		screen.blit(icon,icon_pos)
		FONT_HELVETICA_NEUE.render_to(screen, txt_pos, txt, WHITE,style=0,size=font_size)
		return screen

	def blit_sensor_data(self,screen):
		for item in [
					(WIND_SOCK,     WIND_SOCK_POS,     WIND_TXT_POS,      f"{self.wind_speed}mph",   INFO_FONT_SIZE-2),\
					(THERMOMETER,   THERM_POS,         TEMP_TXT_POS,      f"{self.temperature}°C",   INFO_FONT_SIZE),  \
					(HUMIDITY_ICON, HUMID_ICON_POS,    HUMID_TXT_POS,     f"{self.humidity}%",       INFO_FONT_SIZE),  \
					(PRESSURE_ICON, PRESSURE_ICON_POS, PRESSURE_TXT_POS,  f"{self.pressure}hPa",     INFO_FONT_SIZE),  \
					(LIGHT_ICON,    LIGHT_ICON_POS,    LIGHT_TXT_POS,     f"{self.vis}lux",          INFO_FONT_SIZE),  \
					(UV_ICON,       UV_ICON_POS,       UV_TXT_POS,        f"{self.uvi}",             INFO_FONT_SIZE),  \
					(IR_ICON,       IR_ICON_POS,       IR_TXT_POS,        f"{self.ir}",              INFO_FONT_SIZE),  \
					(SATELLITE,     SATELLITE_POS,     SATELLITE_TXT_POS, f"{self.satellite_count}", INFO_FONT_SIZE)]:
						screen=self.blit_env_data(screen,item[0],item[1],item[2],item[3],item[4])
		return screen

	def blit_gps_pos_data(self,screen):
		FONT_HELVETICA_NEUE.render_to(screen, (260,150), f"roll:{self.roll}° pitch:{self.pitch}° head:{self.heading}°", WHITE,style=0,size=INFO_FONT_SIZE)
		FONT_HELVETICA_NEUE.render_to(screen,LAT_TXT_POS , f"{self.lat}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)
		FONT_HELVETICA_NEUE.render_to(screen, LONG_TXT_POS, f"{self.long}", WHITE,style=0,size=LAT_LNG_TXT_SIZE)
		return screen

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		# ----- get sensor data ----- #
		try:
			self.get_sensor_data()
		except Exception as e:
			logging.error(e)
		self.uvi=self.uv # temp fix

		# ----- artificial horizon ----- #
		screen=self.blit_art_horizon(screen)

		# ----- altitude indicator ----- #
		screen=self.blit_vertical_column(screen, R_ALT, self.altitude, ALTITUDE_TXT_POS, x1)

		# ----- speed indicator ----- #
		screen=self.blit_vertical_column(screen, R_SPD, self.speed, SPEED_TXT_POS, x0)

		# ----- all other data  ----- #
		screen=self.blit_sensor_data(screen)

		# ----- positioning data ----- #
		screen=self.blit_gps_pos_data(screen)

		# ----- ent img ----- #
		screen.blit(ENT_TOP,ENT_TOP_POS)

		# ----- blit title ----- #
		FONT_FEDERATION.render_to(screen, (150, 76), 'Fly', ORANGE,style=0,size=42)

		self.frame_count+=1
		return self.next_screen_name,self.kwargs
