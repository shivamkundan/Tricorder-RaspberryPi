#!/usr/bin/python3
import pygame
import os, sys
import time,datetime

HOME_DIR='/home/pi/Sensor_Scripts/pygame_code/tricorder/'
pygame.init()

number_keys=[pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]


# ----------------- Colors ----------------- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE=(73,81,119)
# ORANGE=(235, 139, 49)

ORANGE=pygame.Color('#ff7700')


# FONT_BLUE=pygame.Color('#5A7280')
FONT_BLUE=pygame.Color('#143045')
LIGHT_BLUE=pygame.Color('#4c9ea7')

# YELLOW = (255, 255, 0)
YELLOW=(255, 153, 0)
DARK_YELLOW=(178, 107, 0)
WHITE=(255,255,255)
LIGHT_GREY=(128,128,128)
GREY=(96,96,96)
DARK_GREY=(63,63,63)
LIGHT_GREY=(144,144,144)
RED = (255, 0, 0)
DARK_RED=(129,31,33)
SKY_BLUE=(64, 101, 225)
BROWN=(78, 54, 18)
R5=(255,50,52)
R4=(200,40,42)
R3=(115,20,22)
R2=(127,0,0)
R1=(63,0,0)

DARK_BLUE=(75,82,120)

GREEN=(0,255,0)
BLUE = pygame.Color("#7ec0ee")
PURPLE=(146, 52, 235)
VIOLET =pygame.Color('#9944ff')
# BLUE = (0,0,100)
GRID_BLUE=(int(0.1*255),int(0.2*255),int(0.3*255))

DARK_YELLOW=(178, 114, 0)

# ---------------------------------------
BLUE_GREY=pygame.Color('#4D6470')

MISTY_BLUE=pygame.Color('#A3BAC0')

SLATE=pygame.Color('#7B9AA0')

CREAM=pygame.Color('#EFEBE2')
# ----------------- Fonts ----------------- #
FONT = pygame.font.SysFont('HelveticaNeue', 12,bold=False)
FPS_FONT = pygame.font.SysFont('Helvetica', 27,bold=True)

FONT_6 = pygame.font.SysFont('Helvetica', 6)
FONT_8= pygame.font.SysFont('Helvetica', 8)
FONT_9= pygame.font.SysFont('Helvetica', 9)
FONT_10 = pygame.font.SysFont('Helvetica', 10)
FONT_11 = pygame.font.SysFont('Helvetica', 11)
FONT_12 = pygame.font.SysFont('Helvetica', 12)
FONT_13 = pygame.font.SysFont('Helvetica', 13)
FONT_14 = pygame.font.SysFont('Helvetica', 14)
FONT_15 = pygame.font.SysFont('Helvetica', 15)
FONT_16 = pygame.font.SysFont('Helvetica', 16)
FONT_18 = pygame.font.SysFont('Helvetica', 18)
FONT_20 = pygame.font.SysFont('Helvetica', 20)
FONT_22 = pygame.font.SysFont('Helvetica', 22)
FONT_26 = pygame.font.SysFont('Helvetica', 26)
FONT_30 = pygame.font.SysFont('Helvetica', 30)
FONT_36 = pygame.font.SysFont('Helvetica', 36)

smallfont = pygame.font.SysFont('Corbel',35)



fontSmall = pygame.font.Font('freesansbold.ttf', 11)
FONT_20 = pygame.font.SysFont('HelveticaNeue', 20)
FONT2 = pygame.font.SysFont('Helvetica', 14,bold=False)
VOLTAGE_FONT = pygame.font.SysFont('Helvetica', 12)
FONT_BRIGHTNESS = pygame.font.SysFont('Helvetica', 15,bold=False)

FONT_TIME = pygame.font.SysFont('Helvetica', 24, bold=True)
FONT_DAY = pygame.font.SysFont('Helvetica', 18, bold=True)
FONT_DATE = pygame.font.SysFont('Helvetica', 22, bold=False)


TEMP_FONT=pygame.font.SysFont('Helvetica', 30)
HELVETICA=pygame.font.SysFont('Helvetica', 30)
FONT_UNITS=pygame.font.SysFont('Helvetica', 18)

font_names=['wifi_font.ttf','Trekbats.ttf','Okuda Bold Italic.otf','Okuda Bold.otf','Okuda Italic.otf','Okuda.otf','Klingon.ttf','LCARS.ttf','din-condensed-light.otf','din-1451-fette-breitschrift-1936.ttf','Borg.ttf','Fabrini.ttf','Dominion.ttf','Ferengi.ttf','Cardassian.ttf','Bajoran.ttf','Federation.ttf','Romulan.ttf']

star_trek_fonts={}

for curr_font in font_names:
    font=pygame.freetype.Font(HOME_DIR+"assets/fonts/"+curr_font)
    star_trek_fonts[curr_font.split('.')[0]]=font


WIFI_FONT=star_trek_fonts['wifi_font']
FONT_FEDERATION=star_trek_fonts['Federation']
FONT_OKUDA=star_trek_fonts['Okuda']
FONT_OKUDA_BOLD=star_trek_fonts['Okuda Bold']
FONT_DIN=star_trek_fonts['din-1451-fette-breitschrift-1936']

FONT_HELVETICA_NEUE=pygame.freetype.Font(HOME_DIR+"assets/fonts/"+'HelveticaNeue.ttc')