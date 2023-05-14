'''
Communication with the microcontroller is event based.\n
Certain device controls are also event based.\n
This file contains my custom defined events.
'''

from pygame.event import Event
from pygame import USEREVENT

# ---------------------------- Device handling ---------------------------- #
TOGGLE_SCREEN=Event(USEREVENT, attr1='TOGGLE_SCREEN')
SET_BACKLIGHT=Event(USEREVENT, attr1='SET_BACKLIGHT')
GET_BACKLIGHT_QUICK_MENU=Event(USEREVENT, attr1='GET_BACKLIGHT_QUICK_MENU')
GO_TO_SLEEP=Event(USEREVENT, attr1='GO_TO_SLEEP')
SCREENSHOT_EVENT=Event(USEREVENT, attr1='SCREENSHOT_EVENT')

# ---------------------------- Bluetooth management---------------------------- #
REQUEST_BLUETOOTH=Event(USEREVENT, attr1='REQUEST_BLUETOOTH')
BLUETOOTH_CONNECTED=Event(USEREVENT, attr1='BLUETOOTH_CONNECTED')
BLUETOOTH_DISCONNECTED=Event(USEREVENT, attr1='BLUETOOTH_DISCONNECTED')

# ---------------------------- File stuff ---------------------------- #
ENTERING_HOME_PAGE=Event(USEREVENT, attr1='ENTERING_HOME_PAGE')
FILE_LOG_EVENT= USEREVENT + 1

# ---------------------------- Send sensor settings  ---------------------------- #
SET_LIGHT_SENSOR_GAIN=Event(USEREVENT, attr1='SET_LIGHT_SENSOR_GAIN')
SET_PRESSURE=Event(USEREVENT, attr1='SET_PRESSURE')
SET_UV_GAIN=Event(USEREVENT, attr1='SET_UV_GAIN')
SET_TEMP_SETTINGS=Event(USEREVENT, attr1='SET_TEMP_SETTINGS')

# # ---------------------------- Receive sensor vslues ---------------------------- #s
POWER_TSL_ON=Event(USEREVENT, attr1='POWER_TSL_ON')
POWER_TSL_OFF=Event(USEREVENT, attr1='POWER_TSL_OFF')
POWER_PM25_ON=Event(USEREVENT, attr1='POWER_PM25_ON')
POWER_PM25_OFF=Event(USEREVENT, attr1='POWER_PM25_OFF')
