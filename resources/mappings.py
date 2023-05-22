'''!
The RaspberryPi and MCU communicate by exchanging pre-determined codes over wired/bluetooth serial connections.\n
Each functopm (output or input) is represented by unique identifier.
'''

import pygame
pygame.init()

# Following vars are for backlight
import pigpio
PIGPIO=pigpio.pi()

d={}	# This makes two-way referencing easier

HELP_CODE ='H'
VERBOSE_CODE ='B'

d['VIS_IR_CODE']      ='L'
d['UV_CODE']          ='U'
d['SPEC_CODE']        ='S'
d['TEMP_HUMID_CODE']  ='T'
d['PRESSURE_CODE']    ='P'
d['PM25_CODE']        ='M'
d['TVOC_CODE']        ='V'
d['THERMAL_CAM_CODE'] ='R'
WIND_CODE             ='#'
d['NOISE_CODE']       ='$'

TSL_SCL_DISCONNECT_CODE ='&'
TSL_SCL_CONNECT_CODE    ='A'

PM25_PWR_ON_CODE='F'
PM25_PWR_OFF_CODE='H'

d['IMU_ORIENTATION_CODE']="O"
d['IMU_ANG_VEL_CODE'] = 'Q'
d['IMU_LIN_ACC_CODE'] = 'W'
d['IMU_MAG_CODE'] = 'X'
d['IMU_ACC_CODE'] = 'Y'
d['IMU_GRAV_CODE'] = 'Z'

d['RADIATION_CODE'] = 'g'
GEIGER_PWR_ON_CODE='I'
GEIGER_PWR_OFF_CODE='J'

d['GPS_CODE']='G'
d['BATTERY_CODE']='B'
d['CURRENT_CODE']='c'

MCU_SLEEP_CODE='^'
MCU_WAKE_CODE='('
MCU_RESET_CODE='~'
MCU_IND_MODE_ENABLE='>'
MCU_IND_MODE_DISABLE='<'

# -------------- UV -------------- #
SET_LTR390_GAIN_1='1'
SET_LTR390_GAIN_3='2'
SET_LTR390_GAIN_6='3'
SET_LTR390_GAIN_9='4'
SET_LTR390_GAIN_18='5'
SET_LTR390_RESOLUTION_20BIT='6'
SET_LTR390_RESOLUTION_19BIT='7'
SET_LTR390_RESOLUTION_18BIT='8'
SET_LTR390_RESOLUTION_17BIT='9'
SET_LTR390_RESOLUTION_16BIT='0'
SET_LTR390_RESOLUTION_13BIT='!'
# -------------------------------- #

# this makes logging easier
d_inv={}
for key, val in d.items():
	d_inv[val]=key

# --- SENSOR CODES --- #
# Light        = L
# UV           = U
# Spectrometer = S
# Temp/Humid   = T
# Pressure     = P
# PM25         = M
# TVOC/eCO2    = V

# --- LIGHT CODES --- #
# Light        = L
# Light Gain   = L_G_(val)

# --- UV CODES --- #
# UV       = U
# UV Gain  = U_G_(val)
# UV Res   = U_R_(val)
# UV Delay = U_D_(val)

# --- PRESSURE CODES --- #
# Pressure          = P
# Pres Oversampling = P_P_(val)
# Temp Oversampling = P_T_(val)

# --- TEMP/HUMID CODES --- #
# Temp/Humid = T
# Temp Res   = T_T_(val)
# Humid Res  = T_H_(val)
# Heater     = T_R_(val=0/1)

# --- SPECTROMETER CODES --- #
# Spectrometer      = S
# Spectrometer Gain = S_G_(val)