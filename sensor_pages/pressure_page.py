'''Display barometric pressure, temperature, and est altitude readings'''
import pygame.event as e
from buttons import ButtonClass, slide_switch_blank,simple_button_short,simple_button_short_alt
from aa_arc_gauge import AA_Gauge
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE, FONT_DIN
from colors import SLATE, ORANGE, WHITE, DARK_GREY, DARK_YELLOW, YELLOW
from page_templates import PageTemplate
from custom_user_events import SET_PRESSURE
from paths_and_utils import PERIPHERAL_MODE
from serial_manager import get_pressure

class PressureSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'
        self.bluetooth_connected=False

        # Button stuff
        self.menu_title_buttons,self.menu_buttons, settings_button=self.init_buttons()
        self.button_list+=self.menu_title_buttons+self.menu_buttons+[settings_button]
        self.basic_buttons.append(settings_button)
        self.button_dict=self.make_dictionary()
        self.button_dict['pressure'].selected=True

        self.frame_count=0
        self.num_tics=5

        self.pressure=-1
        self.bmp_temp=-1
        self.p_oversampling='-1'
        self.t_oversampling='-1'
        self.altitude='-1'
        self.send_code=''
        self.show_menu=False
        self.init_gauges()

    def init_buttons(self):
        menu_title_buttons=[]
        menu_buttons=[]

        button_w=165 #short button
        x_spacing=button_w+20
        button_h=83
        row,col=(400,137)
        f_size=26

        #  Instantiate selection buttons
        menu_title_buttons.append(ButtonClass(3,slide_switch_blank,slide_switch_blank,col,row,text='Pressure',font_size=30,style=0,font_color=DARK_GREY,selected_color=ORANGE,name='pressure',selected_img=slide_switch_blank))
        menu_title_buttons.append(ButtonClass(4,slide_switch_blank,slide_switch_blank,col+255,row,text='Temperature',font_size=f_size,style=0,font_color=DARK_GREY,selected_color=ORANGE,name='temperature',selected_img=slide_switch_blank))

        # Instantiate other buttons
        col,row=(150,490)
        i=0
        for name in ['1','2','4','8','16','32']:
            menu_buttons.append(ButtonClass(i+1,simple_button_short,simple_button_short_alt,col,row,text=name,font_size=f_size,style=1,font_color=ORANGE,name=name))
            col+=x_spacing
            i+=1
            if (i%3==0):
                row+=button_h+15
                col=150
        col+=2*x_spacing
        settings_button=ButtonClass(11,simple_button_short,simple_button_short_alt,col,100,text='Settings',font_size=f_size,style=0,font_color=ORANGE,name='settings')

        return menu_title_buttons, menu_buttons, settings_button

    def init_gauges(self):
        gauge_radius=100
        gauges_spacing=48
        weight=8
        arc_h=210
        font=FONT_HELVETICA_NEUE
        f_color=WHITE
        main_font_size=60
        curr_col=250-gauge_radius
        self.pressure_gauge_origin=(curr_col,arc_h)
        self.pressure_gauge=AA_Gauge(None,(0),in_min=930,in_max=1030,origin=self.pressure_gauge_origin, radius=gauge_radius,weight=weight,color=YELLOW,suffix='hPa',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='PRESSURE',title_font_size=18,main_font_size=54,auto_lims=False)

        self.bmp_temp_gauge_origin=(curr_col+(2.5*gauge_radius)+gauges_spacing,arc_h)
        self.bmp_temp_gauge=AA_Gauge(None,(0),in_min=10,in_max=40,origin=self.bmp_temp_gauge_origin, radius=gauge_radius,weight=weight,color=YELLOW,suffix='°C',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='TEMP',title_font_size=20,main_font_size=main_font_size,auto_lims=False)

    def blit_title(self,screen):
        # Title
        FONT_FEDERATION.render_to(screen, (150, 67), 'Barometric', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 67+40+10), 'Pressure', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117+40+10), 'BMP388', DARK_YELLOW,style=0,size=34)

    def blit_menu(self,screen):
        self.button_dict['settings'].text='Back'
        self.blit_all_buttons(screen)

        a=self.button_dict['pressure'].selected, self.button_dict['temperature'].selected
        b=self.p_oversampling, self.t_oversampling

        for x,y in zip(a,b):
            if x:
                for button in self.menu_buttons:
                    if button.text==y:
                        button.selected=True
                    else:
                        button.selected=False

    def blit_current_settings(self,screen):
        x_pos=138
        y_pos=440
        FONT_FEDERATION.render_to(screen, (256, y_pos),'OVERSAMPLING ', ORANGE, size=28,style=1)
        y_pos+=60
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Pressure: ', ORANGE, size=28)
        y_pos+=35
        FONT_DIN.render_to(screen, (x_pos+20, y_pos),str(self.p_oversampling), SLATE, size=34)
        y_pos=440+60
        x_pos=440
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Temperature: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),str(self.t_oversampling), SLATE, size=34)

        y_pos=440+60+60
        x_pos=138
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Altitude: ', ORANGE, size=28)
        FONT_DIN.render_to(screen, (x_pos+20, y_pos+35),str(self.altitude), SLATE, size=34)

    def flip_selection(self,pressed_button):
        if pressed_button.name=='pressure':
            self.button_dict['pressure'].selected=True
            self.button_dict['temperature'].selected=False
            self.button_dict['pressure'].font_size=30
            self.button_dict['temperature'].font_size=24

        if pressed_button.name=='temperature':
            self.button_dict['pressure'].selected=False
            self.button_dict['temperature'].selected=True
            self.button_dict['pressure'].font_size=24
            self.button_dict['temperature'].font_size=30

    def next_frame(self,screen,curr_events,**kwargs):

        self.next_screen_name=self.name

        self.kwarg_handler(kwargs)

        # Blit everything
        self.blit_title(screen)
        if self.show_menu:
            self.blit_menu(screen)
        else:
            self.button_dict['settings'].text='Settings'
            self.blit_basic_buttons(screen)
            self.blit_current_settings(screen)

        # User interaction
        pressed_button=self.handle_events(screen,curr_events)
        if pressed_button!=None:
            if pressed_button.name=='home_button':
                self.show_menu=False

            if pressed_button.name=='settings':
                self.show_menu=not self.show_menu

            self.flip_selection(pressed_button)

            if self.button_dict['pressure'].selected==True:
                if pressed_button in self.menu_buttons:
                    self.send_code=('P_P_'+str(pressed_button.text))#.encode('utf-8')
                    print (self.send_code)
                    e.post(SET_PRESSURE)

            if self.button_dict['temperature'].selected==True:
                if pressed_button in self.menu_buttons:
                    self.send_code=('P_T_'+str(pressed_button.text))#.encode('utf-8')
                    print (self.send_code)
                    e.post(SET_PRESSURE)

        if self.frame_count%self.num_tics==0:
            self.altitude,self.pressure,self.bmp_temp,self.p_oversampling,self.t_oversampling=get_pressure()

        if self.bluetooth_connected or PERIPHERAL_MODE=='serial':
            self.pressure_gauge_img=self.pressure_gauge.blit_gauge(self.pressure)
            self.bmp_temp_gauge_img=self.bmp_temp_gauge.blit_gauge(self.bmp_temp)
            self.pressure_gauge_img.set_colorkey((0,0,0))
            self.bmp_temp_gauge_img.set_colorkey((0,0,0))
            screen.blit(self.pressure_gauge_img,self.pressure_gauge_origin)
            screen.blit(self.bmp_temp_gauge_img,self.bmp_temp_gauge_origin)
        else:
            x_pos=138
            y_pos=525
            FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'NO BLUETOOTH', WHITE, size=28)

        self.frame_count+=1

        return self.next_screen_name,self.kwargs
