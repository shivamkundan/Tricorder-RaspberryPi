# '''
# This file contains functions invoked by several different parts of the code.
# '''
# import pygame
# import datetime
# from subprocess import PIPE, Popen, check_output
# import psutil

# from fonts import FONT_DIN,FONT_OKUDA,FONT_OKUDA_BOLD,WIFI_FONT
# from colors import WHITE, ORANGE, LIGHT_BLUE
# # ================ Global functions ================================= #

# def my_map(x,in_min,in_max,out_min,out_max):
# 	'''Standard mapping formula. Used in many places'''
# 	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
# def blitRotate2(surf, image, topleft, angle):
# 	'''Rotate an image around its center'''
# 	rotated_image = pygame.transform.rotate(image, angle)
# 	new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

# 	surf.blit(rotated_image, new_rect.topleft)

# def get_text_dimensions(text='',font_style=FONT_DIN,font_color=WHITE,style=0,font_size=28):
# 	'''Return size of to-be-rendered text'''
# 	val_txt=font_style.render(text,fgcolor=font_color,size=font_size)
# 	x=list(val_txt)
# 	w=x[1][2]
# 	h=x[1][3]
# 	surf=x[0]
# 	return surf,w,h

# def flip_buttons(pressed_button,button_list):
# 	'''Unselect all other buttons except the one just pressed'''
# 	if pressed_button.selected:
# 		return
# 	else:
# 		pressed_button.selected=True

# 	for button in button_list:
# 		if button!=pressed_button:
# 			button.selected=False

# def update_cpu_stats(dt=None):
# 	'''Get rapsberry pi usage stats'''
# 	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
# 	output, _error = process.communicate()
# 	output = output.decode()

# 	pos_start = output.index('=') + 1
# 	pos_end = output.rindex("'")

# 	temp = float(output[pos_start:pos_end])

# 	cpu_percent=int(round(psutil.cpu_percent()))

# 	bars=''
# 	for iter in range(cpu_percent//10):
# 		bars+='||'

# 	cpu_pct=bars+f' {cpu_percent}%'
# 	cpu_temp=f'{temp}°C'
# 	# self.cpu_label.text=cpu_txt

# 	return cpu_pct,cpu_temp

# def get_wifi_name():
# 	'''Check for connected wifi network. Return network name'''
# 	try:
# 		wifi_name=check_output(['iwgetid','-r']).decode('utf-8').strip('\n')
# 		if wifi_name=='Wu Tang LAN':
# 			wifi_name='Terok Nor'
# 	except Exception:
# 		wifi_name='No Wifi'
# 	wifi_name=wifi_name
# 	return wifi_name

# def get_date_time():
# 	'''Get formatted time for top toolbar display'''
# 	now = datetime.datetime.now()
# 	day=now.strftime('%a')
# 	date=now.strftime('%b %-d')
# 	# hour_sec=now.strftime('%-I:%M:%S %p')
# 	hour_sec=now.strftime('%-I:%M %p')
# 	return (day,date, hour_sec)

# def blit_some_stats(screen,width,day,date,hour_sec,fps,cpu_pct,cpu_temp,wifi_name,wifi_symbol,bluetooth_img):
# 	'''These pieces of info are always displayed in the top bar or in the Okudagrams'''

# 	# Day/Date
# 	day,date,hour_sec=get_date_time()
# 	FONT_OKUDA_BOLD.render_to(screen, (10, 205), day+', '+date, fgcolor=ORANGE,style=0,size=38)

# 	# Time
# 	txt_surf,w,h=get_text_dimensions(text=hour_sec,font_style=FONT_DIN,font_color=WHITE,style=0,font_size=28)
# 	screen.blit(txt_surf,((width//2-w//2+30),10))

# 	# FPS
# 	rr=255
# 	txt_surf,w,h=get_text_dimensions(text=fps+' FPS',font_style=FONT_OKUDA,font_color=LIGHT_BLUE,style=0,font_size=44)
# 	screen.blit(txt_surf,(105-w,rr))

# 	# CPU percentage
# 	rr+=60
# 	txt_surf,w,h=get_text_dimensions(text=cpu_pct,font_style=FONT_OKUDA,font_color=LIGHT_BLUE,style=0,font_size=32)
# 	screen.blit(txt_surf,(105-w,rr))

# 	# CPU temp
# 	rr+=40
# 	txt_surf,w,h=get_text_dimensions(text=cpu_temp,font_style=FONT_OKUDA,font_color=LIGHT_BLUE,style=0,font_size=32)
# 	screen.blit(txt_surf,(105-w,rr))

# 	# Wifi name
# 	txt_surf,w,h=get_text_dimensions(text=wifi_name,font_style=FONT_OKUDA,font_color=WHITE,style=0,font_size=34)
# 	screen.blit(txt_surf,((width-w-10),10))

# 	# Wifi symbol
# 	txt_surf,w2,h=get_text_dimensions(text=wifi_symbol,font_style=WIFI_FONT,font_color=WHITE,style=0,font_size=26)
# 	screen.blit(txt_surf,(width-w-10-w2-10,8))

# 	# Bluetooth
# 	x_pos=width-w-10-w2-10
# 	screen.blit(bluetooth_img,(x_pos-23,4))

# 	return w,w2

# def adjust_gauge_lims(curr_val,gauge):
# 	'''For circular gauges. Adjusts upper/lower limits to nearest round numbers'''
# 	lower_lims=[0,1,10,100,1000,10000,100000]
# 	upper_lims=[1,10,100,1000,10000,100000,1000000]
# 	for low,up in zip(lower_lims,upper_lims):
# 		if low<=curr_val<up:
# 			gauge.in_max=up

