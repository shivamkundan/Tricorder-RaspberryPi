#!/usr/bin/python3
"""
	This file contains functions for communicating over a serial usb/bluetooth link using tcp/ip sockets.
		-> Each sensor page can import relevant functions for efficiency.

		-> Keeping all in one place in case of changes to how I communicate with sensors.

	By sending data back and forth:
		-> Data can be requested from sensors

		-> Sensor-specific settings can be changed

		-> Microcontroller operations can be changed (e.g., sleep mode)

		-> Both of the above involves sending specific mappings from mappings.py
"""

##
# @file serial_manager.py
#
# @brief Contains Functions for serial comminication with MCU.
#


from mappings import d, d_inv, WIND_CODE, MCU_IND_MODE_DISABLE, \
					TSL_SCL_DISCONNECT_CODE, TSL_SCL_CONNECT_CODE, \
					PM25_PWR_OFF_CODE, PM25_PWR_ON_CODE, \
					GEIGER_PWR_OFF_CODE, GEIGER_PWR_ON_CODE
import serial
import logging

## This is the custom assigned port for esp32
PORT_NAME="/dev/my_esp32"

try:
	## Serial communication object
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
	'''
	Get temperature and humidity readings

	:Dictionary keys: ['temperature', 'relative_humidity', 'heater', 'h_res', 't_res']
	:returns: temperature, relative_humidity, h_res, t_res
	'''

	'''! @brief Get temperature and humidity readings
		@return if normal -> temperature, relative_humidity, h_res, t_res
		@return if error  -> -1,-1,-1,-1
	'''
	try:
		x=get_serial_vals(d['TEMP_HUMID_CODE'],['temperature','relative_humidity','heater','h_res','t_res'])
		c_temp=float(x['temperature'])
		humid=float(x['relative_humidity'])
		h_res=float(x['h_res'])
		t_res=float(x['t_res'])
		return c_temp,humid,h_res,t_res
	except Exception as e:
		logging.error(e)
		return -1,-1,-1,-1

def get_pressure():
	'''
	Dictionary keys:
				['pressure', 'bmp_temp', 'p_over', 't_over', 'alt']
	'''

	'''! @brief Get barometric pressure, temperature, and est altitude readings
		@return if normal -> altitude, pressure, bmp_temp, p_oversampling, t_oversampling
		@return if error  -> -1, -1, -1, -1, -1
	'''



	try:
		x=get_serial_vals(d['PRESSURE_CODE'],['pressure','bmp_temp','p_over','t_over','alt'])
		altitude=float(x['alt'])
		pressure=float(x['pressure'])
		bmp_temp=float(x['bmp_temp'])
		p_oversampling=float(x['p_over'])
		t_oversampling=float(x['t_over'])
		return altitude,pressure,bmp_temp,p_oversampling,t_oversampling
	except Exception as e:
		logging.error(e)
		return -1,-1,-1,-1,-1

def get_tvoc_eco2():
	'''
	Dictionary keys:
				['eCO2', 'TVOC', 'raw_H2', 'raw_ethanol', 'baseline_eCO2', 'baseline_TVOC']
	'''

	'''! Get volatile organic compound and estimated CO2 readings
	@return if normal -> TVOC, eCO2, baseline_eCO2, baseline_TVOC
	@return if error  -> -1,-1,-1,-1
	'''
	try:
		x=get_serial_vals(d['TVOC_CODE'],['eCO2','TVOC','raw_H2','raw_ethanol','baseline_eCO2','baseline_TVOC'])
		TVOC=x['TVOC']
		eCO2=x['eCO2']
		baseline_eCO2=x['baseline_eCO2']
		baseline_TVOC=x['baseline_TVOC']
		return TVOC,eCO2,baseline_eCO2,baseline_TVOC
	except Exception as e:
		logging.error(e)
		return -1,-1,-1,-1

