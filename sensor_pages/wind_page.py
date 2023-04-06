from page_templates import PageTemplate
from fonts import FONT_FEDERATION, ORANGE, DARK_YELLOW
import pygame.event as e
from custom_user_events import REQUEST_WIND
import matplotlib.pyplot as plt
from plotting_functions import *
import matplotlib.backends.backend_agg as agg
from pygame import gfxdraw


# from tricorder import ser
from serial_manager import *

import numpy as np

class WindSensorPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)
		self.prev_page_name='mobile_home_page_1'
		self.wind_out=0
		self.frame_count=0
		self.color_list=['wind']
		self.color_labels=['wind']
		self.num_tics=1


		self.rolling_tics=50
		self.x=[0]

		# ---
		self.fig = plt.figure(figsize=[5,4])
		self.ax = self.fig.add_subplot(111)
		self.canvas = agg.FigureCanvasAgg(self.fig)
		self.ax.set_frame_on(False)
		self.line_surf=pygame.Surface((1,1))

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)


		FONT_FEDERATION.render_to(screen, (150, 67), 'Wind Speed', ORANGE,style=0,size=40)
		FONT_FEDERATION.render_to(screen, (150, 117), (str(self.x[-1])), DARK_YELLOW,style=0,size=34)


		if (self.frame_count%self.num_tics==0):

			if len(self.x)>self.rolling_tics:
				self.x=self.x[1:]

			# if self.frame_count%5==0:
			# e.post(REQUEST_WIND)
			# self.x.append(int(self.wind_out))
			# j=get_wind(ser)
			# print (j)
			# self.x+=j
			try:
				self.x.append(get_wind())


			# self.line_surf = line_plot(self.fig3,self.ax3,self.canvas3,self.color_list,self.x,self.array_dict)

				self.ax.clear()
				self.ax.cla()
				self.ax.plot(self.x,color='r')
				self.ax.set_ylim(bottom=min(self.x),top=max(self.x))
				self.line_surf=plot2img(self.fig,self.ax,self.canvas)

			except Exception as e:
				print ('get_wind err')
				print (e)


		screen.blit(self.line_surf, (120,150))

		# x, y, width, height = screen.get_rect()
		# x+=100
		# freqs = height-np.floor((self.x)*height)
		# print (freqs)
		# ylast = self.x[0]
		# for i in range(1, len(self.x)):
		# 	y = int(self.x[i]/7)
		# 	i+=80
		# 	i*=2
		# 	pygame.draw.line(screen, (  0, 255, 128), (i-1, 720-ylast), (i, 720-y))
		# 	# print ((i-1, ylast), (i, y))
		# 	ylast = y
		# # print()





		# pixel_col=160
		# pixel_row=520


		# m=np.linspace(160, 600, num=50)
		# x_positions = m.astype(int)

		# for col_num in x_positions:
		# 	gfxdraw.pixel(screen, col_num, pixel_row, (255,255,255))

		# for item in self.x:
		# 	item/=7

		# y_last=self.x[0]
		# for i in range(1, len(x_positions)-1):
		# 	y1=self.x[i]
		# 	y2=self.x[i+1]
		# 	pygame.draw.line(screen, (  255, 0, 0), (x_positions[i], y1), (x_positions[i+1], y2))
		# 	print ((x_positions[i], y1), (x_positions[i+1], y2))
		# 	# y_last=self.x[i+1]



		# # print ([self.x[0]]+self.x)

		# # for pixel_num in range(120):
		# # 	for z in range(1):
		# # 		gfxdraw.pixel(screen, pixel_col+z, pixel_row, (255,255,255))
		# # 	pixel_col+=3

		self.frame_count+=1

		return self.next_screen_name,self.kwargs
