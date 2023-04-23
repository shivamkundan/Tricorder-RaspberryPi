from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from images import *
import pygame
import logging
# from colors import
# from mappings import

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
			logging.debug (f"{pressed_button.name}")
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
