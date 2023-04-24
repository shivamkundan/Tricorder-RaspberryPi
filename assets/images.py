#!/usr/bin/python3
import pygame
import os
from paths_and_utils import IMG_PATH,BTN_PATH,ICONS_PATH



IMG_LIST=[]	# global list of loaded images

def img_ld(input_img):
# this function neatly summarizes/prints all images before loading
	# IMG_LIST.append(input_img)
	return pygame.image.load(input_img)

# ------------------------------------ Background image ------------------------------------ #
lcars_bg= img_ld(os.path.join(BTN_PATH,'PIcard_LCARS_square_accent_7_resized.png'))


# =====================================================================================================

page1_dot=img_ld(os.path.join(BTN_PATH,'mobile_style_icons/pdots_1.png'))
page2_dot=img_ld(os.path.join(BTN_PATH,'mobile_style_icons/pdots_2.png'))
page3_dot=img_ld(os.path.join(BTN_PATH,'mobile_style_icons/pdots_3.png'))
page4_dot=img_ld(os.path.join(BTN_PATH,'mobile_style_icons/pdots_4.png'))
page_dots_blank=img_ld(os.path.join(BTN_PATH,'mobile_style_icons/pdots_blank.png'))

PAGE_DOTS={-1:page_dots_blank,1:page1_dot,2:page2_dot,3:page3_dot,4:page4_dot}

# # =====================================================================================================

camera=img_ld(os.path.join(IMG_PATH,'camera.png'))
rolling_tics_icon=img_ld(os.path.join(IMG_PATH,'rolling_tics_icon.png'))

starfleet_logo=img_ld(os.path.join(IMG_PATH,'starfleet_logo.png'))
starfleet_logo_small=pygame.transform.scale(starfleet_logo, (25, 25))

brightness_icon=img_ld(os.path.join(IMG_PATH,'brightness_icon.png'))

wifi_img = img_ld(os.path.join(IMG_PATH,'wifi4.png'))

bluetooth_img = img_ld(os.path.join(IMG_PATH,'bluetooth_icon.png'))
bluetooth_img_not_connected = img_ld(os.path.join(IMG_PATH,'bluetooth_icon_not_connected.png'))

no_battery = img_ld(os.path.join(IMG_PATH,'battery.png'))
no_battery=pygame.transform.scale(no_battery, (30, 30))

satellite=img_ld(os.path.join(IMG_PATH+'satellite.png'))
satellite=pygame.transform.scale(satellite, (40, 40))