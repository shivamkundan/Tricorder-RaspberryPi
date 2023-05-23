'''! @brief This is where fonts are loaded defined
@file fonts.py Font definitions
@dir saved_fonts Contains custom font files.
'''

import sys, os
import pygame
import pygame.freetype
# from paths_and_utils import

os.environ['PYGAME_FREETYPE'] = '1'

pygame.init()
HOME_DIR="/home/pi/Sensor_Scripts/pygame_code/tricorder/"
FONTS_DIR=HOME_DIR+"assets/saved_fonts/"


number_keys=[pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,\
                pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]

# ----------------- Fonts ----------------- #
FONT = pygame.font.SysFont('/home/pi/Sensor_Scripts/pygame_code/tricorder/assets/saved_fonts/HelveticaNeue.ttf', 12,bold=False)
# FONT = pygame.font.SysFont('Helvetica', 12)
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
# FONT_20 = pygame.font.SysFont('Helvetica', 20)
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

font_names=['wifi_font.ttf','Trekbats.ttf','Okuda Bold Italic.otf','Okuda Bold.otf',\
            'Okuda Italic.otf','Okuda.otf','Klingon.ttf','LCARS.ttf','din-condensed-light.otf',\
            'din-1451-fette-breitschrift-1936.ttf','Borg.ttf','Fabrini.ttf','Dominion.ttf',\
            'Ferengi.ttf','Cardassian.ttf','Bajoran.ttf','Federation.ttf','Romulan.ttf']

star_trek_fonts={}

for curr_font in font_names:
    font=pygame.freetype.Font(FONTS_DIR+curr_font)
    star_trek_fonts[curr_font.split('.')[0]]=font


WIFI_FONT=star_trek_fonts['wifi_font']
FONT_FEDERATION=star_trek_fonts['Federation']
FONT_OKUDA=star_trek_fonts['Okuda']
FONT_OKUDA_BOLD=star_trek_fonts['Okuda Bold']
FONT_DIN=star_trek_fonts['din-1451-fette-breitschrift-1936']

# print (star_trek_fonts.keys())

FONT_HELVETICA_NEUE=pygame.freetype.Font(FONTS_DIR+'HelveticaNeue.ttc')