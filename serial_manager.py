#!/usr/bin/python3

'''
-> This file contains functions for communicating over a serial usb/bluetooth link using tcp/ip sockets. By sending data back and forth:
	-> Data can be requested from sensors
	-> Sensor-specific settings can be changed
	-> Microcontroller operations can be changed (e.g., sleep mode)
	-> Both of the above involves sending specific mappings from mappings.py
-> Each sensor page can import relevant functions for efficiency.
-> Keeping all in one place in case of changes to how I communicate with sensors.
'''

from mappings import *
import serial
from my_logging import *
# print ("serial.VERSION:",serial.VERSION)

# set up logging
shivams_logging(script_name="tricorder",console_log_level="info",logfile_log_level="info")
logging.info (f'\n')

PORT_NAME="/dev/my_esp32"	# this is the custom assigned port for esp32

try:
	ser = serial.Serial(
	    port=PORT_NAME, # Change this according to connection methods, e.g. /dev/ttyUSB0
	    baudrate = 115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS,
	    timeout=1
	)
	# ser.write(MCU_RESET_CODE.encode('utf-8'))
	ser.write(MCU_IND_MODE_DISABLE.encode('utf-8'))
	ser.flush()
	logging.info (f'mcu connected on {PORT_NAME}!')

except serial.serialutil.SerialException:
	logging.error (f'mcu not connected on {PORT_NAME}!')
	ser=None

# -------------------------------------------------
def get_temp_humid():
	try:
		x=get_serial_vals(d['TEMP_HUMID_CODE'],['temperature','relative_humidity','heater','h_res','t_res'])
		c_temp=float(x['temperature'])
		humid=float(x['relative_humidity'])
		h_res=float(x['h_res'])
		t_res=float(x['t_res'])
		return c_temp,humid,h_res,t_res
	except Exception:
		return -1,-1,-1,-1

def get_pressure():
	try:
		x=get_serial_vals(d['PRESSURE_CODE'],['pressure','bmp_temp','p_over','t_over','alt'])
		altitude=float(x['alt'])
		pressure=float(x['pressure'])
		bmp_temp=float(x['bmp_temp'])
		p_oversampling=float(x['p_over'])
		t_oversampling=float(x['t_over'])
		return altitude,pressure,bmp_temp,p_oversampling,t_oversampling
	except Exception:
		return -1,-1,-1,-1,-1

def get_tvoc_eco2():
	try:
		x=get_serial_vals(d['TVOC_CODE'],['eCO2','TVOC','raw_H2','raw_ethanol','baseline_eCO2','baseline_TVOC'])
		TVOC=x['TVOC']
		eCO2=x['eCO2']
		baseline_eCO2=x['baseline_eCO2']
		baseline_TVOC=x['baseline_TVOC']
		return TVOC,eCO2,baseline_eCO2,baseline_TVOC
	except Exception:
		return -1,-1,-1,-1

# -------------------------------------------------
def get_vis_ir():
	try:
		x=get_serial_vals(d['VIS_IR_CODE'],['lux','infrared','visible','full_spectrum','tsl2591_gain'])
		lux=float(x['lux'])
		ir=int(x['infrared'])
		gain=x['tsl2591_gain']
		visible=float(x['visible'])
		full_spectrum=float(x['full_spectrum'])
		return lux,ir,gain,visible,full_spectrum
	except Exception:
		return -1,-1,-1,-1,-1

def get_uv():
	x=get_serial_vals(d['UV_CODE'],['uvs','light','uvi','ltr_lux','ltr_gain','ltr_res','ltr_win_fac','ltr_mdelay'])

	if len(x)>1:
		try:
			uvs=x['uvs']
			light=x['light']
			uvi=x['uvi']
			ltr_lux=x['ltr_lux']
			ltr_gain=x['ltr_gain']
			ltr_resolution=x['ltr_res']
			ltr_window_factor=x['ltr_win_fac']
			ltr_measurement_delay=x['ltr_mdelay']
			return uvs,light,uvi,ltr_lux,ltr_gain,ltr_resolution,ltr_window_factor,ltr_measurement_delay
		except Exception:
			return -1,-1,-1,-1,-1,-1,-1,-1

def get_spectrometer():
	try:
		channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
		x=get_serial_vals(d['SPEC_CODE'],channels)
		return x
	except Exception:
		return [1,1,1,1,1,1,1,1,1,1]

