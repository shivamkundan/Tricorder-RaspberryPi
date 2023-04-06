HELP_CODE ='H'
VERBOSE_CODE ='B'

VIS_IR_CODE      ='L'
UV_CODE          ='U'
SPEC_CODE        ='S'
TEMP_HUMID_CODE  ='T'
PRESSURE_CODE    ='P'
PM25_CODE        ='M'
TVOC_CODE        ='V'
THERMAL_CAM_CODE ='R'
WIND_CODE        ='#'
NOISE_CODE       ='$'

TSL_SCL_DISCONNECT_CODE='&'
TSL_SCL_CONNECT_CODE='A'

PM25_PWR_ON_CODE='F'
PM25_PWR_OFF_CODE='H'

IMU_ORIENTATION_CODE="O"

IMU_ANG_VEL_CODE = 'Q'
IMU_LIN_ACC_CODE = 'W'
IMU_MAG_CODE = 'X'
IMU_ACC_CODE = 'Y'
IMU_GRAV_CODE = 'Z'

RADIATION_CODE = 'g'
GEIGER_PWR_ON_CODE='I'
GEIGER_PWR_OFF_CODE='J'

GPS_CODE='G'
BATTERY_CODE='B'
CURRENT_CODE='c'


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