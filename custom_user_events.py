'''
This file contains my custom defined events
'''
from pygame.event import Event
from pygame import USEREVENT

# ---------------------------- Device handling ---------------------------- #
TOGGLE_SCREEN=Event(USEREVENT, attr1='TOGGLE_SCREEN')
SET_BACKLIGHT=Event(USEREVENT, attr1='SET_BACKLIGHT')
GET_BACKLIGHT_QUICK_MENU=Event(USEREVENT, attr1='GET_BACKLIGHT_QUICK_MENU')
GO_TO_SLEEP=Event(USEREVENT, attr1='GO_TO_SLEEP')
WAKE_FROM_SLEEP=Event(USEREVENT, attr1='WAKE_FROM_SLEEP')
SCREENSHOT_EVENT=Event(USEREVENT, attr1='SCREENSHOT_EVENT')

# ---------------------------- Bluetooth management---------------------------- #
REQUEST_BLUETOOTH=Event(USEREVENT, attr1='REQUEST_BLUETOOTH')
BLUETOOTH_CONNECTED=Event(USEREVENT, attr1='BLUETOOTH_CONNECTED')
BLUETOOTH_DISCONNECTED=Event(USEREVENT, attr1='BLUETOOTH_DISCONNECTED')

# ---------------------------- Page navigation ---------------------------- #
# ENTERING_FILES_PAGE=Event(USEREVENT, attr1='ENTERING_FILES_PAGE')
# ENTERING_THERMAL_PAGE=Event(USEREVENT, attr1='ENTERING_THERMAL_PAGE')
ENTERING_HOME_PAGE=Event(USEREVENT, attr1='ENTERING_HOME_PAGE')
# LEAVING_FILES_PAGE=Event(USEREVENT, attr1='LEAVING_FILES_PAGE')
# LEAVING_THERMAL_PAGE=Event(USEREVENT, attr1='LEAVING_THERMAL_PAGE')
# LEAVING_HOME_PAGE=Event(USEREVENT, attr1='LEAVING_HOME_PAGE')

FILE_LOG_EVENT= USEREVENT + 1

# ---------------------------- Send sensor settings  ---------------------------- #
SET_LIGHT_SENSOR_GAIN=Event(USEREVENT, attr1='SET_LIGHT_SENSOR_GAIN')
SET_PRESSURE=Event(USEREVENT, attr1='SET_PRESSURE')
SET_UV_GAIN=Event(USEREVENT, attr1='SET_UV_GAIN')
SET_TEMP_SETTINGS=Event(USEREVENT, attr1='SET_TEMP_SETTINGS')

# ---------------------------- Receive sensor vslues ---------------------------- #
REQUEST_VIS_IR=Event(USEREVENT, attr1='REQUEST_VIS_IR')
REQUEST_UV=Event(USEREVENT, attr1='REQUEST_UV')
REQUEST_SPECTROMETER=Event(USEREVENT, attr1='REQUEST_SPECTROMETER')
REQUEST_PM25=Event(USEREVENT, attr1='REQUEST_PM25')
REQUEST_PRESSURE=Event(USEREVENT, attr1='REQUEST_PRESSURE')
REQUEST_TEMP_HUMID=Event(USEREVENT, attr1='REQUEST_TEMP_HUMID')
REQUEST_TVOC_ECO2=Event(USEREVENT, attr1='REQUEST_TVOC_ECO2')
REQUEST_WIND=Event(USEREVENT, attr1='REQUEST_WIND')
REQUEST_RADIATION=Event(USEREVENT, attr1='REQUEST_RADIATION')
REQUEST_NOISE=Event(USEREVENT, attr1='REQUEST_NOISE')

REQUEST_IMU_ORIENTATION=Event(USEREVENT, attr1='REQUEST_IMU_ORIENTATION')
REQUEST_IMU_ANG_VEL=Event(USEREVENT, attr1='REQUEST_IMU_ANG_VEL')
REQUEST_IMU_LIN_ACC=Event(USEREVENT, attr1='REQUEST_IMU_LIN_ACC')
REQUEST_IMU_MAG=Event(USEREVENT, attr1='REQUEST_IMU_MAG')
REQUEST_IMU_ACC=Event(USEREVENT, attr1='REQUEST_IMU_ACC')
REQUEST_IMU_GRAV=Event(USEREVENT, attr1='REQUEST_IMU_GRAV')

REQUEST_GPS=Event(USEREVENT, attr1='REQUEST_GPS')
REQUEST_BATTERY=Event(USEREVENT, attr1='REQUEST_BATTERY')
REQUEST_CURRENT=Event(USEREVENT, attr1='REQUEST_CURRENT')
REQUEST_FLY_DATA=Event(USEREVENT, attr1='REQUEST_FLY_DATA')


POWER_TSL_ON=Event(USEREVENT, attr1='POWER_TSL_ON')
POWER_TSL_OFF=Event(USEREVENT, attr1='POWER_TSL_OFF')
POWER_PM25_ON=Event(USEREVENT, attr1='POWER_PM25_ON')
POWER_PM25_OFF=Event(USEREVENT, attr1='POWER_PM25_OFF')