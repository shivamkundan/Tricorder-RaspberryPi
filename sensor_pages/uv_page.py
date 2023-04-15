import pygame.event as e
from images import ButtonClass
from aa_arc_gauge import *
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE, FONT_DIN
from colors import PURPLE,DARK_GREY,BLACK,WHITE,ORANGE,DARK_YELLOW
from page_templates import PageTemplate
from custom_user_events import SET_UV_GAIN
from serial_manager import get_uv

class UVSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='MenuHomePage'
        self.gain_codes_dict={'1x':'U_G_0','3x':'U_G_1','6x':'U_G_2','9x':'U_G_3','18x':'U_G_4'}
        self.gain_name_dict={-1:'xx','-1':'xx','0':'1x','1':'3x','2':'6x','3':'9x','4':'18x'}

        self.resolution_codes_dict={'13 bits':'U_R_5','16 bits':'U_R_4','17 bits':'U_R_3','18 bits':'U_R_2','19 bits':'U_R_1','20 bits':'U_R_0'}
        self.resolution_name_dict={-1:'XX','-1':'XX','0':'20 bits','1':'19 bits','2':'18 bits','3':'17 bits','4':'16 bits','5':'13 bits'}

        self.delay_codes_dict={'25ms':'U_D_0','50ms':'U_D_1','100ms':'U_D_2','200ms':'U_D_3','500ms':'U_D_4','1s':'U_D_5','2s':'U_D_6'}
        self.delay_name_dict={'-1':'XX',-1:'XX','0':'25ms','1':'50ms','2':'100ms','3':'200ms','4':'500ms','5':'1.0s','6':'2.0s'}

        self.settings_dicts=[self.gain_codes_dict,self.resolution_codes_dict,self.delay_codes_dict]

        self.uvs=-1
        self.light=-1
        self.uvi=-1
        self.ltr_lux=-1
        self.ltr_gain=-1
        self.ltr_resolution=-1
        self.ltr_window_factor=-1
        self.ltr_measurement_delay=-1
        self.send_code=''

        self.init_gauges()

        # Button stuff
        self.show_menu=False
        self.menu_title_buttons,self.menu_buttons,self.settings_button=self.init_buttons()
        self.button_list+=self.menu_title_buttons+self.menu_buttons+[self.settings_button]
        self.button_dict=self.make_dictionary()
        self.button_dict['gain'].selected=True

    def init_buttons(self):

        button_w=165 #short button
        x_spacing=button_w+20
        col=150-button_w//4
        button_h=83
        y_spacing=button_h+15
        f_size=26

        row=340
        menu_title_buttons=[]
        menu_title_buttons.append(ButtonClass(3,slide_switch_blank,slide_switch_blank,col,row,text='Gain',font_size=f_size,style=0,font_color=DARK_GREY,name='gain',selected_img=slide_switch_blank,selected_color=ORANGE))
        menu_title_buttons.append(ButtonClass(4,slide_switch_blank,slide_switch_blank,col+button_w,row,text='Resolution',font_size=f_size,style=0,font_color=DARK_GREY,name='resolution',selected_img=slide_switch_blank,selected_color=ORANGE))
        menu_title_buttons.append(ButtonClass(4,slide_switch_blank,slide_switch_blank,col+2*button_w,row,text='Delay',font_size=f_size,style=0,font_color=DARK_GREY,name='delay',selected_img=slide_switch_blank,selected_color=ORANGE))

        # --- menu buttons --- #
        row=340
        menu_buttons=[]
        col=150
        row+=70

        for i in range(8):
            name=f'b{i+1}'
            menu_buttons.append(ButtonClass(i+1,simple_button_short,simple_button_short_alt,col,row,text=name,font_size=f_size,style=0,font_color=ORANGE,name=name))
            col+=x_spacing
            # i+=1
            if ((i+1)%3==0):
                row+=y_spacing
                col=150

        col,row=(552-(button_w//2)-10,595)
        settings_button=ButtonClass(7,simple_button_short,simple_button_short_alt,col,row,text='Settings',font_size=f_size,style=1,font_color=ORANGE,name='settings')

        return menu_title_buttons,menu_buttons, settings_button

    def init_gauges(self):
        self.gauge_radius=100
        gauges_spacing=48
        weight=8
        arc_h=165
        font=FONT_HELVETICA_NEUE
        f_color=WHITE
        main_font_size=60
        curr_col=250-self.gauge_radius
        # arc_h+=gauge_radius*2+gauges_spacing
        self.uv_gauge_origin=(curr_col,arc_h)
        self.uv_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=10,origin=self.uv_gauge_origin, radius=self.gauge_radius,weight=weight,color=PURPLE,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='UV Raw',title_font_size=20)

        self.uvi_gauge_origin=(curr_col+(2.5*self.gauge_radius)+gauges_spacing,arc_h)
        self.uvi_gauge=AA_Gauge(None,(0),main_font_size=main_font_size,in_min=0,in_max=10,origin=self.uvi_gauge_origin, radius=self.gauge_radius,weight=weight,color=PURPLE,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='UV Index',title_font_size=20)

    def blit_menu(self,screen):
        for button in self.menu_title_buttons:
            button.blit_button(screen)

        if self.button_dict['resolution'].selected:
            curr=self.resolution_codes_dict

        if self.button_dict['gain'].selected:
            curr=self.gain_codes_dict

        if self.button_dict['delay'].selected:
            curr=self.delay_codes_dict

        # j=[self.gain_name_dict[self.ltr_gain],self.resolution_name_dict[self.ltr_resolution],self.delay_name_dict[self.ltr_measurement_delay]]

        # i=0
        # for name in curr.keys():
        #     self.menu_buttons[i].text=name
        #     if name in j:
        #         self.menu_buttons[i].selected=True
        #     else:
        #         self.menu_buttons[i].selected=False
        #     self.menu_buttons[i].blit_button(screen)
        #     i+=1

    def blit_current_settings(self,screen):

        # Blit dividing line
        pygame.draw.line(screen, SLATE, (410, 395), (410, 645),1)

        # --- Column #2 shows raw light, lux --- #
        x_pos=450
        y_pos=410
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Light: ', ORANGE, size=28,style=1)
        l=f'{int(self.light):,}'
        txt_surf,w,h=get_text_dimensions(text=l,font_style=FONT_DIN,font_color=WHITE,style=0,font_size=34)
        screen.blit(txt_surf,(650-w-10,y_pos+40))

        y_pos+=80
        FONT_DIN.render_to(screen, (x_pos, y_pos),'Lux: ', ORANGE, size=28,style=1)
        lux=f'{round(float(self.ltr_lux),2):,}'
        txt_surf,w,h=get_text_dimensions(text=lux,font_style=FONT_DIN,font_color=WHITE,style=0,font_size=34)
        screen.blit(txt_surf,(650-w-10,y_pos+40))

        # # --- Column #1 shows settings --- #
        # x_pos=155
        # y_pos=410
        # for val,name in zip([self.gain_name_dict[self.ltr_gain],self.resolution_name_dict[self.ltr_resolution],self.delay_name_dict[self.ltr_measurement_delay]],['Gain:','Resolution:','Delay:']):
        #     FONT_DIN.render_to(screen, (x_pos, y_pos),str(name), ORANGE, size=28,bgcolor=BLACK,style=1)
        #     txt_surf,w,h=get_text_dimensions(text=str(val),font_style=FONT_DIN,font_color=WHITE,style=0,font_size=28)
        #     screen.blit(txt_surf,(410-w-25,y_pos+40))
        #     y_pos+=80

    def blit_title(self,screen):
        FONT_FEDERATION.render_to(screen, (150, 67), 'UV SENSOR', ORANGE,style=0,size=44)
        FONT_FEDERATION.render_to(screen, (150, 117), 'LTR390', DARK_YELLOW,style=0,size=34)

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name

        self.kwarg_handler(kwargs)

        self.blit_basic_buttons(screen)
        self.settings_button.blit_button(screen)

        if self.show_menu==True:
            self.settings_button.text='Back'
            self.blit_menu(screen)
        else:
            self.settings_button.text='Settings'

        pressed_button=self.handle_events(screen,curr_events)
        if pressed_button!=None:

            if pressed_button.name=='home_button':
                self.show_menu=False

            if pressed_button.name=='resolution':
                self.button_dict['resolution'].selected=True
                self.button_dict['gain'].selected=False
                self.button_dict['delay'].selected=False

            if pressed_button.name=='gain':
                self.button_dict['resolution'].selected=False
                self.button_dict['gain'].selected=True
                self.button_dict['delay'].selected=False

            if pressed_button.name=='delay':
                self.button_dict['resolution'].selected=False
                self.button_dict['gain'].selected=False
                self.button_dict['delay'].selected=True

            if pressed_button.name=='settings':
                self.show_menu= not self.show_menu

            for dikt in self.settings_dicts:
                if pressed_button.text in dikt.keys():
                    print (pressed_button.text, dikt[pressed_button.text])
                    self.send_code=dikt[pressed_button.text]
                    e.post(SET_UV_GAIN)

        self.blit_title(screen)

        x_pos=138
        y_pos=375
        if self.bluetooth_connected==True:

            try:
                self.uvs,self.light,self.uvi,self.ltr_lux,self.ltr_gain,self.ltr_resolution,self.ltr_window_factor,self.ltr_measurement_delay=get_uv()
            except Exception as e:
                self.uvs,self.light,self.uvi,self.ltr_lux,self.ltr_gain,self.ltr_resolution,self.ltr_window_factor,self.ltr_measurement_delay=-1,-1,-1,-1,-1,-1,-1,-1

            self.uv_gauge_img=self.uv_gauge.blit_gauge(self.uvs)

            try:
                UVI=round(float(self.uvi),2)
            except ValueError:
                UVI=-1
            self.uvi_gauge_img=self.uvi_gauge.blit_gauge(UVI)
            self.uv_gauge_img.set_colorkey((0,0,0))
            self.uvi_gauge_img.set_colorkey((0,0,0))

            screen.blit(self.uv_gauge_img,self.uv_gauge_origin)
            screen.blit(self.uvi_gauge_img,self.uvi_gauge_origin)

            if self.show_menu==False:

                self.blit_current_settings(screen)

        else:
            y_pos+=110
            FONT_FEDERATION.render_to(screen, (x_pos, y_pos+35), 'NO BLUETOOTH', WHITE, size=28)

        return self.next_screen_name,self.kwargs
