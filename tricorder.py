#!/usr/bin/python3
import pygame
import pygame.freetype
import sys
import os
import time, datetime
from subprocess import PIPE, Popen
from threading import Thread
import pigpio
# from bluetooth import *
import trace
import threading
import signal
import csv
# from timeit import timeit

from paths_and_utils import *
sys.path.insert(1,HOME_DIR+'freqshow_code/')
sys.path.insert(1,HOME_DIR+'assets/')
sys.path.insert(1,HOME_DIR+'resources/')
sys.path.insert(1,HOME_DIR+'sensor_pages/')
sys.path.insert(1,HOME_DIR+'general_pages/')


# set up logging
from my_logging import *
shivams_logging(script_name="tricorder",console_log_level="info",logfile_log_level="info")
logging.info (f'\n')   # newline for easier readability

from serial_manager import ser,get_battery, my_flush
from mappings import *
from fonts import smallfont

from images import *
from custom_user_events import TOGGLE_SCREEN,SET_BACKLIGHT,GET_BACKLIGHT_QUICK_MENU,GO_TO_SLEEP,SCREENSHOT_EVENT,ENTERING_HOME_PAGE,FILE_LOG_EVENT
from global_functions import *

# ============== import pages ==============#
from page_templates import PageTemplate,PageWithoutGauge,DeviceStatsPageTemplate,NumPadPage
from sdr_page import SoftwareDefinedRadioPage
from thermal_cam_page import ThermalCamPage
from pm25_page import PM25Page
from noise_page import NoiseSensorPage
from wind_page import WindSensorPage
from spectrometer_page import SpecPage
from temp_humid_page import TempHumidPage
from pressure_page import PressureSensorPage
from uv_page import UVSensorPage
from vis_ir_page import LightSensorPage
from voc_page import VOCSensorPage
from imu_page import IMUSensorPage
from gps_page import *
from radiation_page import *
from weight_page import *
from lidar_page import *
from battery_page import *
from multimeter_page import *
from object_detection_page import *
from fly_page import *
# ---
from developer_page import *
from home_page import *
from sleep_page import *
from exit_page import *
from device_stats_page import *
from settings_page import *
from brightness_slider_page import *
from menu_home_page import *
from quick_menu_page import *
from file_browser_page import *
# ===================== Helper Classes =============================== #
class thread_with_trace(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

def start(self):
	self.__run_backup = self.run
	self.run = self.__run
	threading.Thread.start(self)

def __run(self):
	sys.settrace(self.globaltrace)
	self.__run_backup()
	self.run = self.__run_backup

def globaltrace(self, frame, event, arg):
	if event == 'call':
	  return self.localtrace
	else:
	  return None

def localtrace(self, frame, event, arg):
	if self.killed:
		if event == 'line':
			raise SystemExit()
	return self.localtrace

def kill(self):
	self.killed = True

class DeviceInfoClass():
	def __init__(self):
		self.wifi_name=get_wifi_name()
		# self.day,self.date,self.time=get_date_time()
		self.cpu_pct,self.cpu_temp=update_cpu_stats()
		self.wifi_tics=100
		self.cpu_tics=30

		self.curr_brightness=-1
		self.bluetooth_connected=False
		self.wr_count=0

		self.battery_stats_tics=600
		self.batt_volt=-1
		self.batt_pct=-1
		self.batt_temp=-1

	def blit_bluetooth_status(self,screen,x_pos):
		if self.bluetooth_connected==False:
			screen.blit(bluetooth_img_not_connected,(x_pos-23,4))
		else:
			screen.blit(bluetooth_img,(x_pos-23,4))

	def get_bluetooth_status(self):
		if self.bluetooth_connected:
			b_img=bluetooth_img
		else:
			b_img=bluetooth_img_not_connected
		return b_img

	def read_battery(self,screen,frame_count):
		# ------ Battery ------ #
		screen.blit(no_battery,(10,5))

		batt_string=str(self.batt_pct)+"% / "+\
					str(self.batt_volt)+"V / "+\
					str(self.batt_temp)+"°C"

		FONT_OKUDA.render_to(screen, (50, 11), batt_string, WHITE,style=1,size=26)

		try:
			if frame_count%self.battery_stats_tics==0:
				self.batt_volt,self.batt_pct,self.batt_temp=get_battery()
				# writing to csv file
				if (self.batt_volt>0):
					now = datetime.datetime.now()
					date=now.strftime('%m/%d/%y')
					hour_min=now.strftime('%-I:%M:%S %p')
					with open("batt_history.csv", 'a+') as csvfile:
						csvfile.write(f"{date},{hour_min},{self.batt_volt},{self.batt_pct},{self.batt_temp}\n")
					csvfile.close()
		except Exception as e:
			logging.error (e)

	def update(self,screen,frame_count,bluetooth_count):

		if frame_count%self.wifi_tics==0:
			self.wifi_name=get_wifi_name()
		if frame_count%self.cpu_tics==0:
			self.cpu_pct,self.cpu_temp=update_cpu_stats()

		self.day,self.date,self.time=get_date_time()

		width=screen.get_width()	# Used for aligning text

		# Mouse pos
		mouse_pos_txt=smallfont.render('(x,y): '+str(pygame.mouse.get_pos()), True , WHITE)
		screen.blit(mouse_pos_txt , (180,36))

		day,date,hour_sec=get_date_time()

		w,w2=blit_some_stats(screen,width,day,date,hour_sec,str(round(clock.get_fps(),2)),self.cpu_pct,self.cpu_temp,self.wifi_name,'I',self.get_bluetooth_status())

		# # Show bluetooth count
		# count_txt=FONT_18.render(str(bluetooth_count),1,WHITE)
		# screen.blit(count_txt,(200,5))

		# # Show write count
		# txt_surf,w3,h=get_text_dimensions(text='WR: '+str(self.wr_count),font_style=FONT_OKUDA,font_color=WHITE,style=0,font_size=22)
		# screen.blit(txt_surf,(width-w-w2-w3-60,11))

		# Backlight
		curr_brightness_pct=str(int(round(100*(self.curr_brightness/255),0)))+"%"
		FONT_OKUDA.render_to(screen, (500+28, 11), str(curr_brightness_pct), WHITE,style=1,size=26)
		screen.blit(brightness_icon,(500,6))

		self.read_battery(screen,frame_count)

# ==================================================================== #
class WindowManager():
	def __init__(self,fullscreen_en=False):

		self.ser=ser
		# # Set periodic event for logging to file (in ms)
		# pygame.time.set_timer(FILE_LOG_EVENT, 20000)
		pygame.event.set_blocked(pygame.VIDEOEXPOSE)

		# Display related
		self.fullscreen_en=fullscreen_en
		self.screen_dict,self.curr_screen=self.init_pages()
		self.screen=self.init_screen()
		self.next_screen=self.curr_screen
		lcars_bg.set_colorkey(BLACK)
		# print ('pygame.display.get_allow_screensaver(): ',pygame.display.get_allow_screensaver())

		# Convenient struct to store device stats
		self.DeviceInfo=DeviceInfoClass()

		# Retrieve backlight level
		self.DeviceInfo.curr_brightness=self.screen_dict['brightness_slider_page'].get_current_brightness()

		# For restoring backlight level after wake from sleep
		if self.DeviceInfo.curr_brightness==0:
			self.backlight_restore_level=128
		else:
			self.backlight_restore_level=self.DeviceInfo.curr_brightness

		# Other variables
		self.kwargs={'test_kwarg':-1}
		self.show_mouse=True
		self.client_sock=None
		self.prev_time=0
		self.bluetooth_count=0
		self.frame_count=0
		self.override=False
		self.take_screenshot=False

		self.screenshot_overlay=self.init_screenshot_overlay()
		self.sensor_dict=SENSOR_DICT	# used for home_page


		# # Start bluetooth search in new thread
		# if PERIPHERAL_MODE=='bluetooth':
		# 	try:
		# 		global t1
		# 		t1 = thread_with_trace(target = self.connect_bluetooth)
		# 		t1.daemon=True #This closed thread when main thread exits
		# 		t1.setName('connect_bluetooth')
		# 		t1.start()
		# 	except (KeyboardInterrupt, SystemExit):
		# 		t1.kill()
		# 		print (t1.is_alive())
		# 		print ('closing bluetooth thread')
		# 		sys.exit()
		# elif PERIPHERAL_MODE=='serial':
		# 	global ser
		# 	ser = serial.Serial(
		# 		port=USB_SERIAL_PORT, # Change this according to connection methods, e.g. /dev/ttyUSB0
		# 		baudrate = 115200,
		# 		parity=serial.PARITY_NONE,
		# 		stopbits=serial.STOPBITS_ONE,
		# 		bytesize=serial.EIGHTBITS,
		# 		timeout=1
		# 	)
		# pygame.event.post(BLUETOOTH_CONNECTED)

	def init_screen(self):
		pygame.display.quit()
		pygame.display.init()

		modes = pygame.display.list_modes()
		self.color_depth=pygame.display.mode_ok(modes[0])

		if not self.fullscreen_en:
			screen=pygame.display.set_mode(STARTING_RES,   pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT, depth=self.color_depth)
		else:
			screen=pygame.display.set_mode(FULL_SCREEN_RES, pygame.FULLSCREEN |  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT, depth=self.color_depth)
		starfleet_logo.convert()
		pygame.display.set_icon(starfleet_logo_small)
		pygame.display.set_caption("Tricorder")
		# logging.warning(modes)
		# logging.warning (f"\nscreen: {screen}")
		# # logging.warning (f"\nscreen.color_depth: {screen.color_depth}")
		# logging.warning (f"\npygame.display: {pygame.display}")
		# logging.warning(pygame.display.get_wm_info())
		# logging.warning (f"\npygame.display.mode_ok(modes[0]): {pygame.display.mode_ok(modes[0])}")

		self.screen_dict['quick_menu_page'].fullscreen_en=self.fullscreen_en

		return screen

	def init_pages(self):
	# instantiate all pages
		self.sensor_pages_list=[ThermalCamPage('thermal_cam_page'),
					 LightSensorPage('light_sensor_page'),
					 UVSensorPage('uv_sensor_page'),
					 PM25Page('pm25_sensor_page'),
					 PressureSensorPage('pressure_sensor_page'),
					 SpecPage('spectrometer_page'),
					 TempHumidPage('temp_humid_page'),
					 WindSensorPage('wind_sensor_page'),
					 NoiseSensorPage('noise_page'),
					 VOCSensorPage('tvoc_eco2_page'),
					 SoftwareDefinedRadioPage('sdr_page'),
					 IMUSensorPage('imu_sensor_page'),
					 GPSSensorPage('gps_sensor_page'),
					 GeigerCounterPage('radiation_sensor_page'),
					 WeightSensorPage('weight_sensor_page'),
					 LidarSensorPage('lidar_sensor_page'),
					 BatterySensorPage('battery_sensor_page'),
					 MultimeterPage('multimeter_page'),
					 ObjectDetectionPage('object_detection_page'),
					 FlyPage('fly_page'),
					 DeveloperPage('developer_page'),
					 MenuHomePageClass('menu_home_page')]

		screen_list=self.sensor_pages_list+[HomePage('home_page'),
											 QuickMenuPage('quick_menu_page'),
											 FileBrowserPage('file_browser_page'),
											 SettingsPage('settings_page'),
											 DeviceStatsPage('device_stats_page'),
											 NumPadPage('numpad_page'),
											 BrightnessSliderPage('brightness_slider_page'),
											 SleepPage('sleep_page'),
											 ExitPage('exit')   #placeholder
											]

		screen_dict={}
		for scr in screen_list:
			screen_dict[scr.name]=scr
			scr.bluetooth_connected=False

		return screen_dict,screen_dict['menu_home_page']

	def init_screenshot_overlay(self):
		s=pygame.Surface(FULL_SCREEN_RES)
		s.set_alpha(128) # half of max opacity
		s.fill(WHITE)	 # white color
		return s

	def generic_event_handler(self,curr_events):
		screen=self.screen
		for event in curr_events:

			# -------------------------------- Keyboard Events ------------------------------ #
			if event.type == pygame.KEYUP:
				if (event.key == pygame.K_ESCAPE or event.key==ord('q')):
					self.screen_dict['exit'].next_frame('','',kwargs={'prev_page_name':self.curr_screen.name})

				if (event.key==ord('m')):
					self.next_screen=self.screen_dict['menu_home_page']

				if (event.key==ord('h')):
					self.next_screen=self.screen_dict['home_page']

				if (event.key==ord('f')):
					self.fullscreen_en= not self.fullscreen_en
					self.screen=self.init_screen()
					curr_events.remove(event)

				if (event.key==ord('z')):
					curr_events.remove(event)
					self.minimize()

				if (event.key==ord('s')):
					curr_events.remove(event)
					self.take_screenshot=True

			if event.type == pygame.QUIT:
				# self.screen_dict['exit'].next_frame('','')
				self.screen_dict['exit'].next_frame('','',kwargs={'prev_page_name':self.curr_screen.name})

			if event==ENTERING_HOME_PAGE:
				curr_events.remove(event)
				self.screen_dict['home_page'].bluetooth_count=0

			# Log to file
			if event.type==pygame.USEREVENT + 1:
				curr_events.remove(event)
				if self.curr_screen!=self.screen_dict['thermal_cam_page']:
					if (self.client_sock!=None):
						self.screen.blit(rolling_tics_icon,(2,206))
						try:
							t0 = thread_with_trace(target =  self.log_to_file)
							t0.setName('log to file')
							t0.start()
						except Exception as e:
							raise(e)

			if event==TOGGLE_SCREEN:
				curr_events.remove(event)
				self.fullscreen_en=not self.fullscreen_en
				self.screen=self.init_screen()
				print (self.screen)

			if event==GO_TO_SLEEP:
				logging.info ('GO_TO_SLEEP!!!')
				MODE='sleep'
				self.backlight_restore_level=self.screen_dict['brightness_slider_page'].get_current_brightness()
				self.screen_dict['brightness_slider_page'].set_brightness(0)
				self.DeviceInfo.curr_brightness=self.screen_dict['brightness_slider_page'].get_current_brightness()
				curr_events.remove(event)
				ser.write(MCU_SLEEP_CODE.encode('utf-8'))
				ser.readline()

			if event==SET_BACKLIGHT:
				# print('SET_BACKLIGHT')
				c=self.screen_dict['brightness_slider_page'].get_current_brightness()
				self.DeviceInfo.curr_brightness=c
				self.screen_dict['quick_menu_page'].backlight_lvl=c
				curr_events.remove(event)

			if event==GET_BACKLIGHT_QUICK_MENU:
				self.screen_dict['quick_menu_page'].backlight_lvl=self.screen_dict['brightness_slider_page'].get_current_brightness()
				curr_events.remove(event)

			if event == SCREENSHOT_EVENT:
				curr_events.remove(event)
				logging.warning ('SCREENSHOT_EVENT')
				self.take_screenshot=True

			if event.type==pygame.VIDEOEXPOSE:
				curr_events.remove(event)

			if event.type==FILE_LOG_EVENT:
				# curr_events.remove(event)
				logging.info('FILE_LOG_EVENT')

			if event.type in [pygame.FINGERDOWN,pygame.FINGERUP,pygame.FINGERMOTION, pygame.MULTIGESTURE]:
				if (self.show_mouse==True):
					self.show_mouse=False
					pygame.mouse.set_visible(self.show_mouse)

			if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL, pygame.MOUSEMOTION]:
				if (self.show_mouse==False):
					self.show_mouse=True
					pygame.mouse.set_visible(self.show_mouse)

		return(curr_events)

	def next_frame_main(self):

		next_screen_name=self.curr_screen.name
		self.curr_screen=self.next_screen

		self.screen.fill(BLACK)
		self.screen.blit(lcars_bg,(0,0))
		# curr_events=self.sensor_event_handler(pygame.event.get())
		curr_events=pygame.event.get()

		# ---- screen specific ---- #
		next_screen_name,self.kwargs=self.curr_screen.next_frame(self.screen,curr_events,**self.kwargs)
		self.next_screen=self.screen_dict[next_screen_name]

		if next_screen_name!=self.curr_screen.name:
			try:
				self.curr_screen.on_exit()
			except  AttributeError:
				logging.error ("AttributeError on_exit:"+self.curr_screen.name)

			try:
				self.next_screen.on_enter()
			except  AttributeError:
				logging.error ("AttributeError on_enter:"+self.curr_screen.name)

		curr_events=self.generic_event_handler(curr_events)

		for screen_name,screen in self.screen_dict.items():
			try:
				for butt in screen.button_list:
					if butt.cooldown_val>0:
						butt.cooldown_val-=1
			except Exception as e:
				logging.error (f"{self.__class__.__name__}:{e}")

		self.DeviceInfo.update(self.screen,self.frame_count,self.bluetooth_count)

		if self.take_screenshot:
			self.take_screenshot=False
			self.take_screenshot_func()
			self.screen.blit(self.screenshot_overlay,(0,0))



		self.frame_count+=1
		return self.screen

	# ------------------------ #
	def check_make_file(self):
		#Check if log file exists
		now = datetime.datetime.now()
		date=now.strftime('%m/%d/%y')
		hour_sec=now.strftime('%H:%M:%S')

		log_file_name=LOGS_DIR+LOG_FILE_PREFIX+date.replace('/','_')+'.csv'
		LOG_FILE_EXISTS=os.path.isfile(log_file_name)

		if (LOG_FILE_EXISTS):
			log_file=open(log_file_name,'a+')
		else:
			log_file=open(log_file_name,'w')
			log_file.write(header_row+'\n')
		return log_file

	def log_to_file(self):
		sensor_dict=self.get_bluetooth_vals('L U T P M V S ')
		# ser.flush()
		# print (sensor_dict)
		if sensor_dict!=None:
			t=get_date_time()
			o_str=t[0]+','+t[1]+','+t[2]+','
			for k,v in sensor_dict.items():
				o_str+=str(v)+','
			o_str.rstrip(',')
			o_str+='\n'

			log_file=self.check_make_file()
			try:
				with open(log_file.name,'a+') as f:
					f.write(o_str)
					f.close()
				# print ('write')
				self.DeviceInfo.wr_count+=1
				# print ('write to ',log_file.name)
			except:
				logging.error ('no write')
				return 'XX'
			return('wr')

	def minimize(self):
		logging.info("minimizing")
		pygame.display.set_icon(starfleet_logo)
		pygame.display.iconify()

	def take_screenshot_func(self):
		rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
		sub = self.screen.subsurface(rect)
		dd=get_date_time()

		kk='screenshots/'+self.curr_screen.name
		name= kk+f'_{dd[0]} {dd[1]} {dd[2]}.png'.replace(':','_').replace(' ','_')
		logging.warning (f'screenshot:{name}')

		pygame.image.save(sub,name)
		self.screen.blit(camera,(20,160))

# ==================================================================== #

if __name__=='__main__':

	global MODE

	MODE='normal'

	fullscreen_en=False

	W=WindowManager(fullscreen_en)

	try:
		while True:
			W.screen=W.next_frame_main()
			pygame.display.update()

			if MODE=='sleep':
				clock.tick(1)	# slow down execution. if too slow -> wake from touch also slow
			else:
				# pygame.display.update()
				# clock.tick_busy_loop()
				clock.tick()

	except SystemExit:
		logging.info ('exiting')
		# ser.write(MCU_SLEEP_CODE.encode('utf-8'))
	except KeyboardInterrupt:
		logging.warning ('KeyboardInterrupt exiting')
		wrap_up()
		# ser.write(MCU_SLEEP_CODE.encode('utf-8'))
	except Exception as e:
		logging.error (f'Caught exception: {e}')

		x=PIGPIO.get_PWM_dutycycle(BACKLIGHT_PIN)
		logging.error (f'BACKLIGHT: {x}')
		if x<128:
			PIGPIO.set_PWM_dutycycle(BACKLIGHT_PIN, 128)

		raise (e)
