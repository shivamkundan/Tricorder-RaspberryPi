import pygame
import os, sys
import time,datetime
from fonts import *
from colors import *
import math
from paths_and_utils import IMG_PATH,LCARS_PATH,ICONS_PATH

class ButtonClass():
	def __init__(self,butt_id,button_img,alt_img,pos_x,pos_y,selected_img=None,selected_alt_img=None,cooldown_val=5,icon=None,text='',font=FONT_FEDERATION,style=0,font_size=16,name='',font_color=FONT_BLUE,selected=False,selected_color=GREEN,required_cooldown=10,align_left=False):
		self.butt_id=butt_id
		self.img=button_img
		self.alt_img=alt_img
		# self.pos_x=pos_x
		# self.pos_y=pos_y
		self.cooldown_val=0
		self.required_cooldown=required_cooldown
		self.pressed=False
		self.text=text
		self.font=font
		self.font_size=font_size
		self.name=name
		self.rectangle=self.img.get_rect()
		self.rectangle.top=pos_y
		self.rectangle.left=pos_x
		self.orig_rectangle_top=self.rectangle.top
		self.orig_rectangle_left=self.rectangle.left
		self.cooldown=False
		self.style=style
		self.selected_img=selected_img
		self.selected_alt_img=selected_alt_img
		self.icon=icon
		self.fgcolor=font_color
		self.selected=selected
		self.selected_color=selected_color
		self.align_left=align_left

	def blit_button(self,screen):
		if self.selected:
			fg=self.selected_color
			if self.selected_img!=None:
				img=self.selected_img
			else:
				img=self.img
		else:
			fg=self.fgcolor
			img=self.img

		if (self.pressed==True) or (self.cooldown_val>0):

			if self.selected_alt_img!=None:
				if not self.selected:
					screen.blit(self.alt_img,self.rectangle)
				else:
					screen.blit(self.selected_alt_img,self.rectangle)
			else:
				screen.blit(self.alt_img,self.rectangle)
		else:
			screen.blit(img,self.rectangle)

		# Blit button text
		curr_txt=self.font.render(self.text,fgcolor=fg,style=self.style,rotation=0,size=self.font_size)
		j=list(curr_txt)
		# print (j)
		w=j[1][2]
		h=j[1][3]
		if self.align_left:
			x=self.rectangle.left
		else:
			x= self.rectangle[0]+self.rectangle[2]//2-w//2
		y=self.rectangle[1]+self.rectangle[3]//2-h//2
		self.pos_x,self.pos_y=x,y
		screen.blit(j[0],(self.pos_x,self.pos_y))

		if self.cooldown_val>0:
			pass
		else:
			self.release()

	def update_position(self,pos_x):
		self.rectangle=self.img.get_rect()
		self.rectangle.left=pos_x
		self.rectangle.top=self.orig_rectangle_top
		# print (self.rectangle.left,self.pos_x,self.pos_y)

	def update_y_pos(self,pos_y):
		self.rectangle=self.img.get_rect()
		self.rectangle.top=pos_y        # print (self.rectangle.left,self.pos_x,self.pos_y)
		self.rectangle.left=self.orig_rectangle_left

	def reset_position(self):
		self.rectangle.top=self.orig_rectangle_top
		self.rectangle.left=self.orig_rectangle_left

	def press(self):
		self.pressed=True
		# self.blit_button()

	def release(self):
		self.pressed=False
		# self.blit_button()


# --- Number pad buttons --- #
width=170
height=100
numpad_button=pygame.Surface((width, height))
r=pygame.Rect(0,0,width,height)
pygame.draw.rect(numpad_button,LIGHT_BLUE,r)
numpad_button_alt=pygame.Surface((width, height))
pygame.draw.rect(numpad_button_alt,ORANGE,r)


# --- File page buttons --- #
width=400
height=50
r=pygame.Rect(0,0,width,height)

simp_button=pygame.Surface((width, height))
simp_button.set_alpha(0)
simp_button.fill(BLACK)

simp_button_alt=pygame.Surface((width, height))
simp_button_alt.set_alpha(128)
simp_button_alt.fill(WHITE)

simp_button_selected=pygame.Surface((width, height))
simp_button_selected.set_alpha(20)
simp_button_selected.fill(WHITE)

# ------------------------------------ misc buttons ------------------------------------------------------ #
button_long_simple=pygame.image.load(ICONS_PATH+'long_button.png')
button_long_simple_alt=pygame.image.load(ICONS_PATH+'long_button_pressed.png')

simple_button_short=pygame.image.load(ICONS_PATH+'simple_short_button.png')
simple_button_short_alt=pygame.image.load(ICONS_PATH+'simple_short_button_pressed.png')

simple_button=pygame.image.load(ICONS_PATH+'simple_button.png')
simple_button_alt=pygame.image.load(ICONS_PATH+'simple_button_pressed.png')

quarter_button=pygame.image.load(LCARS_PATH+'/Picard/quarter_button.png')
quarter_button_alt=pygame.image.load(LCARS_PATH+'/Picard/quarter_button_selected.png')

