#!/usr/bin/python3
import pygame
import pygame.freetype
import sys
import os
import time, datetime
from subprocess import PIPE, Popen
from threading import Thread
import psutil
import pigpio
from bluetooth import *
import math
import trace
import threading
import signal
import csv

# ----- plotting libs ----- #
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# -------------- Plotting stuff -------------- #
COLOR = (0.75,0.75,0.75)
mpl.rcParams['font.size'] = 14
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

from paths_and_utils import *
sys.path.insert(1,HOME_DIR+'freqshow_code/')
sys.path.insert(1,HOME_DIR+'assets/')
sys.path.insert(1,HOME_DIR+'sensor_pages/')
sys.path.insert(1,HOME_DIR+'general_pages/')

# from pwmled.driver.gpio import GpioDriver
from mappings import *
from serial_manager import ser,get_battery, my_flush

from images import *
from aa_arc_gauge import *
from custom_user_events import *
from global_functions import *
from plotting_functions import *

# ============== import pages ==============#
from page_templates import *
from sdr_page import *
from thermal_cam_page import *
from pm25_page import *
from noise_page import *
from wind_page import WindSensorPage
from spectrometer_page import *
from temp_humid_page import TempHumidPage
from pressure_page import *
from uv_page import *
from vis_ir_page import *
from voc_page import *
from imu_page import *
from gps_page import *
from radiation_page import *
from weight_page import *
from lidar_page import *
from battery_page import *
from multimeter_page import *
from object_detection_page import *
from fly_page import *
from developer_page import *
from home_page import *
from sleep_page import *

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
				# pygame.event.post(REQUEST_BATTERY)
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

class SliderClass():
	def __init__(self,start_x,y_pos,button_width,button_height,length=100,min_val=0,max_val=249,start_val=None):
		self.start_x=start_x
		self.y_pos=y_pos
		self.length=length
		self.end_x=self.start_x+self.length

		self.button_width=button_width
		self.button_height=button_height
		self.button_surf, self.rectangle=self.initialize_button()

		if start_val!=None:
			self.rectangle.left=self.start_x+start_val-self.button_width//2
		else:
			self.rectangle.left=self.start_x+self.length//2-self.button_width//2
		self.rectangle.top=self.y_pos-self.button_height//2

		self.button_width_half=self.button_width//2

		self.linewidth=5
		padding_x=10
		padding_y=self.button_height
		mid=self.button_height//2
		self.line_rectangle=pygame.Rect(self.start_x-padding_x,self.y_pos-mid-padding_y//2, self.length+padding_x,self.linewidth+mid+padding_y)

		self.min_val=min_val
		self.max_val=max_val

		self.in_min=self.start_x-self.button_width_half
		self.in_max=self.start_x+self.length-self.button_width_half

	def initialize_button(self):

		# Button image
		w,h=self.button_width, self.button_height
		button_surf=pygame.Surface((w,h))
		r=pygame.Rect(0,0,w,h)
		pygame.draw.rect(button_surf,LIGHT_BLUE,r)
		rectangle=button_surf.get_rect()

		return (button_surf, rectangle)

	def blit_slider(self,screen,dx,scale=1):

		if 0<abs(dx)<200*scale:
			dx*=scale

			if self.start_x-self.button_width_half<=(self.rectangle.left+self.button_width_half+dx)<self.end_x+self.button_width_half-1:
				# print ('yes2 ',dx)
				self.rectangle.left+=dx

		# Blit the line
		lin=pygame.draw.line(screen, DARK_YELLOW, (self.start_x,self.y_pos), (self.end_x,self.y_pos), width=self.linewidth)

		# Blit the button
		screen.blit(self.button_surf,(self.rectangle.left,self.rectangle.top))

	def compute_percentage(self):

		pct=(((self.rectangle.left+self.button_width_half)-self.start_x)/self.length)

		if pct<0:
			pct=0
		if pct>0.99:
			pct=1
		num_val=int(round(pct*255,0))
		pct*=100
		if pct==0:
			log_val=0
		else:
			log_val=int(round(math.log(pct),0))

		return round(pct,2),num_val,log_val

	def map(self,x):
		out_min=self.min_val
		out_max=self.max_val
		in_min=self.in_min
		in_max=self.in_max
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# ====================== General Pages =============================== #

# Faux page for clean exit
class ExitPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)

	def next_frame(self,screen,curr_events,**kwargs):
		#  Disbale fullscreen
		if pygame.display.get_window_size()==FULL_SCREEN_RES:
			logging.info ('disabling full screen')
			pygame.display.toggle_fullscreen()

		wrap_up()
		pygame.quit()
		sys.exit()

# class SleepPage(PageTemplate):
# 	def __init__(self,name):
# 		super().__init__(name)
# 		self.event_list=[   pygame.FINGERDOWN,
# 							pygame.FINGERMOTION,
# 							pygame.FINGERUP,
# 							pygame.MULTIGESTURE,
# 							pygame.KEYDOWN,
# 							pygame.KEYUP,
# 							pygame.MOUSEBUTTONDOWN,
# 							# pygame.MOUSEMOTION,
# 							pygame.MOUSEBUTTONUP,
# 							# pygame.MOUSEWHEEL,
# 						]
# 		self.prev_page_name='menu_home_page'
# 		self.backlight_restore_level=255

