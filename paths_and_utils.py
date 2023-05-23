'''! @brief This file contains paths and other definitions.
@file paths_and_utils.py Contains paths and other definitions.
'''
import pygame
## Pygame clock object.
clock=pygame.time.Clock()

## Main program directory, all other paths are relative to this.
HOME_DIR="/home/pi/Sensor_Scripts/pygame_code/tricorder/"
## For bluetooth serial connection this is the max per msg.
MAX_BYTES=1016
## options: serial, bluetooth.
PERIPHERAL_MODE="serial"
## Non full screen window resolution.
STARTING_RES=(680,640)
## Full-screen window resolution.
FULL_SCREEN_RES=(720,720)
## For software PWM pigpio.
BACKLIGHT_PIN=19

## For recording sensor values to file.
LOGS_DIR="/home/pi/Sensor_Scripts/logs/"
## Column titles
header_row="day,date,time,lux,infrared,visible,full_spectrum,uvs,light,gain,uvi,ltr_lux,channel_415nm,channel_445nm,channel_480nm,channel_515nm,channel_555nm,channel_590nm,channel_630nm,channel_680nm,temperature,relative_humidity,pressure,bmp_temperature,03um,05um,10um,25um,50um,100um,eCO2,TVOC,baseline_eCO2,baseline_TVOC\n"
## Log file name prefix.
LOG_FILE_PREFIX="sensors_log_home_"
## Path to where fonts are stored
FONTS_DIR=HOME_DIR+"assets/saved_fonts/"
## File to store battery voltage/pct.
BATT_HIST_FILE=HOME_DIR+"batt_history.csv"

# -------------------------- Images -------------------------- #
## Path to where images are stored.
IMG_PATH=HOME_DIR+"assets/pics/"
## Path to where button images are stored.
BTN_PATH=IMG_PATH+"btn_pics/"
## Path to where menu page icons are stored.
ICONS_PATH=BTN_PATH+"mobile_style_icons/"

## This dictionary used for home_page
SENSOR_DICT={'lux':"-1",'infrared':"-1",'visible':"-1",'full_spectrum':"-1",'tsl2591_gain':"-1",
					 'uvs':"-1",'light':"-1",'uvi':"-1",'ltr_lux':"-1",'ltr_gain':"-1",'ltr_res':"-1",'ltr_win_fac':"-1",'ltr_mdelay':"-1",
					 'c_415nm':"-1",'c_445nm':"-1",'c_480nm':"-1",'c_515nm':"-1",'c_555nm':"-1",'c_590nm':"-1",'c_630nm':"-1",'c_680nm':"-1",'spec_gain':"-1",'FLICKER':"-1",
					 'temperature':"-1",'relative_humidity':"-1",'heater':"-1",'h_res':"-1",'t_res':"-1",
					 'pressure':"-1",'bmp_temp':"-1",'p_over':"-1",'t_over':"-1",
					 '03um':"-1",'05um':"-1",'10um':"-1",'25um':"-1",'50um':"-1",'100um':"-1",
					 'eCO2':"-1",'TVOC':"-1",'baseline_eCO2':"-1",'baseline_TVOC':"-1",}

# if __name__=="__main__":
# 	outstr=""
# 	for k,v in SENSOR_DICT.items():
# 		outstr+=f"\'{k}\',"
# 	print (outstr)