long_button_blue=pygame.image.load(ICONS_PATH+'long_button_blue.png')
long_button_blue_pressed=pygame.image.load(ICONS_PATH+'long_button_blue_pressed.png')

slide_switch_blank=pygame.image.load(ICONS_PATH+'slide_switch_blank.png')

# =====================================================================================================
pref_buttons=[]
path=LCARS_PATH+'/Picard/'
for color_name in ['_blue','_orange']:
	prefix=path+'preferences'+color_name
	pref_buttons.append(pygame.transform.scale(pygame.image.load(prefix+'.png'),(97,97)))
	pref_buttons.append(pygame.transform.scale(pygame.image.load(prefix+'_pressed.png'),(97,97)))

PREF_BUTTON=ButtonClass(0,pref_buttons[0],pref_buttons[1],585,60,name='preferences',selected_img=pref_buttons[2],selected_alt_img=pref_buttons[3])

edit_icon=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/edit_icon.png'))
edit_icon_pressed=pygame.image.load(os.path.join(LCARS_PATH,'Picard/mobile_style_icons/edit_icon_pressed.png'))
EDIT_BUTTON=ButtonClass(0,edit_icon,edit_icon_pressed,385,200,name='edit')

# numpad_blue_pressed.png
# numpad_orange_pressed.png
# numpad_orange.png
# numpad_blue.png

# --- play/pause
play_pause=['reset','reset_pressed','reset5','reset5_pressed','play_orange','play_orange_pressed','pause_orange','pause_orange_pressed',
			'play_blue','play_blue_pressed','pause_blue','pause_blue_pressed',
			'scale_blue','scale_blue_pressed','scale_orange','scale_orange_pressed',
			'color_palette_blue','color_palette_blue_pressed','color_palette_orange','color_palette_orange_pressed'
			]
play_pause_dict={}
for name in play_pause:
	pat='Picard/mobile_style_icons/'+name+'.png'
	play_pause_dict[name]=pygame.transform.scale(pygame.image.load(os.path.join(LCARS_PATH,pat)), (70, 70))

start_y=230
x_pos=610
PLAY_BUTTON=ButtonClass(0,play_pause_dict['play_blue'],play_pause_dict['play_blue_pressed'],x_pos,start_y,name='play',selected_img=play_pause_dict['play_orange'],selected_alt_img=play_pause_dict['play_orange_pressed'])
PAUSE_BUTTON=ButtonClass(0,play_pause_dict['pause_blue'],play_pause_dict['pause_blue_pressed'],x_pos,start_y+100,name='pause',selected_img=play_pause_dict['pause_orange'],selected_alt_img=play_pause_dict['pause_orange_pressed'])
SCALE_BUTTON=ButtonClass(0,play_pause_dict['scale_blue'],play_pause_dict['scale_blue_pressed'],x_pos,start_y+200,name='scale',selected_img=play_pause_dict['scale_orange'],selected_alt_img=play_pause_dict['scale_orange_pressed'])
RESET_BUTTON=ButtonClass(0,play_pause_dict['reset'],play_pause_dict['reset_pressed'],x_pos,start_y+210,name='reset',selected_img=play_pause_dict['reset'],selected_alt_img=play_pause_dict['reset_pressed'])
RESET5_BUTTON=ButtonClass(0,play_pause_dict['reset5'],play_pause_dict['reset5_pressed'],x_pos,start_y+100,name='reset5',selected_img=play_pause_dict['reset5'],selected_alt_img=play_pause_dict['reset5_pressed'])
COLOR_PALETTE_BUTTON=ButtonClass(0,play_pause_dict['color_palette_blue'],play_pause_dict['color_palette_blue_pressed'],x_pos,start_y+300,name='color_palette',selected_img=play_pause_dict['color_palette_orange'],selected_alt_img=play_pause_dict['color_palette_orange_pressed'])

# ------------------------------------ mini buttons ------------------------------------------------------ #
mini_buttons_path=LCARS_PATH+'/Picard/mini_buttons/'

new_res=(80,80)
MINI_BUTTON_NAMES=['bar_chart','pie_chart','line_plot','info']#,'numpad']
MINI_BUTTONS=[]
button_w=97
col=170
row=585
x_spacing=button_w+29
for b_name in MINI_BUTTON_NAMES:
	x=mini_buttons_path+b_name

	# print (x+'_blue.png')
	button_img=         pygame.transform.scale(pygame.image.load(x+'_blue.png'), new_res)
	# print (x+'_blue_pressed.png')
	button_alt_img=     pygame.transform.scale(pygame.image.load(x+'_blue_pressed.png'), new_res)
	# print (x+'_orange.png')
	button_selected_img=pygame.transform.scale(pygame.image.load(x+'_orange.png'), new_res)
	# print (x+'_orange_pressed.png')
	selected_alt_img=   pygame.transform.scale(pygame.image.load(x+'_orange_pressed.png'), new_res)
	MINI_BUTTONS.append(ButtonClass(0,button_img,button_alt_img,col,row,name=b_name,selected_img=button_selected_img,selected_alt_img=selected_alt_img))
	col+=x_spacing

