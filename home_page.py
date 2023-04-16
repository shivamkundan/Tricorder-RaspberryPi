import pygame.event as e
from page_templates import *
from aa_arc_gauge import *
from custom_user_events import *
from paths_and_utils import *
from serial_manager import *


class HomePage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.client_sock=None

        self.recv_data=''
        self.sensor_dict={}
        self.frame_count=0
        self.bluetooth_count=0
        # self.bluetooth_connected=False

        self.wr_count=0
        self.msg_index=0
        self.page_cooldown_val=False

        # First msg updates all sensors
        # self.curr_msg='L U T P M V S '
        self.curr_msg='L T S U P V'
        # self.curr_msg=''
        self.c_temp,self.humid=0,0

        self.sensor_dict=SENSOR_DICT
        # Init surfaces for gauges
        self.TempGauge_img=pygame.Surface((0,0))
        self.HumidGauge_img=pygame.Surface((0,0))
        self.PressureGauge_img=pygame.Surface((0,0))
        self.eco2Gauge_img=pygame.Surface((0,0))
        self.tvoc_gauge_img=pygame.Surface((0,0))
        self.vis_gauge_img=pygame.Surface((0,0))
        self.ir_gauge_img=pygame.Surface((0,0))
        self.uv_gauge_img=pygame.Surface((0,0))
        self.uvi_gauge_img=pygame.Surface((0,0))
        self.spectrometer_img=pygame.Surface((0,0))

        # For bluetooth disconnect message
        with_dots='SEARCHING...'
        without_dots='SEARCHING'
        self.messages=[with_dots,with_dots,without_dots,with_dots,without_dots,with_dots,with_dots,with_dots]
        self.fonts=['Federation','Klingon','Romulan','Cardassian','Bajoran','Borg','Dominion','Ferengi']
        self.font_sizes=[66,62,66,74,46,80,80,58]
        self.bluetooth_msg_counter=0
        self.message=""

        # Plotting parameters
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=[3,3])
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.ax = self.fig.add_subplot(111)

        self.init_gauges()
        self.init_sensor_tics()

        # Drawing functions stored here
        self.my_display_funcs=[self.blit_vis_ir,self.blit_uv,self.blit_temp,self.blit_humid,self.display_particulate_matter,self.blit_tvoc_eco2,self.blit_pressure,self.blit_spectrometer]

        self.prev_page_name='menu_home_page'

    def on_enter(self):
        e.post(POWER_TSL_ON)
        e.post(POWER_PM25_ON)
        print ("homepage enter")

    def on_exit(self):
        e.post(POWER_PM25_OFF)
        print ("homepage enter")

    def init_sensor_tics(self):
        scale=1
        self.light_tics=int(1*scale)
        self.uv_tics=int(1*scale)
        self.temp_tics=int(2*scale)
        self.pressure_tics=int(3*scale)
        self.spectrometer_tics=int(2*scale)
        self.particulate_tics=int(2*scale)
        self.voc_tics=int(5*scale)


    def init_gauges(self):

        # --- set all counters  --- #
        gauges_start_col=150
        gauge_radius=65
        gauges_spacing=48
        weight=8
        arc_h=gauge_radius+weight//2
        font=FONT_DIN
        main_font_size=32
        f_color=WHITE



        self.temp_gauge_origin=(gauges_start_col,arc_h)
        self.TempGauge=AA_Gauge(None,(0),main_font_size=34,in_min=15,in_max=40,origin=self.temp_gauge_origin, radius=gauge_radius,weight=weight,color=YELLOW,suffix='°C',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,title='TEMP',title_font_size=14,auto_lims=False)

        self.humid_gauge_origin=(gauges_start_col+(2*gauge_radius)+gauges_spacing,arc_h)
        self.HumidGauge=AA_Gauge(None,(0),main_font_size=34,in_min=0,in_max=100,origin=self.humid_gauge_origin, radius=gauge_radius,weight=weight,color=BLUE,suffix='%',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,title='RH%',title_font_size=16,auto_lims=False)

        self.pressure_gauge_origin=(gauges_start_col+(5*gauge_radius)+gauges_spacing,arc_h)
        self.PressureGauge=AA_Gauge(None,(0),main_font_size=28,in_min=970,in_max=1030,origin=self.pressure_gauge_origin, radius=gauge_radius,weight=weight, color=ORANGE,suffix='hPa',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,title='PRESSURE',title_font_size=10,auto_lims=False)

        # ----
        rfs=16  #'range font size'
        arc_h+=gauge_radius*2+gauges_spacing-10
        gauge_radius=55
        gauges_spacing=5
        weight=8
        curr_col=gauges_start_col-10
        self.eco2_gauge_origin=(curr_col,arc_h)
        self.eco2Gauge=AA_Gauge(None,(400),in_min=0,in_max=1000,origin=self.eco2_gauge_origin, radius=gauge_radius,weight=weight,color=GREEN,suffix='ppm',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='TVOC',title_font_size=16)

        arc_h+=gauge_radius*2+gauges_spacing
        self.tvoc_gauge_origin=(curr_col,arc_h)
        self.tvocGauge=AA_Gauge(None,(0),in_min=0,in_max=1000,origin=self.tvoc_gauge_origin, radius=gauge_radius,weight=weight,color=GREEN,suffix='ppb',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='eCO2',title_font_size=16)

        # ----
        arc_h+=gauge_radius*2+gauges_spacing
        self.vis_gauge_origin=(curr_col,arc_h)
        self.vis_gauge=AA_Gauge(None,(0),in_min=0,in_max=1000,origin=self.vis_gauge_origin, radius=gauge_radius,weight=weight,color=RED,suffix='lux',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='VIS',title_font_size=16)

        self.ir_gauge_origin=(curr_col+(2.5*gauge_radius)+gauges_spacing,arc_h)
        self.ir_gauge=AA_Gauge(None,(0),in_min=0,in_max=1000,origin=self.ir_gauge_origin, radius=gauge_radius,weight=weight,color=RED,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='IR',title_font_size=16)

        # ----
        arc_h+=gauge_radius*2+gauges_spacing
        self.uv_gauge_origin=(curr_col,arc_h)
        self.uv_gauge=AA_Gauge(None,(0),in_min=0,in_max=10,origin=self.uv_gauge_origin, radius=gauge_radius,weight=weight,color=PURPLE,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='UV',title_font_size=16)

        self.uvi_gauge_origin=(curr_col+(2.5*gauge_radius)+gauges_spacing,arc_h)
        self.uvi_gauge=AA_Gauge(None,(0),in_min=0,in_max=10,origin=self.uvi_gauge_origin, radius=gauge_radius,weight=weight,color=PURPLE,suffix='',CURR_FONT=font,FONT_COLOR=f_color,empty_arc_color=DARK_GREY,solid_bg=False,range_font_size=rfs,title='UVI',title_font_size=16)

    # --------------------------------------------------------------------- #
    def blit_wrapper(self,g1,g2,val1,val2):
        g1_img=g1.blit_gauge(val1)
        g2_img=g2.blit_gauge(val2)
        g1_img.set_colorkey(BLACK)
        g2_img.set_colorkey(BLACK)
        return g1_img,g2_img

    def blit_pressure(self,screen):
        if (self.bluetooth_count%self.pressure_tics==0):
            # print ('updating pressure')
            _,pressure,_,_,_=get_pressure()
            self.PressureGauge_img=self.PressureGauge.blit_gauge(pressure)
            self.PressureGauge_img.set_colorkey((0,0,0))
        screen.blit(self.PressureGauge_img,self.pressure_gauge_origin)

    def blit_temp(self,screen):

        if (self.bluetooth_count%self.temp_tics==0):
            # print ('updating temp')
            self.c_temp,self.humid,_,_=get_temp_humid()

            self.TempGauge_img=self.TempGauge.blit_gauge(self.c_temp)
            self.TempGauge_img.set_colorkey((0,0,0))
        screen.blit(self.TempGauge_img,self.temp_gauge_origin)

    def blit_humid(self,screen):

        if (self.bluetooth_count%self.temp_tics==0):
            # print ('updating humid')
            self.HumidGauge_img=self.HumidGauge.blit_gauge(self.humid)
            self.HumidGauge_img.set_colorkey((0,0,0))
        screen.blit(self.HumidGauge_img,self.humid_gauge_origin)

    def blit_tvoc_eco2(self,screen):
        if (self.bluetooth_count%self.voc_tics==0):
            # print ('updating tvoc/eco2')
            eCO2,TVOC,_,_=get_tvoc_eco2()
            self.tvoc_gauge_img,self.eco2Gauge_img=self.blit_wrapper(self.tvocGauge,self.eco2Gauge,eCO2,TVOC)
        screen.blit(self.eco2Gauge_img,self.eco2_gauge_origin)
        screen.blit(self.tvoc_gauge_img,self.tvoc_gauge_origin)

    def blit_vis_ir(self,screen):
        try:
            if (self.bluetooth_count%self.light_tics==0):
                # print ('updating vis/ir')
                lux,ir,gain,visible,full_spectrum = get_vis_ir()
                self.vis_gauge_img,self.ir_gauge_img=self.blit_wrapper(self.vis_gauge,self.ir_gauge,lux,ir)
            screen.blit(self.vis_gauge_img,self.vis_gauge_origin)
            screen.blit(self.ir_gauge_img,self.ir_gauge_origin)
        except Exception as e:
            print ('blit_vis_ir: ',e)

    def blit_uv(self,screen):

        try:
            if (self.bluetooth_count%self.uv_tics==0):


                uvs,_,uvi,_,_,_,_,_=get_uv()
                self.uv_gauge_img=self.uv_gauge.blit_gauge(uvs)
                self.uvi_gauge_img=self.uvi_gauge.blit_gauge(uvi)
                self.uv_gauge_img.set_colorkey((0,0,0))
                self.uvi_gauge_img.set_colorkey((0,0,0))
            screen.blit(self.uv_gauge_img,self.uv_gauge_origin)
            screen.blit(self.uvi_gauge_img,self.uvi_gauge_origin)
        except:
            pass

    def blit_spectrometer(self,screen):
        if (self.bluetooth_count%self.spectrometer_tics==0):
            color_labels=['Violet\n415nm','Indigo\n445nm/','Blue\n480nm','Cyan\n515nm','Green\n555nm','Yellow\n590nm','Orange\n630nm','Red\n680nm']
            color_list=['violet','indigo','blue','cyan','green','yellow','orange','red']
            # SD=self.sensor_dict
            SD=get_spectrometer()
            spectrum=[  SD['c_415nm'],
                        SD['c_445nm'],
                        SD['c_480nm'],
                        SD['c_515nm'],
                        SD['c_555nm'],
                        SD['c_590nm'],
                        SD['c_630nm'],
                        SD['c_680nm']
                    ]


            curr_vals=[self.scale(int(x)) for x in spectrum]

            self.spectrometer_img=pie_plot(self.fig,self.ax,self.canvas,color_list,color_labels,curr_vals)

        screen.blit(self.spectrometer_img, (400, 420))

    def display_particulate_matter(self,screen):
        # screen=self.screen
        try:
            # SD=self.sensor_dict
            # ==== particulate matter ==== #
            pm25_font=star_trek_fonts['din-condensed-light']
            # pm25_curr_vals=[str(SD["03um"]),str(SD["05um"]),str(SD["10um"]),str(SD["25um"]),str(SD["50um"]),str(SD["100um"])]

            pm25_curr_vals=get_pm25()
            title_txt='        Particles / 0.1L air'
            particle_txt_list=[FONT_DIN.render(title_txt,fgcolor=WHITE,rotation=0,size=15)]

            x_labels=['>0.3um ','>0.5um ','>1.0um ','>2.5um ','>5.0um ','>10um  ']

            try:
                x_len=168
                bar_vals=[]
                for val,label in zip(pm25_curr_vals,x_labels):
                    val=int(val)
                    if val!=0:
                        log_val=int(round(math.log10(val),0))
                        bar_vals.append(int(round((log_val/4.8)*x_len,0)))
                    else:
                        bar_vals.append(0)
                    # particle_txt=pm25_font.render(label+' ['+str(val)+' ] ',1,WHITE)
                    particle_txt=FONT_DIN.render(label+' ['+str(val)+'] ',fgcolor=WHITE,rotation=0,size=15)
                    particle_txt_list.append(particle_txt)
            except ValueError:
                pass
            # ============================ #

            # blit the text
            row=245
            col=360
            for txt in particle_txt_list:
                # txt_height=txt.get_size()[1]
                w,txt_height=txt[1][2],txt[1][3]
                screen.blit(txt[0],(col,row))
                row+=txt_height+15

            y_pos=275
            x_start=520
            x_end=x_start+x_len

            # print (bar_vals)

            for log_val in bar_vals:
                pygame.draw.line(screen,DARK_GREY,(x_start,y_pos),(x_end,y_pos),5)
                pygame.draw.line(screen,ORANGE,(x_start,y_pos),(x_start+log_val,y_pos),5)
                y_pos+=27


        except Exception as e:
            print (e)
            # raise (e)

    def scale(self,read_value):
        scaled = int(round(int(read_value / 1000),0))
        return read_value
    # --------------------------------------------------------------------- #
    def print_message(self,screen):
        # if self.bluetooth_msg_counter%5==0:
        self.msg_index=self.frame_count%len(self.fonts)
        self.bluetooth_msg_counter+=1

        curr_font=star_trek_fonts[self.fonts[self.msg_index]]
        siz=self.font_sizes[self.msg_index]
        self.message=self.messages[self.msg_index]


        msg_txt=curr_font.render(self.message,fgcolor=SLATE,rotation=0,size=siz)
        w,h=msg_txt[1][2],msg_txt[1][3]
        screen.blit(msg_txt[0],((screen.get_width()//2-w//2+40),screen.get_height()//2-h//2+20))
        time.sleep(0.2)

    # --------------------------------------------------------------------- #
    def next_frame(self,screen,curr_events,**kwargs):
        # self.page_cooldown_val=False
        # self.page_cooldown_val=0
        try:
            self.next_screen_name=self.name
            self.kwarg_handler(kwargs)
            pressed_button=self.handle_events(screen,curr_events)

            self.blit_all_buttons(screen)

            if PERIPHERAL_MODE=='bluetooth' and self.client_sock == None:
                self.print_message(screen)

            else:

                # Draw everything
                if self.sensor_dict!=None:
                    for curr_func in self.my_display_funcs:
                        curr_func(screen)
                else:
                    print ('sensor_dict is None')



            # Show bluetooth count
            count_txt=FONT_18.render(str(self.bluetooth_count),1,WHITE)
            screen.blit(count_txt,(25,100))
        except Exception as e:
            print(e)

        self.frame_count+=1

        return self.next_screen_name,self.kwargs
