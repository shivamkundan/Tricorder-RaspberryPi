#!/usr/bin/python3
'''
This file contains functions for communicating over a serial usb/bluetooth link using tcp/ip sockets. By sending data back and forth:
-> Data can be requested from sensors
-> Sensor-specific settings can be changed
-> Microcontroller operations can be changed (e.g., sleep mode)
-> Each of the above involve specific mapping from mappings.py
'''
from mappings import *
import serial
from my_logging import *
# print ("serial.VERSION:",serial.VERSION)

# set up logging
shivams_logging(script_name="tricorder",console_log_level="info",logfile_log_level="info")
logging.info (f'\n')

port_name="/dev/my_esp32"
try:
	ser = serial.Serial(
	    port=port_name, # Change this according to connection methods, e.g. /dev/ttyUSB0
	    baudrate = 115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS,
	    timeout=1
	)
	# ser.write(MCU_RESET_CODE.encode('utf-8'))
	ser.write(MCU_IND_MODE_DISABLE.encode('utf-8'))
	ser.flush()
	logging.info (f'mcu connected on {port_name}!')

except serial.serialutil.SerialException:
	logging.error (f'mcu not connected on {port_name}!')
	ser=None

# -------------------------------------------------
def get_temp_humid():

	try:
		x=get_serial_vals(TEMP_HUMID_CODE,['temperature','relative_humidity','heater','h_res','t_res'])

		c_temp=float(x['temperature'])
		humid=float(x['relative_humidity'])
		h_res=float(x['h_res'])
		t_res=float(x['t_res'])
		return c_temp,humid,h_res,t_res

	except TypeError:
		print ('type err: request temp_humid')
		return -1,-1,-1,-1
	except KeyError:
		print ('key err: request temp_humid')
		return -1,-1,-1,-1

def get_pressure():
	try:
		x=get_serial_vals(PRESSURE_CODE,['pressure','bmp_temp','p_over','t_over','alt'])

		altitude=float(x['alt'])
		pressure=float(x['pressure'])
		bmp_temp=float(x['bmp_temp'])
		p_oversampling=float(x['p_over'])
		t_oversampling=float(x['t_over'])

		return altitude,pressure,bmp_temp,p_oversampling,t_oversampling

	except TypeError:
		print ('type err: request pressure')
		return -1,-1,-1,-1,-1
	except KeyError:
		print ('key err: request pressure')
		return -1,-1,-1,-1,-1

def get_tvoc_eco2():
	try:
		x=get_serial_vals(TVOC_CODE,['eCO2','TVOC','raw_H2','raw_ethanol','baseline_eCO2','baseline_TVOC'])

		TVOC=x['TVOC']
		eCO2=x['eCO2']
		baseline_eCO2=x['baseline_eCO2']
		baseline_TVOC=x['baseline_TVOC']

		return TVOC,eCO2,baseline_eCO2,baseline_TVOC

	except TypeError:
		print ('type err: request tvoc')
		return -1,-1,-1,-1
	except KeyError:
		print ('key err: request tvoc')
		return -1,-1,-1,-1

# -------------------------------------------------
def get_vis_ir():
	try:
		x=get_serial_vals(VIS_IR_CODE,['lux','infrared','visible','full_spectrum','tsl2591_gain'])

		lux=float(x['lux'])
		ir=int(x['infrared'])
		gain=x['tsl2591_gain']
		visible=float(x['visible'])
		full_spectrum=float(x['full_spectrum'])

		return lux,ir,gain,visible,full_spectrum

	except TypeError:
		print ('type err: request vis_ir')
		return -1,-1,-1,-1,-1
	except KeyError:
		print ('key err: request vis_ir')
		return -1,-1,-1,-1,-1

def get_uv():
	x=get_serial_vals(UV_CODE,['uvs','light','uvi','ltr_lux','ltr_gain','ltr_res','ltr_win_fac','ltr_mdelay'])

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
		except TypeError:
			print ('type err: request uv')
			return -1,-1,-1,-1,-1,-1,-1,-1
		except KeyError:
			print ('key err: request uv: ',x)
			return -1,-1,-1,-1,-1,-1,-1,-1

def get_spectrometer():
	try:
		channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
		x=get_serial_vals(SPEC_CODE,channels)

		return x

	except TypeError:
		print ('type err: request spectrometer')
		return [1,1,1,1,1,1,1,1,1,1]
	except KeyError:
		print ('key err: request spectrometer')
		return [1,1,1,1,1,1,1,1,1,1]

# -------------------------------------------------
def get_pm25():
	try:
		aqdata=[]
		x=get_serial_vals(PM25_CODE,['03um','05um','10um','25um','50um','100um'])
		aqdata.append(x['03um'])
		aqdata.append(x['05um'])
		aqdata.append(x['10um'])
		aqdata.append(x['25um'])
		aqdata.append(x['50um'])
		aqdata.append(x['100um'])
		# print ('aq: ',aqdata)
		return aqdata

	except Exception as e:
		print ("pm25 error: ",e)
		return [1, 1, 1, 1, 1, 1]
	except KeyError:
		print ('key err: request pm25')
		return [1, 1, 1, 1, 1, 1]

def get_noise():
	try:
		x=get_serial_vals(NOISE_CODE,['noise_out'])
		return int(x['noise_out'])
	except TypeError:
		print ('type err: request noise')