# -------------------------------------------------
def get_vis_ir():
	'''
	Dictionary keys:
				['lux', 'infrared', 'visible', 'full_spectrum', 'tsl2591_gain']
	'''

	'''! Get readings for visible and infrared light
	@return if normal -> lux, ir, gain, visible, full_spectrum
	@return if error  -> -1,-1,-1,-1,-1
	'''
	try:
		x=get_serial_vals(d['VIS_IR_CODE'],['lux','infrared','visible','full_spectrum','tsl2591_gain'])
		lux=float(x['lux'])
		ir=int(x['infrared'])
		gain=x['tsl2591_gain']
		visible=float(x['visible'])
		full_spectrum=float(x['full_spectrum'])
		return lux,ir,gain,visible,full_spectrum
	except Exception as e:
		logging.error(e)
		return -1,-1,-1,-1,-1

def get_uv():
	'''
	Dictionary keys:
				['uvs','light','uvi','ltr_lux','ltr_gain','ltr_res','ltr_win_fac','ltr_mdelay']
	'''

	'''! Get readings from UV light sensor
	@return if normal -> uvs, light, uvi, ltr_lux, ltr_gain, ltr_resolution, ltr_window_factor, ltr_measurement_delay
	@return if error  -> -1, -1, -1, -1, -1, -1, -1, -1
	'''
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
		except Exception as e:
			logging.error(e)
			return -1,-1,-1,-1,-1,-1,-1,-1

def get_spectrometer():
	'''
	Dictionary keys:
		['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
	'''

	'''! Get readings from photo spectrometer
	@return if normal -> {'c_415nm':val, 'c_445nm':val, 'c_480nm':val, 'c_515nm':val, 'c_555nm':val, 'c_590nm':val, 'c_630nm':val, 'c_680nm':val, 'clear':val, 'nir':val}
	@return if error  -> {'c_415nm':0,'c_445nm':0,'c_480nm':0,'c_515nm':0,'c_555nm':0,'c_590nm':0,'c_630nm':0,'c_680nm':0,'clear':0,'nir':0}
	'''
	try:
		channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
		x=get_serial_vals(d['SPEC_CODE'],channels)
		return x
	except Exception as e:
		logging.error(e)
		return {'c_415nm':0,'c_445nm':0,'c_480nm':0,'c_515nm':0,'c_555nm':0,'c_590nm':0,'c_630nm':0,'c_680nm':0,'clear':0,'nir':0}

# -------------------------------------------------
def get_pm25():
	'''
	Dictionary keys:
		['03um', '05um', '10um', '25um', '50um', '100um']
	'''

	'''! Get particulate matter readings
	@return if normal -> [val, val, val, val, val, val]
	@return if error -> [1, 1, 1, 1, 1, 1]
	'''

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
	except Exception as e:
		logging.error(e)
		return [1, 1, 1, 1, 1, 1]

def get_noise():
	'''
	Dictionary keys:
		['noise_out']
	'''
	'''! Get analog value from electret microphone
	@return if normal -> noise_out
	@return if error  -> 0
	'''
	try:
		x=get_serial_vals(d['NOISE_CODE'],['noise_out'])
		return int(x['noise_out'])
	except Exception as e:
		logging.error(e)
		return 0

