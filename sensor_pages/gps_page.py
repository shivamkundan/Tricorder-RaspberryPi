'''! @brief Read and visualize data from GPS module
@file gps_page.py Contains GPSSensorPage class
'''

from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN,FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW,  WHITE, SLATE
from serial_manager import get_gps
from images import SATELLITE, WORLD_MAP, ALT_ICON, SPD_ICON, DOT2, LAT_ICON
from global_functions import my_map
from pygame import draw as pdraw

# lat/long limits for world map
left_lim=-167.3
right_lim=190.5
top_lim=84.7
bottom_lim=-56

# world map pic params
# PIC_TOP=250
PIC_TOP=175
PIC_LEFT=150

# WORLD_MAP: 530 by 266
PIC_W=530
PIC_H=266
PIC_BOTTOM=PIC_TOP+PIC_H
PIC_RIGHT=PIC_LEFT+PIC_W

# top grid
row1=490
col1=170
col2=400

col3=col1+55
col4=col2+66

row2=row1+35

DOT2_W_DIV_2=10

## Blit page title at this position
TITLE_POS = (150, 92)

class GPSSensorPage(PageTemplate):
	'''! Visualize data from BN880 GPS module.'''
	def __init__(self,name):
		'''! Constructor'''
		super().__init__(name)
		## Return page
		self.prev_page_name='menu_home_page'
		## Next page
		self.next_screen_name=self.name

		## Satellite icon pos
		self.SATELLITE_POS=(555,100)
		## Num satellite text pos
		self.SATELLITE_TXT_POS=(self.SATELLITE_POS[0]+55,self.SATELLITE_POS[1]+20)

		## Altitude icon pos
		self.alt_pos=(col1,row1+5)
		## Speed icon pos
		self.spd_pos=(col2,row1+5)

		## Current latitude
		self.lat=-1
		## Current longitude
		self.long=-1
		## Current altitude
		self.alt=-1
		## Current speed
		self.spd=-1
		## Num of connected satellites
		self.sat=-1

	def draw_location_lines(self,screen):
		'''! Draw the cross hairs denoting current position on map'''
		if (self.sat>0):
			# Map gps co-ords to world-map image co-ords
			y=round(my_map(self.lat,top_lim,bottom_lim,0,PIC_H),0)
			x=round(my_map(self.long,left_lim,right_lim,0,PIC_W),0)

			lw=2
			x_pos=PIC_LEFT+x-DOT2_W_DIV_2+lw/2
			pdraw.line(screen, SLATE, (x_pos,PIC_TOP), (x_pos,PIC_BOTTOM), width=lw)

			y_pos=PIC_TOP+y-DOT2_W_DIV_2-lw/2
			pdraw.line(screen, SLATE, (PIC_LEFT,y_pos), (PIC_RIGHT,y_pos), width=lw)

			# circle(surface, color, center, radius)

	def blit_icons(self,screen):
		'''! Display all icons.'''
		screen.blit(SATELLITE,self.SATELLITE_POS)
		screen.blit(ALT_ICON,self.alt_pos)
		screen.blit(SPD_ICON,self.spd_pos)
		screen.blit(WORLD_MAP,(PIC_LEFT,PIC_TOP))

	def blit_altitude_speed(self,screen):
		'''! Display speed and estimated altitude'''

		# altitude
		FONT_DIN.render_to(screen, (col3,row1), f'{round(self.alt,3)}m', WHITE,style=0,size=36)
		FONT_DIN.render_to(screen, (col3,row2), f'{round(self.alt*3.281,1)}ft', SLATE,style=0,size=24)

		# speed
		FONT_DIN.render_to(screen, (col4,row1), f'{round(self.spd,3)}m/s', WHITE,style=0,size=36)
		FONT_DIN.render_to(screen, (col4,row2), f'{round(self.spd*2.237,3)}mph', SLATE,style=0,size=24)

	def blit_lat_long(self,screen):
		'''! Display latitude and longitude values'''
		row=610
		col=col1

		# Blit title/icon
		FONT_FEDERATION.render_to(screen, (col,row-25), "LAT", ORANGE,style=1,size=20)
		FONT_FEDERATION.render_to(screen, (col2,row-25), "LONG", ORANGE,style=1,size=20)

		# Blit latitude
		minutes=str(self.lat).split('.')[1]
		minutes=int((int(minutes)/100)*60)
		FONT_DIN.render_to(screen, (col,row), f'{self.lat}°', WHITE,style=0,size=34)
		FONT_DIN.render_to(screen, (col,row+40), f'{int(self.lat)}° {minutes}\"', SLATE,style=0,size=24)

		# Blit longitude
		minutes=str(self.long).split('.')[1]
		minutes=int((int(minutes)/100)*60)
		FONT_DIN.render_to(screen, (col2,row), f'{self.long}°', WHITE,style=0,size=34)
		FONT_DIN.render_to(screen, (col2,row+40), f'{int(self.long)}° {minutes}\"', SLATE,style=0,size=24)

	def update_gps_data(self):
		'''! Retrieve new data from sensor'''
		self.lat,self.long,self.alt,self.spd,self.sat=get_gps()

	def blit_num_sats(self,screen):
		'''! Display number of connected satellites'''
		FONT_DIN.render_to(screen, self.SATELLITE_TXT_POS, f"{self.sat}", WHITE,style=0,size=40)

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		FONT_FEDERATION.render_to(screen, TITLE_POS, 'GPS', ORANGE,style=0,size=65)

		self.update_gps_data()
		self.blit_icons(screen)
		try:
			self.blit_altitude_speed(screen)
			self.blit_lat_long(screen)
			self.blit_num_sats(screen)
			self.draw_location_lines(screen)
		except Exception as e:
			logging.error(f"GPS page: {e}")

		return self.next_screen_name,self.kwargs
