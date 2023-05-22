'''! @brief Shows statistics about the RaspberryPi and the running application.
@file device_stats_page.py Shows statistics about the RaspberryPi and the running application.
'''

from page_templates import DeviceStatsPageTemplate
from fonts import FONT_FEDERATION, FONT_DIN
from colors import SLATE, DARK_YELLOW,  WHITE
from subprocess import PIPE, Popen
import psutil
from exit_page import elapsed_time

class DeviceStatsPage(DeviceStatsPageTemplate):
	'''! Shows statistics about the RaspberryPi and the running application.'''
	def __init__(self,name):
		'''! Constructor'''
		super().__init__(name)
		## Current subpage number.
		self.pg_id=0
		# self.kwargs={} #reset kwargs
		# self.button_list+=self.init_buttons()
		## Return page.
		self.prev_page_name='menu_home_page'
		## Next page
		self.next_screen_name=self.name

	def update_cpu_stats(self,dt=None):
		'''! Retrieve CPU load percentage and temperature.'''
		process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode()

		pos_start = output.index('=') + 1
		pos_end = output.rindex("'")

		cpu_temp = f'{float(output[pos_start:pos_end])}°C'
		cpu_pct=str(int(round(psutil.cpu_percent())))+'%'
		return cpu_pct,cpu_temp

	def update_up_time(self):
		'''! Returns up time of tricoder.py application.'''
		process = Popen(['uptime', '-p'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('up ','')
		output = output[0:len(output)-1]
		# print (output)
		# print (output.rstrip())
		return output

	def update_other_stats(self):
		'''! Returns amount of time spent in each governer.'''
		process = Popen(['cpufreq-info', '-m','--stats'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','').replace(' ','').split(',')
		# print (output)
		return output

	def get_curr_freq(self):
		'''! Retrieve current clock frequency in MHz.'''
		process = Popen(['cpufreq-info', '-m','--hwfreq'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','')#.replace(' ','').split(',')
		# print (output)
		return output

	def get_curr_governor(self):
		'''! Retrieve current dvfs policy.'''
		process = Popen(['cpufreq-info', '-m','--policy'], stdout=PIPE)
		output, _error = process.communicate()
		output = output.decode().replace('\n','').split(' ')
		# print (output)
		return output

	def get_mem_use(self):
		'''! Get mem stats.'''
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
		'''! Blit subpage number.'''
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