# -------------------------------------------------
def get_pm25():
	try:
		aqdata=[]
		x=get_serial_vals(d['PM25_CODE'],['03um','05um','10um','25um','50um','100um'])
		aqdata.append(x['03um'])
		aqdata.append(x['05um'])
		aqdata.append(x['10um'])
		aqdata.append(x['25um'])
		aqdata.append(x['50um'])
		aqdata.append(x['100um'])
		return aqdata
	except Exception:
		return [1, 1, 1, 1, 1, 1]

def get_noise():
	try:
		x=get_serial_vals(d['NOISE_CODE'],['noise_out'])
		return int(x['noise_out'])
	except Exception:
		return 0

def get_wind():
	try:
		# my_flush()
		ser.write(WIND_CODE.encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
		return int(curr_line)
	except Exception as e:
		print (f"{e}: wind error")
		return -1

# -------------------------------------------------
def get_multimeter():
	try:
		# my_flush()
		ser.write(d['CURRENT_CODE'].encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')
		return float(curr_line[0]),float(curr_line[1]),float(curr_line[2])
	except Exception:
		return -1,-1,-1

def get_gps():
	try:
		x=get_serial_vals(d['GPS_CODE'],['lat','lng','alt','spd','sat'])
		return float(x['lat']),float(x['lng']),float(x['alt']),float(x['spd']),int(x['sat'])
	except Exception:
		return -1,-1,-1,-1,-1

def get_battery():
	try:
		x=get_serial_vals(d['BATTERY_CODE'],['volt','pct','temp'])
		return float(x['volt']),float(x['pct']),float(x['temp'])
	except Exception:
		return -1,-1,-1

def get_radiation():
	try:
		x=get_serial_vals(d['RADIATION_CODE'],['CPM'])
		return float(x['CPM'])
	except Exception:
		return -1

# --------- Inertial measurement unit --------- #
def get_imu_orientation():
	try:
		x=get_serial_vals(d['IMU_ORIENTATION_CODE'],['Hd','Rl','Ph'])
		return float(x['Hd']),float(x['Rl']),float(x['Ph'])
	except Exception:
		return -1,-1,-1

def get_imu_ang_vel():
	try:
		x=get_serial_vals(d['IMU_ANG_VEL_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception:
		return -1,-1,-1

def get_imu_lin_acc():
	try:
		x=get_serial_vals(d['IMU_LIN_ACC_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception:
		return -1,-1,-1

def get_imu_acc():
	try:
		x=get_serial_vals(d['IMU_ACC_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception:
		return -1,-1,-1

def get_imu_mag():
	try:
		x=get_serial_vals(d['IMU_MAG_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception:
		return -1,-1,-1

def get_imu_grav():
	try:
		x=get_serial_vals(d['IMU_GRAV_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception:
		return -1,-1,-1

# -------------- VIS/IR light sensor  -------------- #
def set_tsl_scl_disconnect():
	ser.write(TSL_SCL_DISCONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_tsl_scl_connect():
	ser.write(TSL_SCL_CONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_tsl_gain(new_gain):
	ser.write(new_gain.encode('utf-8'))
	ser.readline()

# ------------------- PM25 ------------------------- #
def set_pm25_power_off():
	ser.write(PM25_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_pm25_power_on():
	ser.write(PM25_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_geiger_power_off():
	ser.write(GEIGER_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_geiger_power_on():
	ser.write(GEIGER_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())

# -------------------------------------------------
def get_serial_vals(send_msg,dict_names_list):
		recv_msg={}

		for char in send_msg.rstrip(' ').split(' '):
			ser.write(send_msg.encode('utf-8'))
			curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
			logging.debug ("curr_line: "+str(curr_line))

			# sometimes a blank line gets sent. brute force to remove.
			if curr_line=="":
				curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
				logging.debug ("curr_line 2: "+str(curr_line))

			# if (ser.inWaiting() > 0):
			# 	curr_line = ser.read(ser.inWaiting()).decode('ascii')

			for item,name in zip(curr_line.split(' '),dict_names_list):
				try:
					val=item.split(":")[1]
				except IndexError as e:
					val=-1
					logging.error(f"{e} sent:{d_inv[send_msg]} [{send_msg}] recvd:{curr_line}")
				recv_msg[name]=val
			logging.debug (str(send_msg)+":"+str(recv_msg))

		return recv_msg

def my_flush():
	while (len(ser.readline())>0):
		logging.warning ('dumping serial vals')

