from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN
from colors import ORANGE
from buttons import ButtonClass,long_button_blue,long_button_blue_pressed

class SettingsPage(PageTemplate):
	'''Meant for changing device settings'''
	def __init__(self,name):
		super().__init__(name)
		self.button_list+=self.init_buttons()
		self.button_mapping={
							'home_button':'menu_home_page',
							'Num Pad':'numpad_page',
							'Exit':'exit'}

	def init_buttons(self):
		butt_list=[]
		col=165
		row=90
		button_h=115
		y_spacing=35
		f_size=60
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Backlight',font_size=f_size,style=0,font_color=ORANGE,name='Backlight'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Slider',font_size=f_size,style=0,font_color=ORANGE,font=FONT_DIN,name='slider'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Num Pad',font_size=f_size,style=0,font_color=ORANGE,name='Num Pad'))
		row+=button_h+y_spacing
		butt_list.append(ButtonClass(1,long_button_blue,long_button_blue_pressed,col,row,text='Exit',font_size=f_size,style=0,font_color=ORANGE,name='Exit'))
		return butt_list

	def handle_events_custom(self,screen,curr_events):

		self.handle_events(screen,curr_events)

		# for event in curr_events:
		# 	if (event.type==pygame.MOUSEBUTTONUP or event.type==pygame.FINGERUP):
		# 		self.reset_subpage()

		# 	# Dragging with mouse
		# 	scale=2
		# 	if event.type==pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
		# 		curr_x,curr_y=pygame.mouse.get_pos()
		# 		dx=curr_x-self.prev_x
		# 		if 0<abs(dx)<100:
		# 			for button in self.buttons_list:
		# 				button.rectangle.left+=(dx*scale)
		# 		self.prev_x=curr_x
		# 		self.prev_y=curr_y

		# 	# Dragging with finger
		# 	if event.type==pygame.FINGERMOTION:
		# 		curr_x,curr_y=event.x*screen.get_width(),event.y*screen.get_height()
		# 		dx=curr_x-self.prev_x

		# 		if 0<abs(dx)<100:
		# 			for button in self.buttons_list:
		# 				button.rectangle.left+=dx
		# 		self.prev_x=curr_x
		# 		self.prev_y=curr_y

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		# screen.blit(lcars_bg,(0,0))
		pressed_button=self.handle_events(screen,curr_events)

		if pressed_button!=None:
			if pressed_button.name in self.button_mapping.keys():
				self.next_screen_name=self.button_mapping[pressed_button.name]

			if pressed_button.name=='Num Pad':
				self.next_screen_name='numpad_page'
				self.kwargs['prev_page_name']="settings_page"
				# return self.next_screen_name,{'prev_page_name':self.name}

			# if pressed_button.name=='slider':
				# self.next_screen_name='slider_test_page'


		return self.next_screen_name,self.kwargs
