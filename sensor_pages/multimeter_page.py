'''! Read and plot values of current, voltage, and power from the current sensor.'''

import pygame
from page_templates import PageTemplate
from fonts import FONT_DIN, FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW, LIGHT_GREY, WHITE

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams['font.size'] = 10
COLOR = (0.75,0.75,0.75)
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

from plotting_functions import plot2img
import matplotlib.backends.backend_agg as agg
from pygame import gfxdraw, Surface
import pygame.event as e
from serial_manager import get_multimeter
import logging

class MultimeterPage(PageTemplate):
	'''! For visualizing volt/current/powerndata from current sensor'''
	def __init__(self,name):
		super().__init__(name)
		self.prev_page_name='menu_home_page'
		self.num_tics=3
		self.current=-1
		self.voltage=-1
		self.power=-1

		self.frame_count=0

		# --- graphing stuff --- #
		self.rolling_tics=50
		self.curr_array=[]
		self.voltage_array=[]
		self.power_array=[]
		self.fig = plt.figure(figsize=[6,1.3])
		self.ax = self.fig.add_subplot(111)
		self.canvas = agg.FigureCanvasAgg(self.fig)
		self.ax.set_frame_on(False)

		self.current_line_surf=Surface((1,1))
		self.voltage_line_surf=Surface((1,1))
		self.power_line_surf=Surface((1,1))

	def render_generic_graph(self,plot_array,color='r'):
		'''! returns line plot as img'''
		self.ax.clear()
		self.ax.cla()
		self.ax.plot(plot_array,color=color)
		try:
			self.ax.set_ylim(bottom=min(plot_array),top=max(plot_array))
		except Exception as e:
			logging.debug(e)
		line_surf=plot2img(self.fig,self.ax,self.canvas)
		return line_surf

	def blit_all(self,screen,line_surf,curr_row,title,val):
		'''! Generic function for blitting line plots'''
		increment_val=215
		FONT_DIN.render_to           (screen, (155,curr_row),  title,           DARK_YELLOW, style=0,size=30)
		FONT_HELVETICA_NEUE.render_to(screen, (330,curr_row), val,  WHITE,       style=0,size=35)
		screen.blit(line_surf, (120,curr_row+40))
		curr_row+=increment_val
		return curr_row

	def array_handler(self,arr,new_val,color):
		'''! Trims the plotting array'''
		if len(arr)>self.rolling_tics:
			arr=arr[1:]
		arr.append(new_val)
		return arr,self.render_generic_graph(arr,color=color)

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		# FONT_FEDERATION.render_to(screen, (150, 67), 'MULTIMETER', ORANGE,style=0,size=40)
		# FONT_FEDERATION.render_to(screen, (150, 117), 'INA290', DARK_YELLOW,style=0,size=34)

		if self.frame_count%self.num_tics:
			self.current,self.voltage,self.power=get_multimeter()

			self.voltage=self.voltage/1000

			self.curr_array,self.current_line_surf=self.array_handler(self.curr_array,self.current,'g')
			self.voltage_array,self.voltage_line_surf=self.array_handler(self.voltage_array,self.voltage,'r')
			self.power_array,self.power_line_surf=self.array_handler(self.power_array,self.power,'y')

		curr_row=80 #220

		curr_row=self.blit_all(screen,self.current_line_surf,curr_row,"Current:",f"{self.current} mA")
		curr_row=self.blit_all(screen,self.voltage_line_surf,curr_row,"Voltage:",f"{self.voltage} V")
		curr_row=self.blit_all(screen,self.power_line_surf,curr_row,"Power:",f"{self.power} mW")

		self.frame_count+=1
		return self.next_screen_name,self.kwargs