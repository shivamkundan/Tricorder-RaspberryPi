from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW, ORANGE, WHITE
import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg
from pygame import gfxdraw
from images import RESET_BUTTON, RESET5_BUTTON

from serial_manager import get_radiation,set_geiger_power_off,set_geiger_power_on

import numpy as np

import logging

class GeigerCounterPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.prev_page_name='menu_home_page'
		self.wind_out=0
		self.frame_count=0
		self.cpm=0


		self.rolling_tics=200
		self.x=[]
		self.avg_array=[]

		# ---
		self.fig = plt.figure(figsize=[5,4])
		self.ax = self.fig.add_subplot(111)
		self.canvas = agg.FigureCanvasAgg(self.fig)
		self.ax.set_frame_on(False)
		self.line_surf=pygame.Surface((1,1))

		self.button_list+=[RESET_BUTTON,RESET5_BUTTON]

	def on_enter(self):
		logging.info(f"entering {self.__class__.__name__}")
		set_geiger_power_on()


	def on_exit(self):
	    set_geiger_power_off()

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:
			if pressed_button.name=='reset':
				self.x=[]
				self.avg_array=[]
			if pressed_button.name=='reset5':
				if len(self.x)>5:
					self.x=self.x[:len(self.x)-5]
					self.avg_array=self.avg_array[:len(self.avg_array)-5]

		FONT_FEDERATION.render_to(screen, (150, 67), 'Radiation', ORANGE,style=0,size=40)
		FONT_FEDERATION.render_to(screen, (150, 117), "Geiger Counter", DARK_YELLOW,style=0,size=30)


		if (self.frame_count%3==0):

			if len(self.x)>self.rolling_tics:
				self.x=self.x[1:]
				self.avg_array=self.avg_array[1:]

			# if self.frame_count%5==0:
			# e.post(REQUEST_RADIATION)
			self.cpm=get_radiation()
			self.x.append(self.cpm)

			# if w>0:
			self.avg_array.append( np.mean(np.array(self.x)))

			# self.line_surf = line_plot(self.fig3,self.ax3,self.canvas3,self.color_list,self.x,self.array_dict)

			self.ax.clear()
			self.ax.cla()
			self.ax.plot(self.x,color='r',label='CPM')
			self.ax.plot(self.avg_array,color='g',label='AVG')
			self.ax.legend(loc='upper center',bbox_to_anchor=(0.5, 1.2),ncol=2,frameon=False)
			self.ax.set_ylim(bottom=min(self.x),top=max(self.x))
			self.line_surf=plot2img(self.fig,self.ax,self.canvas)


		screen.blit(self.line_surf, (120,150))

		FONT_FEDERATION.render_to(screen, (193, 574), "CPM", ORANGE,style=1,size=25)
		FONT_FEDERATION.render_to(screen, (415, 574), "AVG", ORANGE,style=1,size=25)

		try:
			FONT_FEDERATION.render_to(screen, (193, 574+30), str(int(round(self.x[-1],0))), WHITE,style=0,size=23)
			FONT_FEDERATION.render_to(screen, (415, 574+30), str(int(round(self.avg_array[-1],0))), WHITE,style=0,size=23)
		except Exception as e:
			logging.error (e)

		self.frame_count+=1

		return self.next_screen_name,self.kwargs