# 	def handle_events(self,screen,curr_events):
# 		for event in curr_events:
# 			if event.type in self.event_list:
# 				# print (event)
# 				curr_events.remove(event)
# 				return True
# 		return False

# 	def on_enter(self):
# 		self.backlight_restore_level=PIGPIO.get_PWM_dutycycle(BACKLIGHT_PIN)

# 	def wake_from_sleep(self):
# 		logging.info("WAKE_FROM_SLEEP")
# 		PIGPIO.set_PWM_dutycycle(BACKLIGHT_PIN, self.backlight_restore_level)
# 		ser.write(MCU_RESET_CODE.encode('utf-8'))
# 		time.sleep(5)
# 		my_flush()
# 		ser.write(MCU_IND_MODE_DISABLE.encode('utf-8'))
# 		ser.flush()

# 	def next_frame(self,screen,curr_events,**kwargs):
# 		self.next_screen_name=self.name

# 		if 'prev_page_name' in kwargs.keys():
# 			self.prev_page_name=kwargs['prev_page_name']

# 		time.sleep(1)

# 		pressed_button=self.handle_events(screen,curr_events)
# 		if pressed_button==True:
# 			self.wake_from_sleep()


# 			self.next_screen_name=self.prev_page_name
# 			# print ('pressed: sleep->',self.next_screen_name)
# 			return self.next_screen_name,{}

# 		return self.next_screen_name,{}

class DeviceStatsPage(DeviceStatsPageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.pg_id=0
		# self.kwargs={} #reset kwargs
		# self.button_list+=self.init_buttons()
		self.prev_page_name='menu_home_page'

	def update_cpu_stats(self,dt=None):
		process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode()

		pos_start = output.index('=') + 1
		pos_end = output.rindex("'")

		cpu_temp = f'{float(output[pos_start:pos_end])}°C'
		cpu_pct=str(int(round(psutil.cpu_percent())))+'%'
		return cpu_pct,cpu_temp

	def update_up_time(self):
		process = Popen(['uptime', '-p'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('up ','')
		output = output[0:len(output)-1]
		# print (output)
		# print (output.rstrip())
		return output

	def update_other_stats(self):
		process = Popen(['cpufreq-info', '-m','--stats'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','').replace(' ','').split(',')
		# print (output)
		return output

	def get_curr_freq(self):
		process = Popen(['cpufreq-info', '-m','--hwfreq'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','')#.replace(' ','').split(',')
		# print (output)
		return output

	def get_curr_governor(self):
		process = Popen(['cpufreq-info', '-m','--policy'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','').split(' ')
		# print (output)
		return output

	def get_mem_use(self):
		process = Popen(['free', '-h'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().split('\n')
		# print (output)
		return output
		# vcgencmd get_mem arm && vcgencmd get_mem gpu #
		# free -h #mem use
		# df -h
		# lsusb
		# vcgencmd measure_volts
		# hostname
		# cat /proc/meminfo

	def blit_page_num(self,screen):
	    FONT_FEDERATION.render_to(screen, (30, 100), str(self.pg_id+1)+'/3', SLATE,style=0,size=28)
	    # FONT_FEDERATION.render_to(screen, (370, 640), "3", DARK_YELLOW,style=0,size=18)
	    FONT_FEDERATION.render_to(screen, (370, 640), str(self.pg_id+1)+'/3', DARK_YELLOW,style=0,size=18)

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)

		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:

			if pressed_button.name=='left_arrow':
				if self.pg_id>0:
					self.pg_id-=1
			elif pressed_button.name=='right_arrow':
				if self.pg_id<2:
					self.pg_id+=1
			print (self.pg_id)


		x_pos=170
		y_pos=65
		if self.pg_id==0:
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos),'Elapsed time: ', WHITE, size=28)
			FONT_DIN.render_to(screen, (x_pos, y_pos+35), str(elapsed_time()), WHITE, size=36)


			y_pos+=110
			pct,temp=self.update_cpu_stats()
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos),'CPU utilization: ', WHITE, size=28)
			FONT_DIN.render_to(screen, (x_pos, y_pos+35), pct, WHITE, size=36)

			y_pos+=110
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos),'CPU temperature: ', WHITE, size=28)
			FONT_DIN.render_to(screen, (x_pos, y_pos+35), temp, WHITE, size=36)

			y_pos+=110
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos),'System up time: ', WHITE, size=28)
			FONT_DIN.render_to(screen, (x_pos, y_pos+35), self.update_up_time(), WHITE, size=26)

		if self.pg_id==1:
		# y_pos+=110
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos),'Freq Stats: ', WHITE, size=28)
			for item in self.update_other_stats():
				freq,pct=item.split(':')
				FONT_DIN.render_to(screen, (x_pos, y_pos+35), str(freq)+': ', WHITE, size=24)
				FONT_DIN.render_to(screen, (x_pos+165, y_pos+35), str(pct) , WHITE, size=24)
				y_pos+=35

			y_pos+=20
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'Curr Freq:', WHITE, size=28)
			FONT_DIN.render_to(screen, (x_pos+220, y_pos+35), self.get_curr_freq() , WHITE, size=24)

			y_pos+=50
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'Curr Gov:', WHITE, size=28)
			g=self.get_curr_governor()
			g=g[::-1]
			for item in g:
				FONT_DIN.render_to(screen, (x_pos+220, y_pos+35), item , WHITE, size=24)
				y_pos+=35

		if self.pg_id==2:
			y_pos=65
			FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'Memory:', WHITE, size=28)
			y_pos+=35
			for item in self.get_mem_use():
				FONT_DIN.render_to(screen, (x_pos, y_pos+35), item , WHITE, size=10)
				y_pos+=25

		self.blit_page_num(screen)

		return self.next_screen_name,self.kwargs

class SettingsPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.button_list+=self.init_buttons()
		self.button_mapping={
							'home_button':'menu_home_page',
							'Num Pad':'numpad_page',
							'Exit':'exit'}

	def init_buttons(self):
		butt_list=[]
		col=165
		row=90
		button_h=115
		y_spacing=35
		f_size=60
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Backlight',font_size=f_size,style=0,font_color=ORANGE,name='Backlight'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Slider',font_size=f_size,style=0,font_color=ORANGE,font=FONT_DIN,name='slider'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Num Pad',font_size=f_size,style=0,font_color=ORANGE,name='Num Pad'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Exit',font_size=f_size,style=0,font_color=ORANGE,name='Exit'))
		return butt_list

	def handle_events_custom(self,screen,curr_events):

		self.handle_events(screen,curr_events)

		# for event in curr_events:
		# 	if (event.type==pygame.MOUSEBUTTONUP or event.type==pygame.FINGERUP):
		# 		self.reset_subpage()

		# 	# Dragging with mouse
		# 	scale=2
		# 	if event.type==pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
		# 		curr_x,curr_y=pygame.mouse.get_pos()
		# 		dx=curr_x-self.prev_x
		# 		if 0<abs(dx)<100:
		# 			for button in self.buttons_list:
		# 				button.rectangle.left+=(dx*scale)
		# 		self.prev_x=curr_x
		# 		self.prev_y=curr_y

		# 	# Dragging with finger
		# 	if event.type==pygame.FINGERMOTION:
		# 		curr_x,curr_y=event.x*screen.get_width(),event.y*screen.get_height()
		# 		dx=curr_x-self.prev_x

		# 		if 0<abs(dx)<100:
		# 			for button in self.buttons_list:
		# 				button.rectangle.left+=dx
		# 		self.prev_x=curr_x
		# 		self.prev_y=curr_y

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		# screen.blit(lcars_bg,(0,0))
		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:
			if pressed_button.name in self.button_mapping.keys():
				self.next_screen_name=self.button_mapping[pressed_button.name]

			if pressed_button.name=='Num Pad':
				self.next_screen_name='numpad_page'
				# return self.next_screen_name,{'prev_page_name':self.name}

			# if pressed_button.name=='slider':
				# self.next_screen_name='slider_test_page'


		return self.next_screen_name,self.kwargs

class SliderTestPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)

		self.button_dict=self.make_dictionary()
		self.prev_x,self.prev_y=pygame.mouse.get_pos()
		self.limit_low=0
		self.limit_high=255
		self.length=400
		self.x_pos=200
		self.end_pos=self.x_pos+self.length
		self.prev_page_name='menu_home_page'

		self.slider=SliderClass(200,290,20,50,length=320,min_val=7,max_val=250,start_val=200)
		# def __init__(self,start_x,y_pos,button_width,button_height,length=100,min_val=0,max_val=250,start_val=None):
		self.PIN_NUM=BACKLIGHT_PIN
		# self.gpio = pigpio.pi()
		self.gpio = PIGPIO

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		self.kwarg_handler(kwargs)

		self.transition_events(screen,curr_events)

		self.blit_all_buttons(screen)

		x=self.slider.rectangle.left
		y=self.slider.rectangle.top

		pos_string=f"(x,y): {x},{y}"

		FONT_DIN.render_to(screen, (300, 67),pos_string , WHITE,style=0,size=40)

		pressed_button=self.handle_events(screen,curr_events)

		pct,num_val,log_val=self.slider.compute_percentage()

		mp=math.ceil(self.slider.map(self.slider.rectangle.left))

		# ---- Set brightness --- #
		if 63<mp<=255:
			self.set_brightness(mp)
		self.gpio.set_PWM_dutycycle(19, mp)  #0-255, so 64 is 1/4 duty cycle

		FONT_DIN.render_to(screen, (200, 200),f'{pct}% {num_val} /255]'  , WHITE,style=0,size=40)
		FONT_DIN.render_to(screen, (200, 360),f'{self.get_current_brightness()}'  , WHITE,style=0,size=40)
		FONT_DIN.render_to(screen, (200, 420),f'{mp}' , WHITE,style=0,size=40)

		pygame.event.post(SET_BACKLIGHT)

		return self.next_screen_name,self.kwargs

	def transition_events(self,screen,curr_events):

		dx=0
		scale=1
		for event in curr_events:

				if (event.type==pygame.MOUSEBUTTONDOWN ):
					curr_x,curr_y=pygame.mouse.get_pos()
					if self.slider.line_rectangle.collidepoint(curr_x,curr_y):
						self.slider.rectangle.left=curr_x-self.slider.button_width//2

				# Dragging with mouse
				if (event.type==pygame.MOUSEMOTION ):
					curr_x,curr_y=pygame.mouse.get_pos()
					if self.slider.line_rectangle.collidepoint(curr_x,curr_y):
						if pygame.mouse.get_pressed()[0]==True:
							dx=event.rel[0]
							scale=5
							# print('collide mouse: ',curr_x,' ',curr_y)

				elif event.type==pygame.FINGERMOTION:
					curr_x,curr_y=event.x*screen.get_width(),event.y*screen.get_height()
					print('collide finger: ',curr_x,' ',curr_y)
					print (self.slider.line_rectangle.collidepoint(int(curr_x),int(curr_y)))

					# dx=curr_x-self.prev_x
					dx=curr_x-self.prev_x
					print ('finger dx: ',dx)
					self.prev_x=curr_x
					self.prev_y=curr_y

		self.slider.blit_slider(screen,dx,scale)

	def get_current_brightness(self):
		x=self.gpio.get_PWM_dutycycle(self.PIN_NUM)
		return x

	def set_brightness(self,curr):
		# self.print_current_brightness(self.gpio)
		self.gpio.set_PWM_dutycycle(self.PIN_NUM, int(curr))  #0-255, so 64 is 1/4 duty cycle
		# self.print_current_brightness(self.gpio)
		pygame.event.post(SET_BACKLIGHT)

	# ==================================================================== #

