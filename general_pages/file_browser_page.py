import pygame
import os
from page_templates import PageTemplate
from buttons import ButtonClass, NAV_BUTTONS_VERTICAL, simp_button, simp_button_alt, simp_button_selected
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE
from colors import ORANGE, WHITE

class FileBrowserPage(PageTemplate):
	def __init__(self,name):
		super().__init__(name)

		self.button_list+=NAV_BUTTONS_VERTICAL
		self.refresh_files_list()

		self.button_list+=self.file_button_list
		self.prev_page_name='menu_home_page'
		self.p=pygame.Surface((0,0))

		self.bg=pygame.Surface((320,320))
		self.bg.set_alpha(200)
		self.bg.fill(WHITE)

		self.curr_butt_index=0
		self.curr_butt=self.file_button_list[self.curr_butt_index]
		self.curr_butt.selected=True
		self.p=pygame.image.load(self.curr_butt.name)
		self.p=pygame.transform.scale(self.p, (300, 300))

	def refresh_files_list(self):
		self.screenshot_files=[]
		for root, dirs, files in os.walk("screenshots/", topdown=True):
			for name in files:
				self.screenshot_files.append(os.path.join(root, name))
		self.screenshot_files.sort(key=os.path.getctime,reverse=True)	# sort by date added

		self.file_button_list=[]
		self.start_y=400
		x=150
		y=self.start_y
		f_size=24
		for item in self.screenshot_files:
			# item=item.replace('screenshots/','').replace('.png','')
			self.file_button_list.append(ButtonClass(0,simp_button,simp_button_alt,x,y,name=item,text=item.replace('screenshots/','').replace('.png',''),font=FONT_HELVETICA_NEUE,font_color=WHITE,selected_img=simp_button_selected,selected_color=ORANGE,align_left=True))
			# FONT_HELVETICA_NEUE.render_to(screen, (x, y),item, WHITE,style=0,size=f_size)
			y+=65
			# for name in dirs:
			#     print(os.path.join(root, name))
		self.end_y=y

	def gruntwork(self):
		self.curr_butt=self.file_button_list[self.curr_butt_index]
		self.curr_butt.selected=True
		self.p=pygame.image.load(self.curr_butt.name)
		self.p=pygame.transform.scale(self.p, (300, 300))
		for b in self.button_list:
			if b!=self.curr_butt:
				b.selected=False

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)

		self.blit_all_buttons(screen)
		screen.blit(self.bg,(300-10,80-10))
		screen.blit(self.p,(300,80))

		self.blit_title(screen)

		# self.refresh_files_list()

		# Keyboard navigation
		for event in curr_events:

			if event.type==pygame.KEYUP:
				if (event.key == pygame.K_DOWN):

					curr_events.remove(event)

					# if self.file_button_list[0].rectangle.top-50<self.start_y:
					print(self.curr_butt_index,len(self.file_button_list))
					if self.curr_butt_index<len(self.file_button_list)-1:
						self.curr_butt_index+=1
						self.gruntwork()
						for b in self.file_button_list:
							b.rectangle.top-=65

				if (event.key == pygame.K_UP):
					curr_events.remove(event)
					print(self.curr_butt_index,len(self.file_button_list))
					if self.curr_butt_index>0:
						self.curr_butt_index-=1
						self.gruntwork()
						# if self.file_button_list[-1].rectangle.top+50>self.end_y:
						for b in self.file_button_list:
							b.rectangle.top+=65


		pressed_button=self.handle_events(screen,curr_events)
		if pressed_button!=None:
			if pressed_button in self.file_button_list:
				# try:
					self.p=pygame.image.load(pressed_button.name)
					self.p=pygame.transform.scale(self.p, (300, 300))
					if not pressed_button.selected:
						pressed_button.selected=not pressed_button.selected

					for b in self.button_list:
						if b!=pressed_button:
							b.selected=False

				# except Exception as e:
				#     print(e)

			if pressed_button.name=='up':
				if self.curr_butt_index>0:
					self.curr_butt_index-=1
					self.gruntwork()
					# if self.file_button_list[-1].rectangle.top+50>self.end_y:
					for b in self.file_button_list:
						b.rectangle.top+=65

			if pressed_button.name=='page_up':
				self.curr_butt_index=0
				self.gruntwork()
				for hh in range(len(self.file_button_list)-self.curr_butt_index+1):
					for b in self.file_button_list:
						b.rectangle.top+=65

			if pressed_button.name=='down':
				if self.curr_butt_index<len(self.file_button_list)-1:
					self.curr_butt_index+=1
					self.gruntwork()
					for b in self.file_button_list:
						b.rectangle.top-=65


			if pressed_button.name=='page_down':
				self.curr_butt_index=len(self.file_button_list)-1
				self.gruntwork()
				for hh in range(len(self.file_button_list)-self.curr_butt_index+1):
					# print (hh)
					for b in self.file_button_list:
						b.rectangle.top-=65

		return self.next_screen_name,self.kwargs

	def blit_title(self,screen):
		FONT_FEDERATION.render_to(screen, (150, 67), 'Files', ORANGE,style=0,size=44)