# -------------------------------- Icon Buttons ---------------------------------------------------------- #
icon_button_names=['home','noise','pm25',
'pressure','spectrometer','temp_humid',
'uv','vis_ir','wind',
'thermal_cam','object','imu_2',
'SDR','voc','gps',
'radiation','lidar','weigh_scale',
'multimeter','battery','drive',
'fly','walk','device_stats_2',
'settings','files','developer',
'sleep','plot_button','new_page_button',
'exit_button']

ICON_BUTTON_H=148
ICON_BUTTON_W=135
COLUMN_SPACING=ICON_BUTTON_W+30
row_spacing=ICON_BUTTON_H+25

COL1_POS=185
ROW1_POS=85
column_positions=[COL1_POS,COL1_POS+COLUMN_SPACING,COL1_POS+2*COLUMN_SPACING]
row_positions=[ROW1_POS,ROW1_POS+row_spacing,ROW1_POS+2*row_spacing]

# Calculate pages, rows, and cols
icons_per_page=9
NUM_PAGES=math.ceil(len(icon_button_names)/icons_per_page)
num_cols=len(column_positions)
num_rows=len(row_positions)
PAGE_OFFSET=720

pos_list=[]
for page_num in range(NUM_PAGES):
	for curr_row in range(num_rows):
		for curr_col in range(num_cols):
			y=row_positions[curr_row]
			x=column_positions[curr_col]+page_num*PAGE_OFFSET
			pos_list.append((x,y))

i=0
ICON_BUTTONS=[]
for b_name in icon_button_names:
	button_img=pygame.image.load(os.path.join(ICONS_PATH,b_name+'.png'))
	button_alt_img=pygame.image.load(os.path.join(ICONS_PATH,b_name+'_pressed.png'))

	# print(button_img)
	# print(button_alt_img)

	ICON_BUTTONS.append(ButtonClass(i,button_img,button_alt_img,pos_list[i][0],pos_list[i][1],name=b_name))
	i+=1

 # =====================================================================================================

# Blank buttons for home-buttons and top-left button
button_selected_3=pygame.image.load(os.path.join(LCARS_PATH,'Picard/button_selected_3.png'))
button_selected_3_blank=pygame.image.load(os.path.join(LCARS_PATH,'Picard/button_selected_3_blank.png'))

top_button_selected=pygame.image.load(os.path.join(LCARS_PATH,'Picard/top_button_selected.png'))

button=pygame.image.load(os.path.join(LCARS_PATH,'Picard/button.png'))
button_alt=pygame.image.load(os.path.join(LCARS_PATH,'Picard/button_alt.png'))
button_selected=pygame.image.load(os.path.join(LCARS_PATH,'Picard/button_selected.png'))

# =======================================================================================================
# Quick menu buttons
quick_menu_button_names=['fullscreen','backlight','sleep','device_stats','home','screenshot','exit','blank']
prefix='/quick_menu_8_buttons/'

start_x,start_y=(175,78)
x_spacing=205+57
y_spacing=113+39

positions=[]
QUICK_MENU_BUTTONS=[]
for i in range(8):
	positions.append((start_x,start_y+i*y_spacing))
	positions.append((start_x+x_spacing,start_y+i*y_spacing))

i=0
for b_name in quick_menu_button_names:
	x=LCARS_PATH+prefix+b_name
	button=pygame.image.load(x+'.png')
	button_alt=pygame.image.load(x+'_pressed.png')

	button=pygame.transform.scale(button, (205, 113))
	button_alt=pygame.transform.scale(button_alt, (205, 113))

	QUICK_MENU_BUTTONS.append(ButtonClass(i,button,button_alt,positions[i][0],positions[i][1],name=b_name))
	i+=1

# =======================================================================================================
# Navigation buttons
positions=[(200,600),(500,597)]
nav_button_names=['left_arrow','right_arrow']


NAV_BUTTONS=[]
i=0
for b_name in nav_button_names:
	button_img=pygame.image.load(os.path.join(LCARS_PATH,b_name+'.png'))
	button_alt_img=pygame.image.load(os.path.join(LCARS_PATH,b_name+'_pressed.png'))

	NAV_BUTTONS.append(ButtonClass(i,button_img,button_alt_img,positions[i][0],positions[i][1],name=b_name))
	i+=1

# ---
x_pos=610
y_pos=95
small_butt_h=72
big_butt_h=168
vspace=20

y=[y_pos,
y_pos+small_butt_h+vspace,
y_pos+small_butt_h+vspace+big_butt_h+vspace,
y_pos+small_butt_h+vspace+big_butt_h+vspace+big_butt_h+vspace]

nav_button_vertical_names=['page_up','up','down','page_down']
NAV_BUTTONS_VERTICAL=[]
i=0
for b_name in nav_button_vertical_names:
	a=os.path.join(ICONS_PATH,b_name+'_blue.png')
	# print (a)
	button_img=pygame.image.load(a)
	b=os.path.join(ICONS_PATH,b_name+'.png')
	# print (b)
	button_alt_img=pygame.image.load(b)
	NAV_BUTTONS_VERTICAL.append(ButtonClass(i,button_img,button_alt_img,x_pos,y[i],name=b_name))
	i+=1