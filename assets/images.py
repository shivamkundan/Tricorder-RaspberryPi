#!/usr/bin/python3
import pygame
import os
from paths_and_utils import IMG_PATH,BTN_PATH,ICONS_PATH



IMG_LIST=[]	# global list of loaded images

def img_ld(input_img):
# this function neatly summarizes/prints all images before loading
	# IMG_LIST.append(input_img)
	return pygame.image.load(os.path.join(input_img))

# ------------------------------------ Background image ------------------------------------ #
lcars_bg= img_ld(BTN_PATH+'PIcard_LCARS_square_accent_7_resized.png')


# =====================================================================================================

page1_dot=img_ld(BTN_PATH+'mobile_style_icons/pdots_1.png')
page2_dot=img_ld(BTN_PATH+'mobile_style_icons/pdots_2.png')
page3_dot=img_ld(BTN_PATH+'mobile_style_icons/pdots_3.png')
page4_dot=img_ld(BTN_PATH+'mobile_style_icons/pdots_4.png')
page_dots_blank=img_ld(BTN_PATH+'mobile_style_icons/pdots_blank.png')

PAGE_DOTS={-1:page_dots_blank,1:page1_dot,2:page2_dot,3:page3_dot,4:page4_dot}

# =====================================================================================================

camera=img_ld(IMG_PATH+'camera.png')
rolling_tics_icon=img_ld(IMG_PATH+'rolling_tics_icon.png')

starfleet_logo=img_ld(IMG_PATH+'starfleet_logo.png')
starfleet_logo_small=pygame.transform.scale(starfleet_logo, (25, 25))

brightness_icon=img_ld(IMG_PATH+'brightness_icon.png')

wifi_img = img_ld(IMG_PATH+'wifi4.png')

bluetooth_img = img_ld(IMG_PATH+'bluetooth_icon.png')
bluetooth_img_not_connected = img_ld(IMG_PATH+'bluetooth_icon_not_connected.png')

no_battery = img_ld(IMG_PATH+'battery.png')
no_battery=pygame.transform.scale(no_battery, (30, 30))

SATELLITE=img_ld(IMG_PATH+'satellite.png')
SATELLITE=pygame.transform.scale(SATELLITE, (40, 40))

# =====================================================================================================

# ------------- These are for IMU page ------------- #
COMPASS=img_ld(IMG_PATH+'compass_custom.png')
COMPASS=pygame.transform.scale(COMPASS, (200, 200))

ENT_BACK=img_ld(IMG_PATH+'ent_back.png')
ENT_BACK=pygame.transform.scale(ENT_BACK, (200, 75))

ENT_SIDE=img_ld(IMG_PATH+'ent_side_small.png')
scale=1.5
ENT_SIDE=pygame.transform.scale(ENT_SIDE, (int(111*scale), int(35*scale)))

DOT=img_ld(IMG_PATH+'dot.png')
DOT2=pygame.transform.scale(DOT, (20, 20))

XYZ_ROT=img_ld(IMG_PATH+'xyz_rotation.png')
XYZ_3D_ROT=img_ld(IMG_PATH+'xyz_3D_rot.png')
XYZ_3D=img_ld(IMG_PATH+'xyz_3D.png')

# ======================================================================================================

# ------------- These are for FLY page ------------- #
ART_HORIZON_MARKINGS=img_ld(IMG_PATH+'artificial-horizon_markings.png')
HEADING_INDICATOR=img_ld(IMG_PATH+'compass_avionic.png')
ENT_TOP=img_ld(IMG_PATH+'enterprise_top2.png')

WIND_SOCK=img_ld(IMG_PATH+'wind_sock.png')
WIND_SOCK=pygame.transform.scale(WIND_SOCK, (50, 50))

THERMOMETER=img_ld(IMG_PATH+'thermometer_plain.png')
HUMIDITY_ICON=img_ld(IMG_PATH+'humidity_icon.png')
PRESSURE_ICON=img_ld(IMG_PATH+'pressure_icon2.png')
LIGHT_ICON=img_ld(IMG_PATH+'vis_icon.png')

UV_ICON=img_ld(IMG_PATH+'uvi_icon.png')
IR_ICON=img_ld(IMG_PATH+'ir_icon.png')

ENT_BACK_TRACE=img_ld(IMG_PATH+'ent_back_trace.png')
ROLL_INDICATOR=img_ld(IMG_PATH+'roll_indicator.png')

# ======================================================================================================

# ------------- These are for GPS page ------------- #
WORLD_MAP=img_ld(IMG_PATH+'world_map_orange.png')
ALT_ICON=img_ld(IMG_PATH+'altitude.png')
SPD_ICON=img_ld(IMG_PATH+'speed.png')
LAT_ICON=img_ld(IMG_PATH+'latitude.png')