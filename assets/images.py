#!/usr/bin/python3
import pygame
import os, sys
import time,datetime
from fonts import *
from colors import *
import math
from paths_and_utils import IMG_PATH,LCARS_PATH,ICONS_PATH
pygame.init()

# ------------------------------------ Background image ------------------------------------ #
lcars_bg= pygame.image.load(os.path.join(LCARS_PATH,'Picard/PIcard_LCARS_square_accent_7_resized.png'))


# =====================================================================================================

page1_dot=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/pdots_1.png'))
page2_dot=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/pdots_2.png'))
page3_dot=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/pdots_3.png'))
page4_dot=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/pdots_4.png'))
page_dots_blank=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/pdots_blank.png'))

PAGE_DOTS={-1:page_dots_blank,1:page1_dot,2:page2_dot,3:page3_dot,4:page4_dot}

# # =====================================================================================================

camera=pygame.image.load(os.path.join(IMG_PATH,'camera.png'))
rolling_tics_icon=pygame.image.load(os.path.join(IMG_PATH,'rolling_tics_icon.png'))

starfleet_logo=pygame.image.load(os.path.join(IMG_PATH,'starfleet_logo.png'))
brightness_icon=pygame.image.load(os.path.join(IMG_PATH,'brightness_icon.png'))
starfleet_logo_small=pygame.transform.scale(starfleet_logo, (25, 25))

wifi_img = pygame.image.load(os.path.join(IMG_PATH,'wifi4.png'))
bluetooth_img = pygame.image.load(os.path.join(IMG_PATH,'bluetooth_icon.png'))
bluetooth_img_not_connected = pygame.image.load(os.path.join(IMG_PATH,'bluetooth_icon_not_connected.png'))

no_battery = pygame.image.load(os.path.join(IMG_PATH,'battery.png'))

no_battery=pygame.transform.scale(no_battery, (30, 30))

satellite=pygame.image.load(os.path.join(IMG_PATH+'satellite.png'))
satellite=pygame.transform.scale(satellite, (40, 40))