def get_wind():
	'''! Read analog value from wind sensor.
	@warning This works differently from others.
	@return if normal -> wind_val
	@return if error  -> -1
	'''
	try:
		# my_flush()
		ser.write(WIND_CODE.encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
		return int(curr_line)
	except Exception as e:
		logging.error (f"{e}: wind error")
		return -1

# -------------------------------------------------
def get_multimeter():
	'''! Get readings from current sensor INA219
	@warning This works differently from others.
	@return if normal -> current, voltage, power
	@return if error  -> -1, -1, -1
	'''
	try:
		# my_flush()
		ser.write(d['CURRENT_CODE'].encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')
		return float(curr_line[0]),float(curr_line[1]),float(curr_line[2])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_gps():
	'''
	Dictionary keys:
		['lat', 'lng', 'alt', 'spd', 'sat']
	'''

	'''! Read data from GPS sensor
	@return if normal -> latitude, longitude, altitude, speed, num satellites
	@return if error  -> -1, -1, -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['GPS_CODE'],['lat','lng','alt','spd','sat'])
		return float(x['lat']),float(x['lng']),float(x['alt']),float(x['spd']),int(x['sat'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1,-1,-1

def get_battery():
	'''
	Get battery voltage & percentage from Adafruit fuel gauge

	:Dictionary keys: ['volt', 'pct', 'temp']
	:return:
		:normal: voltage, battery pct, battery temperature
		:error: -1, -1, -1

	'''

	'''! Get battery voltage & percentage from Adafruit fuel gauge
	@return if normal -> voltage, battery pct, battery temperature
	@return if error  -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['BATTERY_CODE'],['volt','pct','temp'])
		return float(x['volt']),float(x['pct']),float(x['temp'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_radiation():
	'''
	Dictionary keys:
		['CPM']
	'''

	'''! Read analog value from geiger counter module
	@return if normal -> CPM
	@return if error  -> -1
	'''
	try:
		x=get_serial_vals(d['RADIATION_CODE'],['CPM'])
		return float(x['CPM'])
	except Exception as e:
		logging.error(e)
		return -1

# --------- Inertial measurement unit --------- #
def get_imu_orientation():
	'''
	Dictionary keys:
		['Hd','Rl','Ph']
	'''

	'''! BNO055 IMU: get heading, roll, pitch
	@return if normal -> heading, roll, pitch
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_ORIENTATION_CODE'],['Hd','Rl','Ph'])
		return float(x['Hd']),float(x['Rl']),float(x['Ph'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_imu_ang_vel():
	'''
	Dictionary keys:
		['X','Y','Z']
	'''

	'''! BNO055 IMU: get x/y/z axes angular velocity
	@return if normal -> x, y, z
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_ANG_VEL_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_imu_lin_acc():
	'''
	Dictionary keys:
		['X','Y','Z']
	'''

	'''! BNO055 IMU: get x/y/z axes linear acceleration
	@return if normal -> x, y, z
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_LIN_ACC_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_imu_acc():
	'''
	Dictionary keys:
		['X','Y','Z']
	'''

	'''! BNO055 IMU: get x/y/z axes overall acceleration
	@return if normal -> x, y, z
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_ACC_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_imu_mag():
	'''
	Dictionary keys:
		['X','Y','Z']
	'''

	'''! BNO055 IMU: get x/y/z axes magnetic field strength
	@return if normal -> x, y, z
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_MAG_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

def get_imu_grav():
	'''
	Dictionary keys:
		['X','Y','Z']
	'''

	'''! BNO055 IMU: get x/y/z axes readings for adjusted gravitational acceleration
	@return if normal -> x, y, z
	@return if  error -> -1, -1, -1
	'''
	try:
		x=get_serial_vals(d['IMU_GRAV_CODE'],['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])
	except Exception as e:
		logging.error(e)
		return -1,-1,-1

# -------------- VIS/IR light sensor  -------------- #
def set_tsl_scl_disconnect():
	'''! Disconnect the SCL signal for TSL2591 vis/ir sensor'''
	ser.write(TSL_SCL_DISCONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_tsl_scl_connect():
	'''! Reconnect the SCL signal for TSL2591 vis/ir sensor'''
	ser.write(TSL_SCL_CONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_tsl_gain(new_gain):
	'''! Set gain of TSL2591 vis/ir sensor'''
	ser.write(new_gain.encode('utf-8'))
	ser.readline()

# ------------------- PM25 ------------------------- #
def set_pm25_power_off():
	'''! Disconnect power to PM25 sensor by switching assigned mosfet'''
	ser.write(PM25_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_pm25_power_on():
	'''! Reconnect power to PM25 sensor by switching assigned mosfet'''
	ser.write(PM25_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_geiger_power_off():
	'''! Disconnect power to geiger counter module by switching assigned mosfet'''
	ser.write(GEIGER_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())

def set_geiger_power_on():
	'''! Reconnect power to geiger counter module by switching assigned mosfet'''
	ser.write(GEIGER_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())

# -------------------------------------------------
def get_serial_vals(send_msg,dict_names_list):
	'''! @brief Main function actually responsible for serial communication msg send/recv.
		@param send_msg Message (i.e., code) to be sent.
		@param dict_names_list Sensor specific names for returned name/value pairs.
		@returns Dictionary with name-value pairs specified in dict_names_list.

		@note This is a note

	'''

	'''More comment'''
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
	'''! Dump serial vals'''
	while (len(ser.readline())>0):
		logging.warning ('dumping serial vals')

