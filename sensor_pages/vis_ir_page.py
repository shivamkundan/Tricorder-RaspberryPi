'''! @brief For visualizing data from TSL2591 vis/ir sensor.
     @file vis_ir_page.py Contains definition for LightSensorPage class.
     @warning Requires mosfet on/off control.
'''
import pygame.event as e
from buttons import ButtonClass, quarter_button, quarter_button_alt
from aa_arc_gauge import AA_Gauge
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE, FONT_DIN
from colors import DARK_GREY, ORANGE, SLATE, DARK_YELLOW, WHITE, RED
from page_templates import PageTemplate
# from custom_user_events import SET_LIGHT_SENSOR_GAIN, POWER_TSL_ON,POWER_TSL_OFF
from serial_manager import get_vis_ir,set_tsl_scl_connect,set_tsl_scl_disconnect, set_tsl_gain,ser
from paths_and_utils import PERIPHERAL_MODE
import logging

class LightSensorPage(PageTemplate):
    '''! @brief For visualizing data from TSL2591 vis/ir sensor.
    @warning Requires mosfet on/off control.
    '''
    def __init__(self,name):
        '''! Constructor'''
        super().__init__(name)
        ## Next page
        self.next_screen_name=self.name
        ## Return page
        self.prev_page_name='menu_home_page'
        ## List of buttons for gain selection
        self.gain_buttons=self.init_buttons()
        ## List of sll buttons for this page
        self.button_list+=self.gain_buttons
        ## Hold number of frames displayed
        self.frame_count=0

        ## Current luminous flux reading
        self.lux=-1
        ## Current raw IR reading
        self.ir=-1
        ## Current sensor gain
        self.gain=-1
        ## Current raw VIS reading
        self.visible=-1
        ## Current raw VIS+IR reading
        self.full_spectrum=-1
        ## Tracks MCU connection
        self.bluetooth_connected=False
        ## Number of frames between updates.
        self.num_tics=10
        ## Holds integer <-> text mappings for gain settings
        self.gain_dict={-1:'XX','-1':'XX','0':'LOW (1x)','16':'MED (25x)','32':'HIGH (428x)','48': 'MAX (9876x)'}
        ## Holds integer <-> send_code mappings for gain settings
        self.gain_codes_dict={'1x':'LA','25x':'LB','428x':'LC','9876x':'LD'}

        self.init_gauges()

    def on_enter(self):
        '''! Turns on tsl_scl mosfet.'''
        set_tsl_scl_connect()
        self.frame_count=0
        logging.info(f"entering {self.__class__.__name__}")

    def on_exit(self):
        '''! Turns off tsl_scl mosfet.'''
        set_tsl_scl_disconnect()

    def init_gauges(self):
        '''! Init gauges for this page.'''
        # --- set all counters  --- #
        gauges_start_col=145
        gauge_radius=100
        gauges_spacing=48
        weight=8
        arc_h=gauge_radius+weight//2
        font=FONT_HELVETICA_NEUE
        f_color=WHITE
        main_font_size=54
        curr_col=250-gauge_radius
        # ----
        arc_h+=gauge_radius*2+
        ## Origin for VIS gauge
        self.vis_gauge_origin=(curr_col,160)
        ## VIS gauge object
        self.vis_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=1000,origin=self.vis_gauge_origin, radius=gauge_radius,weight=weight,color=RED,suffix='lux',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='VIS',title_font_size=20)

        ## Origin for IR gauge
        self.ir_gauge_origin=(curr_col+(2.5*gauge_radius)+gauges_spacing,160)
        ## IR gauge object
        self.ir_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=1000,origin=self.ir_gauge_origin, radius=gauge_radius,weight=weight,color=RED,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='IR',title_font_size=20)

    def blit_current_settings(self,screen):
        '''! Display current settings for this page/sensor.'''
        vis_raw=f'{int(self.visible):,}'
        r=float(self.full_spectrum)-float(self.visible)
        ir_raw=f'{r:,}'

        x_pos,y_pos=165,400
        FONT_DIN.render_to(screen, (x_pos, y_pos),'VIS Raw: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),vis_raw, SLATE, size=34)
        x_pos=455
        FONT_DIN.render_to(screen, (x_pos, y_pos),'IR Raw: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),ir_raw, SLATE, size=34)
        x_pos,y_pos=165,475
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Gain: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),self.gain_dict[str(self.gain)], SLATE, size=34)

    def flip_gain_buttons(self):
        '''! Flip button selections.'''
        for button in self.gain_buttons:
            button.selected=False

        if self.gain=='0':
            self.gain_buttons[0].selected=True
        elif self.gain=='16':
            self.gain_buttons[1].selected=True
        elif self.gain=='32':
            self.gain_buttons[2].selected=True
        elif self.gain=='48':
            self.gain_buttons[3].selected=True

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)

        self.flip_gain_buttons()

        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        if pressed_button!=None:
            if pressed_button.name in self.gain_codes_dict.keys():
                new_gain=self.gain_codes_dict[pressed_button.name]
                set_tsl_gain(new_gain)
        x_pos=170
        y_pos=375
        FONT_FEDERATION.render_to(screen, (150, 67), 'Light Sensor', ORANGE,style=0,size=44)
        FONT_FEDERATION.render_to(screen, (150, 117), 'TSL2591', DARK_YELLOW,style=0,size=34)

        if self.bluetooth_connected==True or PERIPHERAL_MODE=='serial':

            if self.frame_count%self.num_tics==0:
                self.lux,self.ir,self.gain,self.visible,self.full_spectrum = get_vis_ir()

            self.blit_current_settings(screen)

            # ----- adjust units ----- #
            if 0<self.lux<1:
                adjusted_lux=str(round(self.lux*1000,2))
                self.vis_gauge.suffix=' μLux'
            else:
                adjusted_lux=f'{round(self.lux,2):,}'
                self.vis_gauge.suffix=' Lux'

            # ----- blit gauges----- #
            ## Pygame surf for VIS gauge
            self.vis_gauge_img=self.vis_gauge.blit_gauge(str(self.lux),print_val=adjusted_lux)
            ## Pygame surf for IR gauge
            self.ir_gauge_img=self.ir_gauge.blit_gauge(str(self.ir),print_val=f'{self.ir:,}')
            self.vis_gauge_img.set_colorkey((0,0,0))
            self.ir_gauge_img.set_colorkey((0,0,0))
            screen.blit(self.vis_gauge_img,self.vis_gauge_origin)
            screen.blit(self.ir_gauge_img,self.ir_gauge_origin)

        else:
            y_pos+=110
            FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'NO BLUETOOTH', WHITE, size=28)

        self.frame_count+=1
        return self.next_screen_name,self.kwargs

    def init_buttons(self):
        '''! Init buttons for this page.'''
        butt_list=[]
        width=120   # quarter button
        height=82

        gain_levels=['1x','25x','428x','9876x']
        f_size=26

        x_spacing=width+20
        row=580
        col=135

        i=0
        for name in gain_levels:
            b=ButtonClass(i,quarter_button,quarter_button_alt,col,row,text=name,font_color=ORANGE,style=1,font_size=f_size,name=name)
            print (b.selected)
            butt_list.append(b)
            col+=x_spacing
            i+=1

        return butt_list
