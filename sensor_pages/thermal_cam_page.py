import sys, os
sys.path.append(os.path.abspath("../"))

import select
from bluetooth import *
import numpy as np

from pygame.image import frombuffer
from pygame import KEYUP,K_RIGHT,K_LEFT
import pygame.event as e

# -------------- my libs -------------- #
from page_templates import PageTemplate
from custom_user_events import BLUETOOTH_DISCONNECTED
from paths_and_utils import MAX_BYTES, PERIPHERAL_MODE
from images import lcars_bg
from fonts import FONT_DIN, FONT_FEDERATION
from buttons import PREF_BUTTON,PLAY_BUTTON,PAUSE_BUTTON,SCALE_BUTTON,COLOR_PALETTE_BUTTON,NAV_BUTTONS
from colors import WHITE, ORANGE, DARK_YELLOW
from plotting_functions import plot2img
from global_functions import flip_buttons
from mappings import d

# ----- plotting libs ----- #
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# -------------- Plotting stuff -------------- #
COLOR = (0.75,0.75,0.75)
mpl.rcParams['font.size'] = 14
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

import serial
import signal

from serial_manager import ser

import picamera
import io

# Init camera
camera = picamera.PiCamera()
camera.resolution = (464, 464)
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.rotation = 90

x=120
y=50

# Init buffer
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)


class ThermalCamPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.button_list+=[PREF_BUTTON,PLAY_BUTTON,PAUSE_BUTTON,SCALE_BUTTON,COLOR_PALETTE_BUTTON]+NAV_BUTTONS
        self.button_dict=self.make_dictionary()
        self.b_names=['play','pause']

        start_y=230-45
        x_pos=610
        y_space=85

        for btn_name in ['play','pause','scale','color_palette']:
            y=start_y
            self.button_dict[btn_name].update_y_pos(y)
            start_y+=y_space

        self.init_plotting_stuff()
        self.client_sock=None
        self.prev_page_name='menu_home_page'

        self.absolute_scale=False
        self.f_num=0
        self.frame = [0] * 768
        self.mode='relative'
        self.pause=False

    def init_plotting_stuff(self):
        # self.fig = plt.figure(figsize=[5,4])
        self.fig = plt.figure(figsize=[7.5,6])
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)

        num_colors=1000
        top = cm.get_cmap('jet', num_colors)
        # bottom = cm.get_cmap('Reds', num_colors)
        newcolors = np.vstack((top(np.linspace(0, 1, num_colors))))#,
        # bottom(np.linspace(0, 1, num_colors))))
        self.newcmp = ListedColormap(newcolors, name='OrangeBlue')
        MAX_TEMP=300 # max celsius value that thermal cam can detect
        self.c_num=0
        self.default_cmaps=['jet','autumn','bone','cool','copper','gray','hot','hsv','inferno','magma','pink','plasma','spring','summer','viridis','winter',]
        # print ('len(self.default_cmaps):',len(self.default_cmaps))
        self.curr_cmap='jet'

        plt.axis('off')

    def blit_title(self,screen):
        FONT_FEDERATION.render_to(screen, (150, 67), 'Thermal Cam', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), 'MLX90640', DARK_YELLOW,style=0,size=34)

    def thermal_plotter(self,frame):
        '''Works in a different way than all other sensor-MCU communication'''
        self.fig.canvas.flush_events()

        plt.tick_params(left=False)
        plt.gca().tick_params(axis=u'both', which=u'both',length=0)

        if self.absolute_scale:
            psm= self.ax.pcolormesh(np.fliplr(np.rot90(frame)), cmap=self.curr_cmap, rasterized=True,vmin=-10, vmax=300)
        else:
            psm= self.ax.pcolormesh(np.fliplr(np.rot90(frame)), cmap=self.curr_cmap, rasterized=True,vmin=np.min(frame), vmax=np.max(frame),alpha=0.4)

        cb=self.fig.colorbar(psm, ax=self.ax,alpha=None)#,orientation = 'horizontal')

        cb.ax.tick_params(axis=u'both', which=u'both',length=0)

        surf= (plot2img(self.fig,self.ax,self.canvas))

        # surf = plot2img(self.fig,self.ax,self.canvas)
        # # this works on images with per pixel alpha too
        # alpha = 128
        # surf.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        cb.remove()
        return surf

    # def recv_frame_data(self,client_sock):
    #     expected=''.join('#' for _ in range(MAX_BYTES))



    #     # print ('pos1')
    #     PRE_MSG='7'+''.join('*' for m in range (1015))
    #     self.client_sock.send(PRE_MSG)
    #     # print ('pos2')
    #     recv_data=''
    #     m=1
    #     try:
    #         while recv_data!=expected:
    #             # print ('msg#:',m)
    #             # print(recv_data)
    #             try:
    #                 ready = select.select([self.client_sock], [], [], 3)
    #                 if ready[0]:
    #                     recv_data = self.client_sock.recv(MAX_BYTES).decode("utf-8")
    #                 # recv_data = self.client_sock.recv(MAX_BYTES).decode("utf-8")
    #                 self.client_sock.makefile().flush()
    #                 # print ((recv_data))
    #                 # if recv_data==expected:
    #                     # print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #             except btcommon.BluetoothError:
    #                 self.bluetooth_connected=False
    #                 pygame.event.post(BLUETOOTH_DISCONNECTED)
    #             m+=1
    #             if (m>25):
    #                 break
    #     except KeyboardInterrupt:
    #         print('interrupt')
    #     except btcommon.BluetoothError:
    #         self.bluetooth_connected=False
    #         pygame.event.post(BLUETOOTH_DISCONNECTED)
    #     # print ('pos3')

    #     MIN_MSG_LEN=4
    #     START_MSG='STRT'+''.join('*' for i in range (1012))
    #     ACK_MSG1='CONF'+''.join('*' for i in range (1012))
    #     ACK_MSG2='RECV'+''.join('*' for i in range (1012))
    #     END_MSG='DONE'+''.join('*' for i in range (1012))

    #     # start
    #     client_sock.send(START_MSG)

    #     # print ('pos4')
    #     xxx=np.ndarray(shape=(32,24))
    #     frame = [0] * 768



    #     # receive number of pieces

    #     try:
    #         ready = select.select([self.client_sock], [], [], 3)
    #         if ready[0]:

    #             recv_num_msgs = client_sock.recv(MAX_BYTES).decode("utf-8")
    #             # print ('recv_num_msgs: ',recv_num_msgs)
    #             recv_num_msgs = int(recv_num_msgs.replace('*','').replace('\x00','').replace(' ','').rstrip(' '))
    #         # recv_num_msgs = client_sock.recv(MAX_BYTES).decode("utf-8")
    #         # recv_num_msgs= int(recv_num_msgs.replace('*','').replace('\x00','').replace(' ','').rstrip(' '))
    #         # print('number of pieces: ',recv_num_msgs)
    #             client_sock.send(ACK_MSG1)
    #             recv_str=''
    #     except btcommon.BluetoothError:
    #             self.bluetooth_connected=False
    #             pygame.event.post(BLUETOOTH_DISCONNECTED)
    #             return frame
    #     # print ('pos5')
    #     # receive all pieces of data
    #     for i in range (int(recv_num_msgs)):
    #     # for i in range (4):
    #         ready = select.select([self.client_sock], [], [], 3)
    #         if ready[0]:
    #             recv_msg = client_sock.recv(MAX_BYTES).decode("utf-8").replace('*','').replace('\x00','').rstrip(' ')
    #             # print ('len(recv_msg):',len(recv_msg))
    #             recv_str+=recv_msg
    #             client_sock.send(ACK_MSG2)
    #     # print ('pos6')
    #     client_sock.send(END_MSG)
    #     # print (recv_str)
    #     # print ('pos7')
    #     # combine recv data
    #     recv_str=recv_str.replace('*','').replace('\x00','').rstrip(' ')
    #     num_list=recv_str.split(' ')
    #     for rr in range(len(num_list)):
    #         frame[rr]=float(num_list[rr])

    #     # restructure recv vals
    #     for h in range(24):
    #         for w in range(32):
    #             t = frame[h * 32 + w]
    #             xxx[w][h]=t

    #     return xxx

    def recv_frame_data_usb_serial(self):
        temp_str=""
        xxx=np.ndarray(shape=(32,24))
        frame = [0] * 768
        ser.write(d['THERMAL_CAM_CODE'].encode('utf-8'))
        curr_char="p"
        while (curr_char!='F'):
            curr_char=(ser.read()).decode('utf-8')
            temp_str+=curr_char

        try:
            temp_str=temp_str.replace('F',"")
            temp_str=temp_str.split('S')[1]

            # remove start and end markers
            frame=temp_str.split(" ")[1:-1]

            i=0
            for row in range(24):
                for col in range(32):
                    xxx[col][row]=frame[i]
                    i+=1

        except Exception as e:
            print("Exception\n:",e)
        return xxx

    def increment_color_map(self):
        if self.bluetooth_connected==True or PERIPHERAL_MODE=='serial':
            self.c_num+=1
            self.curr_cmap=self.default_cmaps[self.c_num%len(self.default_cmaps)]

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)

        try:
            self.blit_all_buttons(screen)
            for event in curr_events:
                 if event.type == KEYUP:
                    if event.key==K_RIGHT:
                        self.increment_color_map()
                        # self.c_num+=1
                        # self.curr_cmap=self.default_cmaps[self.c_num%len(self.default_cmaps)]
                        curr_events.remove(event)
                    elif event.key==K_LEFT:
                        self.c_num-=1
                        self.curr_cmap=self.default_cmaps[self.c_num%len(self.default_cmaps)]
                        curr_events.remove(event)

            pressed_button=self.handle_events(screen,curr_events)

            if self.bluetooth_connected==True or PERIPHERAL_MODE=='serial':

                if pressed_button!=None:
                    print (f'pressed {pressed_button.name}')

                    if pressed_button.name=='color_palette':
                        self.increment_color_map()

                    if pressed_button.name=='scale':
                        self.absolute_scale=not self.absolute_scale
                        if self.absolute_scale:
                            # pressed_button.text='SCALE: ABS'
                            self.mode='absolute'
                        else:
                            # pressed_button.text='SCALE: REL'
                            self.mode='relative'


                    if pressed_button.name in self.b_names:
                        flip_buttons(pressed_button,[ self.button_dict['play'], self.button_dict['pause']])

                        if self.button_dict['pause'].selected:
                            self.pause=True
                        else:
                            self.pause=False

                if not self.pause:

                    stream = io.BytesIO()
                    camera.capture(stream, use_video_port=True, format='rgb')
                    stream.seek(0)
                    stream.readinto(rgb)
                    stream.close()
                    img = frombuffer(rgb[0:
                          (camera.resolution[0] * camera.resolution[1] * 3)],
                           camera.resolution, 'RGB')

                    if img:
                        # img.set_alpha(175)
                        screen.blit(img, (x,y))

                    if self.f_num%7==0:
                        # self.frame=self.recv_frame_data(self.client_sock)
                        self.frame=self.recv_frame_data_usb_serial()
                        self.surf=self.thermal_plotter(self.frame)
                        self.surf.set_alpha(100)
                screen.blit(self.surf,(25,-20))

                val_list=[np.max(self.frame),round(np.mean(self.frame),2),np.min(self.frame)]

                start_x=165
                start_y=540
                x_space=165
                y_space=40
                f_size=24
                FONT_DIN.render_to(screen, (start_x, start_y),'max:', ORANGE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x, start_y+y_space),'avg:', ORANGE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x, start_y+2*y_space),'min:', ORANGE, size=f_size,bgcolor=None,style=1)

                start_x+=80
                FONT_DIN.render_to(screen, (start_x, start_y),f"{val_list[0]}°C", WHITE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x, start_y+y_space),f"{val_list[1]}°C", WHITE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x, start_y+2*y_space),f"{val_list[2]}°C", WHITE, size=f_size,bgcolor=None,style=1)

                start_x+=160
                y_space=30
                FONT_DIN.render_to(screen, (start_x, start_y),'Color map: ', ORANGE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x+20, start_y+y_space),self.curr_cmap, WHITE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x, start_y+2*y_space),'Scale:', ORANGE, size=f_size,bgcolor=None,style=1)
                FONT_DIN.render_to(screen, (start_x+20, start_y+3*y_space),self.mode, WHITE, size=f_size,bgcolor=None,style=1)
                # FONT_DIN.render_to(screen, (start_x, start_y+2*y_space),'min:', ORANGE, size=f_size,bgcolor=BLACK,style=1)

                screen.blit(lcars_bg,(0,0))
                # txt_surf,w,h=get_text_dimensions(text='Color map: ',font_style=FONT_DIN,font_color=ORANGE,style=0,font_size=f_size)
                # screen.blit(txt_surf,(start_x,start_y))
                # # --- Column #1 shows settings --- #
                # x_pos=155
                # y_pos=410+160
                # for val,name in zip(val_list,name_list):
                #     FONT_DIN.render_to(screen, (x_pos, y_pos),str(name), ORANGE, size=28,bgcolor=BLACK,style=1)
                #     txt_surf,w,h=get_text_dimensions(text=str(val),font_style=FONT_DIN,font_color=WHITE,style=0,font_size=28)
                #     screen.blit(txt_surf,(410-w-25,y_pos+40))
                #     y_pos+=80
        except btcommon.BluetoothError:
            self.bluetooth_connected=False
            e.post(BLUETOOTH_DISCONNECTED)
        except ValueError:
            print ('thermal cam value error')

        # self.blit_title(screen)

        self.f_num+=1
        return self.next_screen_name,self.kwargs