HOME_DIR='/home/pi/Sensor_Scripts/pygame_code/tricorder/'
MAX_BYTES=1016

LOGS_DIR='/home/pi/Sensor_Scripts/logs/'
header_row='day,date,time,lux,infrared,visible,full_spectrum,uvs,light,gain,uvi,ltr_lux,channel_415nm,channel_445nm,channel_480nm,channel_515nm,channel_555nm,channel_590nm,channel_630nm,channel_680nm,temperature,relative_humidity,pressure,bmp_temperature,03um,05um,10um,25um,50um,100um,eCO2,TVOC,baseline_eCO2,baseline_TVOC\n'
LOG_FILE_PREFIX='sensors_log_home_'

PERIPHERAL_MODE='serial'
# PERIPHERAL_MODE='bluetooth'

SENSOR_DICT={'lux':"-1",'infrared':"-1",'visible':"-1",'full_spectrum':"-1",'tsl2591_gain':"-1",
					 'uvs':"-1",'light':"-1",'uvi':"-1",'ltr_lux':"-1",'ltr_gain':"-1",'ltr_res':"-1",'ltr_win_fac':"-1",'ltr_mdelay':"-1",
					 'c_415nm':"-1",'c_445nm':"-1",'c_480nm':"-1",'c_515nm':"-1",'c_555nm':"-1",'c_590nm':"-1",'c_630nm':"-1",'c_680nm':"-1",'spec_gain':"-1",'FLICKER':"-1",
					 'temperature':"-1",'relative_humidity':"-1",'heater':"-1",'h_res':"-1",'t_res':"-1",
					 'pressure':"-1",'bmp_temp':"-1",'p_over':"-1",'t_over':"-1",
					 '03um':"-1",'05um':"-1",'10um':"-1",'25um':"-1",'50um':"-1",'100um':"-1",
					 'eCO2':"-1",'TVOC':"-1",'baseline_eCO2':"-1",'baseline_TVOC':"-1",
		 }

SENSOR_LIST=['lux','infrared','visible','full_spectrum','tsl2591_gain','uvs','light','uvi','ltr_lux','ltr_gain','ltr_res','ltr_win_fac','ltr_mdelay','c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','spec_gain','FLICKER','temperature','relative_humidity','heater','h_res','t_res','pressure','bmp_temp','p_over','t_over','03um','05um','10um','25um','50um','100um','eCO2','TVOC','baseline_eCO2','baseline_TVOC']

if __name__=='__main__':
	outstr=''
	for k,v in SENSOR_DICT.items():
		outstr+=f'\'{k}\','
	print (outstr)