def get_wind():
	try:
		# my_flush()
		ser.write(WIND_CODE.encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')

		# return int(curr_line[0]),int(curr_line[1]),int(curr_line[2])
		return int(curr_line)

	except Exception as e:
		print ('wind error')
		print (e)
		return -1

# -------------------------------------------------
def get_multimeter():
	try:
		# my_flush()
		ser.write(CURRENT_CODE.encode('utf-8'))
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')
		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n').split(' ')

		return float(curr_line[0]),float(curr_line[1]),float(curr_line[2])

	except:
		print ('multimeter error')
		return -1,-1,-1

def get_gps():
	try:
		x=get_serial_vals(GPS_CODE,['lat','lng','alt','spd','sat'])
		return float(x['lat']),float(x['lng']),float(x['alt']),float(x['spd']),int(x['sat'])

	except TypeError:
		print ('type err: request gps')
		return -1,-1,-1,-1,-1
	except KeyError:
		print ('key err: request gps')
		return -1,-1,-1,-1,-1

def get_battery():
	try:
		x=get_serial_vals(BATTERY_CODE,['volt','pct','temp'])

		return float(x['volt']),float(x['pct']),float(x['temp'])

	except TypeError:
		print ('type err: request battery')
		return -1,-1,-1
	except KeyError:
		print ('key err: request battery')
		return -1,-1,-1

def get_radiation():
	try:
		x=get_serial_vals(RADIATION_CODE,['CPM'])
		# self.screen_dict['radiation_sensor_page'].x.append(float(x['CPM']))
		return float(x['CPM'])

	except TypeError:
		print ('type err: request radiation')
		return -1
	except KeyError:
		print ('key err: request radiation')
		return -1

# -------------------------------------------------
def get_imu_orientation():
	try:
		x=get_serial_vals(IMU_ORIENTATION_CODE,['Hd','Rl','Ph'])

		return float(x['Hd']),float(x['Rl']),float(x['Ph'])

	except TypeError:
		print ('type err: request imu orientation')
		return -1,-1,-1
	except KeyError:
		print ('key err: request orientation')
		return -1,-1,-1

def get_imu_ang_vel():
	try:
		x=get_serial_vals(IMU_ANG_VEL_CODE,['X','Y','Z'])

		return float(x['X']),float(x['Y']),float(x['Z'])

	except TypeError:
		print ('type err: request imu angular velocity')
		return -1,-1,-1
	except KeyError:
		print ('key err: request ')
		return -1,-1,-1

def get_imu_lin_acc():
	try:
		x=get_serial_vals(IMU_LIN_ACC_CODE,['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])

	except TypeError:
		print ('type err: request imu accelerometer')
		return -1,-1,-1
	except KeyError:
		print ('key err: request ')
		return -1,-1,-1

def get_imu_acc():
	try:
		x=get_serial_vals(IMU_ACC_CODE,['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])

	except TypeError:
		print ('type err: request imu linear acc')
		return -1,-1,-1
	except KeyError:
		print ('key err: request ')
		return -1,-1,-1

def get_imu_mag():
	try:
		x=get_serial_vals(IMU_MAG_CODE,['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])

	except TypeError:
		print ('type err: request imu linear acc')
		return -1,-1,-1
	except KeyError:
		print ('key err: request ')
		return -1,-1,-1

def get_imu_grav():
	try:
		x=get_serial_vals(IMU_GRAV_CODE,['X','Y','Z'])
		return float(x['X']),float(x['Y']),float(x['Z'])

	except TypeError:
		print ('type err: request imu linear acc')
		return -1,-1,-1
	except KeyError:
		print ('key err: request ')
		return -1,-1,-1

# -------------------------------------------------
def set_tsl_scl_disconnect():
	ser.write(TSL_SCL_DISCONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

def set_tsl_scl_connect():
	ser.write(TSL_SCL_CONNECT_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

def set_tsl_gain(new_gain):
	ser.write(new_gain.encode('utf-8'))
	ser.readline()

# -------------------------------------------------
def set_pm25_power_off():
	ser.write(PM25_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

def set_pm25_power_on():
	ser.write(PM25_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

def set_geiger_power_off():
	ser.write(GEIGER_PWR_OFF_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

def set_geiger_power_on():
	ser.write(GEIGER_PWR_ON_CODE.encode('utf-8'))
	curr_line=(ser.readline())#.decode('utf-8').lstrip(' ').rstrip('\r\n')

# -------------------------------------------------
def get_serial_vals(send_msg,dict_names_list):
		# ==========================================
		# serial.serialutil.SerialException:
	# try:
		# while (len(ser.readline())>0):
		# 	print ('dumping serial vals')


		# ser.flush()

		recv_msg={}

		for char in send_msg.rstrip(' ').split(' '):
			# print ('char:',char)

			ser.write(send_msg.encode('utf-8'))


			curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
			# print ("curr_line: ",curr_line)

			if curr_line=="":

				curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
				# print ("curr_line 2: ",curr_line)

			# if (ser.inWaiting() > 0):
			# 	curr_line = ser.read(ser.inWaiting()).decode('ascii')


			for item,name in zip(curr_line.split(' '),dict_names_list):
				try:
					val=item.split(":")[1]
				except IndexError:
					val=-1
				# print (val)
				recv_msg[name]=val
			print (send_msg,":",recv_msg)

		return recv_msg
	# except:
	# # except serial.serialutil.SerialException:
	# 	pass


		# ==========================================

def my_flush():
	while (len(ser.readline())>0):
		print ('dumping serial vals')