class MenuHomePageClass(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.bluetooth_connected=False

		# Determine positions and spacing for icons
		self.button_w=ICON_BUTTON_W
		self.column_spacing=COLUMN_SPACING
		self.col1_pos=COL1_POS
		self.row1_pos=ROW1_POS
		self.num_pages=NUM_PAGES

		# Page parameters
		self.page_offset=PAGE_OFFSET
		self.curr_subpage=1

		# UI stuff
		self.transition_right=False
		self.transition_left=False
		self.prev_x,self.prev_y=pygame.mouse.get_pos()

		self.page_dots=PAGE_DOTS
		self.page_dots_pos=(330,645)

		# Button stuff
		self.icon_buttons_list=ICON_BUTTONS
		self.button_list+=NAV_BUTTONS+self.icon_buttons_list
		self.button_mapping={'thermal_cam':'thermal_cam_page',
							'home':'home_page',
							'noise':'noise_page',
							'pm25':'pm25_sensor_page',
							'pressure':'pressure_sensor_page',
							'spectrometer':'spectrometer_page',
							'temp_humid':'temp_humid_page',
							'uv':'uv_sensor_page',
							'vis_ir':'light_sensor_page',
							'wind':'wind_sensor_page',
							'imu_2':'imu_sensor_page',
							'gps':'gps_sensor_page',
							'SDR':'sdr_page',
							'voc':'tvoc_eco2_page',
							'radiation':'radiation_sensor_page',
							'weigh_scale':'weight_sensor_page',
							'lidar':'lidar_sensor_page',
							'device_stats_2':'device_stats_page',
							'settings':'settings_page',
							'files':'file_browser_page',
							'sleep':'sleep_page',
							'battery':'battery_sensor_page',
							'multimeter':'multimeter_page',
							'object':'object_detection_page',
							'fly':'fly_page',
							'developer':'developer_page',
							'exit_button':'exit',
							}

	def blit_page_num(self,screen):
		FONT_FEDERATION.render_to(screen, (30, 100), str(self.curr_subpage)+'/'+str(self.num_pages), SLATE,style=0,size=28)

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)

		# Graphics
		self.transition_events(screen,curr_events)                          # check for dragging/scrolling
		self.blit_all_buttons(screen)
		self.blit_page_num(screen)                                          # page num

		try:
			screen.blit(self.page_dots[self.curr_subpage],self.page_dots_pos)   # page dots
		except Exception as e:
			logging.error(f"{self.__class__.__name__}: KeyError page_dots pg:{e}")

		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button!=None:
			if pressed_button.name in self.button_mapping.keys():
				self.next_screen_name=self.button_mapping[pressed_button.name]
			if pressed_button.name=='home_button':
				if self.curr_subpage==1:
					# self.next_screen_name='home_page'
					pass
				else:
					self.decrement_subpage(step=self.curr_subpage-1)

			if pressed_button.name=='sleep':
				pygame.event.post(GO_TO_SLEEP)
				ser.write(MCU_SLEEP_CODE.encode('utf-8'))
			if pressed_button.name=='right_arrow':
				self.increment_subpage()
			if pressed_button.name=='left_arrow':
				self.decrement_subpage()

		return self.next_screen_name,self.kwargs

	def increment_subpage(self,step=1):
		if self.curr_subpage<self.num_pages:
			for button in self.icon_buttons_list:
				button.update_position(button.rectangle.left-step*self.page_offset)
			self.curr_subpage+=1*step

	def decrement_subpage(self,step=1):
		if self.curr_subpage>1:
			for button in self.icon_buttons_list:
				button.update_position(button.rectangle.left+step*self.page_offset)
			self.curr_subpage-=1*step

	def reset_subpage(self):
		for button in self.icon_buttons_list:
			button.rectangle.left=(button.orig_rectangle_left-(self.curr_subpage-1)*720)

	def transition_events(self,screen,curr_events):

		transitioning= (self.transition_left or self.transition_right)
		if not transitioning:
			for event in curr_events:
				if (event.type==pygame.MOUSEBUTTONUP or event.type==pygame.FINGERUP):
					self.reset_subpage()

				# Dragging with mouse
				scale=2
				if event.type==pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
					curr_x,curr_y=pygame.mouse.get_pos()
					dx=curr_x-self.prev_x
					if 0<abs(dx)<100:
						for button in self.icon_buttons_list:
							button.rectangle.left+=(dx*scale)
					self.prev_x=curr_x
					self.prev_y=curr_y

				# Dragging with finger
				if event.type==pygame.FINGERMOTION:
					curr_x,curr_y=event.x*screen.get_width(),event.y*screen.get_height()
					dx=curr_x-self.prev_x

					if 0<abs(dx)<100:
						for button in self.icon_buttons_list:
							button.rectangle.left+=dx
					self.prev_x=curr_x
					self.prev_y=curr_y

				# Keyboard navigation
				if event.type==pygame.KEYUP:
					if (event.key == pygame.K_RIGHT):
						curr_events.remove(event)
						# self.transition_right=True
						self.increment_subpage()

					if (event.key == pygame.K_LEFT):
						curr_events.remove(event)
						# self.transition_left=True
						self.decrement_subpage()

		# --- Auto turn page --- #
		if not transitioning:
			left_lim=1.5*self.button_w   #since we are measuring from left side of button
			right_lim=screen.get_width()

			first_button_num=(self.curr_subpage-1)*9
			dist_to_middle_pos=self.button_w+self.column_spacing

			curr=self.icon_buttons_list[first_button_num].rectangle.left+dist_to_middle_pos
			if curr<left_lim:
				self.transition_right=True
			if curr>right_lim:
				self.transition_left=True

		# --- Transitions --- #
		self.transitions(screen)
		return self.next_screen_name,{}

	def transitions(self,screen):
		dx_transition=60
		if self.transition_right:
			if self.curr_subpage!=self.num_pages:  #checking if we are already on last page
				# dx_transition*=-1
				butt=self.icon_buttons_list[self.curr_subpage*9]
				self.curr_subpage+=1

				# Start animation
				self.get_sidebar_stats(screen)
				while (butt.rectangle.left>(self.col1_pos)):
					dx=min(dx_transition,(butt.rectangle.left-self.col1_pos))
					for button in self.icon_buttons_list:
						button.rectangle.left-=dx
					self.animate(screen)
			self.transition_right=False

		if self.transition_left:
			if self.curr_subpage>1:  #checking if we are already on last page
				if self.curr_subpage==2:
					butt=self.icon_buttons_list[0]
				if self.curr_subpage==3:
					butt=self.icon_buttons_list[9]
				if self.curr_subpage==4:
					butt=self.icon_buttons_list[18]
				self.curr_subpage-=1

				# Start animation
				self.get_sidebar_stats(screen)
				while ((self.col1_pos)>butt.rectangle.left):
					dx=min(dx_transition,(self.col1_pos-butt.rectangle.left))
					for button in self.icon_buttons_list:
						button.rectangle.left+=dx
					self.animate(screen)
			self.transition_left=False

	def draw_rectangle(self,screen):
		surf=pygame.Surface((118, 550))
		r=pygame.Rect(0,0,118,550)
		pygame.draw.rect(surf,BLACK,r)
		screen.blit(surf,(0,40))

	def get_sidebar_stats(self,screen):
		self.wifi_name=get_wifi_name()
		self.cpu_pct,self.cpu_temp=update_cpu_stats()
		self.sw=screen.get_width()
		self.fps=str(round(clock.get_fps(),2))
		if self.bluetooth_connected:
			self.b_img=bluetooth_img
		else:
			self.b_img=bluetooth_img_not_connected

	def animate(self,screen):
		# Graphics
		screen.fill(BLACK)
		self.blit_all_buttons(screen)
		self.draw_rectangle(screen)                         # Prevents icon/sidebar overlap
		screen.blit(self.page_dots[-1],self.page_dots_pos)  # Page dots
		screen.blit(lcars_bg,(0,0))                         # Background
		width=self.sw                                       # Screen width

		day,date,hour_sec=get_date_time()
		blit_some_stats(screen,self.sw,day,date,hour_sec,self.fps,self.cpu_pct,self.cpu_temp,self.wifi_name,'I',self.b_img)
		self.blit_page_num(screen)
		# pygame.display.flip()
		pygame.display.update()

class QuickMenuPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.butt_list=QUICK_MENU_BUTTONS
		self.button_list+=self.butt_list
		self.prev_page_name=self.name
		self.backlight_lvl=-1
		self.fullscreen_en=False

		self.screen_dict={'backlight':'slider_test_page','device_stats':'device_stats_page',
							'home':'home_page','exit':'exit',
							'sleep':'sleep_page','screenshot':self.prev_page_name,
							'exit_fullscreen':self.prev_page_name,
							'fullscreen':self.prev_page_name
							}
		self.event_dict={'exit_fullscreen':TOGGLE_SCREEN,'fullscreen':TOGGLE_SCREEN,
						 'sleep':GO_TO_SLEEP,'screenshot':SCREENSHOT_EVENT}

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name

		if 'prev_page_name' in kwargs:
			self.prev_page_name=kwargs['prev_page_name']

		self.blit_basic_buttons(screen)
		self.blit_some_buttons(screen,self.butt_list)

		FONT_FEDERATION.render_to(screen, (534, 140),f'{self.backlight_lvl}' , ORANGE,style=1,size=36)

		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button!=None:
			if pressed_button.name in self.screen_dict.keys():
				self.next_screen_name=self.screen_dict[pressed_button.name]

			if pressed_button.name=='screenshot':
				pygame.event.post(SCREENSHOT_EVENT)
				self.next_screen_name=self.prev_page_name
				return self.next_screen_name,{}

			if pressed_button.name=='fullscreen':
				pygame.event.post(TOGGLE_SCREEN)
				self.next_screen_name=self.prev_page_name
				return self.next_screen_name,{}

			elif pressed_button.name in self.event_dict.keys():
				e=self.event_dict[pressed_button.name]
				pygame.event.post(e)

		pygame.event.post(SET_BACKLIGHT)
		return self.next_screen_name,{}

class FileBrowserPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)

		self.button_list+=NAV_BUTTONS_VERTICAL
		self.refresh_files_list()

		self.button_list+=self.file_button_list
		self.prev_page_name='menu_home_page'
		self.p=pygame.Surface((0,0))

		self.bg=pygame.Surface((320,320))
		self.bg.set_alpha(200)
		self.bg.fill(WHITE)

		self.curr_butt_index=0
		self.curr_butt=self.file_button_list[self.curr_butt_index]
		self.curr_butt.selected=True
		self.p=pygame.image.load(self.curr_butt.name)
		self.p=pygame.transform.scale(self.p, (300, 300))

	def refresh_files_list(self):
		self.screenshot_files=[]
		for root, dirs, files in os.walk("screenshots/", topdown=True):
			for name in files:
				self.screenshot_files.append(os.path.join(root, name))
		self.screenshot_files.sort(key=os.path.getctime,reverse=True)

		self.file_button_list=[]
		self.start_y=400
		x=150
		y=self.start_y
		f_size=24
		for item in self.screenshot_files:
			# item=item.replace('screenshots/','').replace('.png','')
			self.file_button_list.append(ButtonClass(0,simp_button,simp_button_alt,x,y,name=item,text=item.replace('screenshots/','').replace('.png',''),font=FONT_HELVETICA_NEUE,font_color=WHITE,selected_img=simp_button_selected,selected_color=ORANGE,align_left=True))
			# FONT_HELVETICA_NEUE.render_to(screen, (x, y),item, WHITE,style=0,size=f_size)
			y+=65
			# for name in dirs:
			#     print(os.path.join(root, name))
		self.end_y=y

	def gruntwork(self):
		self.curr_butt=self.file_button_list[self.curr_butt_index]
		self.curr_butt.selected=True
		self.p=pygame.image.load(self.curr_butt.name)
		self.p=pygame.transform.scale(self.p, (300, 300))
		for b in self.button_list:
			if b!=self.curr_butt:
				b.selected=False

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)

		self.blit_all_buttons(screen)
		screen.blit(self.bg,(300-10,80-10))
		screen.blit(self.p,(300,80))

		self.blit_title(screen)

		# self.refresh_files_list()

		# Keyboard navigation
		for event in curr_events:

			if event.type==pygame.KEYUP:
				if (event.key == pygame.K_DOWN):

					curr_events.remove(event)

					# if self.file_button_list[0].rectangle.top-50<self.start_y:
					print(self.curr_butt_index,len(self.file_button_list))
					if self.curr_butt_index<len(self.file_button_list)-1:
						self.curr_butt_index+=1
						self.gruntwork()
						for b in self.file_button_list:
							b.rectangle.top-=65

				if (event.key == pygame.K_UP):
					curr_events.remove(event)
					print(self.curr_butt_index,len(self.file_button_list))
					if self.curr_butt_index>0:
						self.curr_butt_index-=1
						self.gruntwork()
						# if self.file_button_list[-1].rectangle.top+50>self.end_y:
						for b in self.file_button_list:
							b.rectangle.top+=65


		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button!=None:
			if pressed_button in self.file_button_list:
				# try:
					self.p=pygame.image.load(pressed_button.name)
					self.p=pygame.transform.scale(self.p, (300, 300))
					if not pressed_button.selected:
						pressed_button.selected=not pressed_button.selected

					for b in self.button_list:
						if b!=pressed_button:
							b.selected=False

				# except Exception as e:
				#     print(e)

			if pressed_button.name=='up':
				if self.curr_butt_index>0:
					self.curr_butt_index-=1
					self.gruntwork()
					# if self.file_button_list[-1].rectangle.top+50>self.end_y:
					for b in self.file_button_list:
						b.rectangle.top+=65

			if pressed_button.name=='page_up':
				self.curr_butt_index=0
				self.gruntwork()
				for hh in range(len(self.file_button_list)-self.curr_butt_index+1):
					for b in self.file_button_list:
						b.rectangle.top+=65

			if pressed_button.name=='down':
				if self.curr_butt_index<len(self.file_button_list)-1:
					self.curr_butt_index+=1
					self.gruntwork()
					for b in self.file_button_list:
						b.rectangle.top-=65


			if pressed_button.name=='page_down':
				self.curr_butt_index=len(self.file_button_list)-1
				self.gruntwork()
				for hh in range(len(self.file_button_list)-self.curr_butt_index+1):
					# print (hh)
					for b in self.file_button_list:
						b.rectangle.top-=65





		return self.next_screen_name,self.kwargs

	def blit_title(self,screen):
		FONT_FEDERATION.render_to(screen, (150, 67), 'Files', ORANGE,style=0,size=44)

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
		self.intermediate_screen=self.next_screen
		lcars_bg.set_colorkey(BLACK)
		# print ('pygame.display.get_allow_screensaver(): ',pygame.display.get_allow_screensaver())

		# Convenient struct to store device stats
		self.DeviceInfo=DeviceInfoClass()

		# Retrieve backlight level
		self.DeviceInfo.curr_brightness=self.screen_dict['slider_test_page'].get_current_brightness()

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
		modes = pygame.display.list_modes()
		# print(f"mode:{modes}")
		# print(pygame.display.get_wm_info())
		# print (pygame.display.mode_ok(modes[0]))
		# self.full_res=modes[0]
		self.color_depth=pygame.display.mode_ok(modes[0])
		if not self.fullscreen_en:
			screen=pygame.display.set_mode(STARTING_RES,   pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT, self.color_depth)
		else:
			screen=pygame.display.set_mode(FULL_SCREEN_RES, pygame.FULLSCREEN |  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT, self.color_depth)
		starfleet_logo.convert()
		pygame.display.set_icon(starfleet_logo_small)
		pygame.display.set_caption("Tricorder")
		# print(modes)
		# print (f"screen: {screen}")
		# print (f"pygame.display: {pygame.display}")
		# print(pygame.display.get_wm_info())
		# print (pygame.display.mode_ok(modes[0]))

		self.screen_dict['quick_menu_page'].fullscreen_en=self.fullscreen_en

		return screen

	def init_pages(self):

		self.sensor_pages_list=[ThermalCamPage('thermal_cam_page'),
					 LightSensorPage('light_sensor_page'),
					 UVSensorPage('uv_sensor_page'),
					 pm25page('pm25_sensor_page'),
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
											 SliderTestPage('slider_test_page'),
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
		# self.screenshot_overlay=s
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
					logging.info (self.screen.get_size())
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
				self.backlight_restore_level=self.screen_dict['slider_test_page'].get_current_brightness()
				self.screen_dict['slider_test_page'].set_brightness(0)
				self.DeviceInfo.curr_brightness=self.screen_dict['slider_test_page'].get_current_brightness()
				curr_events.remove(event)
				ser.write(MCU_SLEEP_CODE.encode('utf-8'))
				ser.readline()

			if event==SET_BACKLIGHT:
				# print('SET_BACKLIGHT')
				c=self.screen_dict['slider_test_page'].get_current_brightness()
				self.DeviceInfo.curr_brightness=c
				self.screen_dict['quick_menu_page'].backlight_lvl=c
				curr_events.remove(event)

			if event==GET_BACKLIGHT_QUICK_MENU:
				self.screen_dict['quick_menu_page'].backlight_lvl=self.screen_dict['slider_test_page'].get_current_brightness()
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

	def sensor_event_handler(self,curr_events):

		screen=self.screen
		for event in curr_events:

			if event==REQUEST_FLY_DATA:
				curr_events.remove(event)

				p=self.screen_dict['fly_page']

				if p.frame_count%p.imu_tics==0:
					try:
						x=self.get_sensor_vals(IMU_ORIENTATION_CODE,['Hd','Rl','Ph'])
						p.heading=x['Hd']
						p.roll=(round(float(x['Rl']),1))
						p.pitch=x['Ph']

					except TypeError:
						print ('type err: REQUEST_FLY_DATA request imu orientation')
					except KeyError:
						print ('key err: REQUEST_FLY_DATA request orientation')

				if p.frame_count%p.temp_humid_tics==0:
					x=self.get_sensor_vals(TEMP_HUMID_CODE,['temperature','relative_humidity','heater','h_res','t_res'])
					try:
						p.temperature=x['temperature']
						p.humidity=x['relative_humidity']
					except TypeError:
						print ('type err: REQUEST_FLY_DATA request temp_humid')
					except KeyError:
						print ('key err: REQUEST_FLY_DATA request temp_humid')
				if p.frame_count%p.gps_tics==0:
					try:
						x=self.get_sensor_vals(GPS_CODE,['lat','lng','alt','spd','sat'])

						p.lat=float(x['lat'])
						p.long=float(x['lng'])
						p.altitude=float(x['alt'])
						p.speed=float(x['spd'])
						p.satellite_count=int(x['sat'])

					except TypeError:
						print ('type err: REQUEST_FLY_DATA request gps')
					except KeyError:
						print ('key err: REQUEST_FLY_DATA request gps')

				if p.frame_count%p.pressure_tics==0:
					try:
						x=self.get_sensor_vals(PRESSURE_CODE,['pressure','bmp_temp','p_over','t_over','alt'])

						p.bmp_alt=x['alt']
						p.pressure=round(float(x['pressure']),1)

					except TypeError:
						print ('type err: REQUEST_FLY_DATA request pressure')
					except KeyError:
						print ('key err: REQUEST_FLY_DATA request pressure')

				if p.frame_count%p.uv_tics==0:
					x=self.get_sensor_vals(UV_CODE,['uvs','light','uvi','ltr_lux','ltr_gain','ltr_res','ltr_win_fac','ltr_mdelay'])

					if len(x)>1:
						try:
							p.uv=x['uvs']
						except TypeError:
							print ('type err: REQUEST_FLY_DATA request uv')
						except KeyError:
							print ('key err: REQUEST_FLY_DATA request uv: ',x)

				if p.frame_count%p.vis_ir_tics==0:
					ser.write(TSL_SCL_CONNECT_CODE.encode('utf-8'))
					time.sleep(1)

					try:
						x=self.get_sensor_vals(VIS_IR_CODE,['lux','infrared','visible','full_spectrum','tsl2591_gain'])
						p.vis=x['lux']
						p.ir=x['infrared']
					except TypeError:
						print ('type err: REQUEST_FLY_DATA request vis_ir')
					except KeyError:
						print ('key err: REQUEST_FLY_DATA request vis_ir')


					ser.write(TSL_SCL_DISCONNECT_CODE.encode('utf-8'))

				# vis_ir_tics
				# imu_tics
				# gps_tics
				# temp_humid_tics
				# pressure_tics

			if event==REQUEST_BLUETOOTH:
				curr_events.remove(event)
				# try:
				# 	msg=self.screen_dict['home_page'].compose_message()
				# 	x=self.get_sensor_vals(msg,SENSOR_LIST)
				# 	self.screen_dict['home_page'].sensor_dict=x
				# 	self.screen_dict['home_page'].bluetooth_count+=1
				# except TypeError:
				# 	print ('type err: request_bluetooth')
				# except KeyError:
				# 	print ('key err: request ')

			if event==SET_TEMP_SETTINGS:
				curr_events.remove(event)
				# print ('SET_TEMP_SETTINGS',self.screen_dict['temp_humid_page'].send_code)
				# x=self.get_bluetooth_vals(self.screen_dict['temp_humid_page'].send_code)

			if event==SET_UV_GAIN:
				curr_events.remove(event)
				print ('SET_UV_GAIN')
				x=self.get_bluetooth_vals(self.screen_dict['uv_sensor_page'].send_code)

			if event==SET_LIGHT_SENSOR_GAIN:
				curr_events.remove(event)
				print ('SET_LIGHT_SENSOR_GAIN')
				x=self.get_bluetooth_vals(self.screen_dict['light_sensor_page'].new_gain)

			if event==SET_PRESSURE:
				curr_events.remove(event)
				print ('SET_PRESSURE')
				x=self.get_bluetooth_vals(self.screen_dict['pressure_sensor_page'].send_code)

			if event==BLUETOOTH_CONNECTED:
				curr_events.remove(event)
				print ('BLUETOOTH_CONNECTED!!!')
				self.DeviceInfo.bluetooth_connected=True
				self.screen_dict['home_page'].client_sock=self.client_sock
				self.screen_dict['thermal_cam_page'].client_sock=self.client_sock
				for page in self.sensor_pages_list:
					page.bluetooth_connected=True
				# msg=self.screen_dict['home_page'].curr_msg
				# x=self.get_bluetooth_vals(msg)
				# self.screen_dict['home_page'].sensor_dict=x

			if event==BLUETOOTH_DISCONNECTED:
				curr_events.remove(event)
				print ('BLUETOOTH_DISCONNECTED!!!')
				self.DeviceInfo.bluetooth_connected=False
				self.screen_dict['home_page'].client_sock=None
				self.screen_dict['thermal_cam_page'].client_sock=None
				for page in self.sensor_pages_list:
					page.bluetooth_connected=False

				try:
					t1 = thread_with_trace(target =  self.connect_bluetooth)
					t1.setName('connect_bluetooth')
					t1.start()
				except Exception as e:
					raise(e)

		return curr_events

	def next_frame_main(self):

		next_screen_name=self.curr_screen.name
		self.curr_screen=self.next_screen

		self.screen.fill(BLACK)
		self.screen.blit(lcars_bg,(0,0))
		curr_events=self.sensor_event_handler(pygame.event.get())

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


		# # ---- control power brute force method ---- #
		# if self.curr_screen.name=="radiation_sensor_page" and next_screen_name!="radiation_sensor_page":
		# 	ser.write(GEIGER_PWR_OFF_CODE.encode('utf-8'))
		# if self.curr_screen.name!="radiation_sensor_page" and next_screen_name=="radiation_sensor_page":
		# 	ser.write(GEIGER_PWR_ON_CODE.encode('utf-8'))


		curr_events=self.generic_event_handler(curr_events)

		for screen_name,screen in self.screen_dict.items():
			# print (screen_name)
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
def wrap_up():
		print ('\nLive long & prosper... bye!')
		t=elapsed_time(print_res=True)

def elapsed_time(print_res=False):
		end_time=round(time.time()-start_time_overall,2)
		elapsed_time=(datetime.timedelta(seconds=round(end_time)))
		if (print_res):
			logging.info (f'time elapsed: {elapsed_time} s')
		return elapsed_time

if __name__=='__main__':

	global start_time_overall
	global MODE
	global PIGPIO

	# # following vars are for backlight
	# PIGPIO=pigpio.pi()

	MODE='normal'
	start_time_overall=time.time()

	clock=pygame.time.Clock()

	fullscreen_en=False

	W=WindowManager(fullscreen_en)

	try:
		while True:
			W.screen=W.next_frame_main()
			# scr.blit(pygame.transform.rotate(scr, 270), (0, 0))
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
