from fonts import FONT_FEDERATION, FONT_DIN
from colors import ORANGE,DARK_YELLOW,WHITE
from page_templates import PageWithoutGauge
from global_functions import get_text_dimensions
import pygame.event as e
from serial_manager import get_spectrometer
import logging

class SpecPage(PageWithoutGauge):
    def __init__(self,name):
        color_list=['violet','indigo','blue','cyan','green','yellow','orange','red']
        color_labels=['Violet\n415nm','Indigo\n445nm/','Blue\n480nm','Cyan\n515nm','Green\n555nm','Yellow\n590nm','Orange\n630nm','Red\n680nm']
        self.gain_dict={'-1':'-1','0':'0.5X','1':'1X','2':'2X','3':'4X','4':'8X','5':'16X','6':'32X','7':'64X','8':'128X','9':'256X','10':'512X'}
        self.gain='-1'
        self.clear=0
        self.nir=0
        self.flicker_detection_enabled='-1'
        self.channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
        self.num_tics=5
        super().__init__(name,color_list,color_labels)

    def info_subpage(self,screen,curr_vals):
        col1=170
        col2=265
        row=200
        y_spacing=20

        if len(curr_vals)>0:
            uuu=0
            for name,val in zip(reversed(self.color_list),reversed(curr_vals)):

                if uuu==4:
                    row=200
                    col1=col1+240
                    col2=col2+240

                txt_surf,w,h1=get_text_dimensions(text=name.upper()+':',font_style=FONT_FEDERATION,font_color=ORANGE,style=1,font_size=26)
                screen.blit(txt_surf,(col1,row))
                row+=h1+y_spacing

                txt_surf,w,h2=get_text_dimensions(text=f'{int(val):,}',font_style=FONT_DIN,font_color=WHITE,style=0,font_size=30)
                screen.blit(txt_surf,(col2,row))
                row+=h2+1.6*y_spacing

                uuu+=1

    def next_frame(self,screen,curr_events,**kwargs):

        # ----- get vals ----- #
        if self.frame_count%self.num_tics==0:
            x=get_spectrometer()
            self.i+=1
            self.x.append(self.i)
            for color_name,channel in zip(self.names_list,self.channels):
                try:
                    val=x[channel]
                except Exception as e:
                    logging.error(f"{e}: recvd: {x}")
                    val=0
                    FONT_DIN.render_to(screen, (290, 240), f'ERR: {channel}', WHITE,style=0,size=26)
                self.array_dict[color_name].append(int(float(val)))

            try:
                self.clear=x['clear']
                self.nir=x['nir']
            except Exception as e:
                logging.error(e)
                self.clear=-1
                self.nir=-1
                FONT_DIN.render_to(screen, (290, 305), f'ERR: clear/nir', WHITE,style=0,size=26)

        curr_vals=[]
        for name, color_array in self.array_dict.items():
            curr_vals.append(color_array[-1])

        self.next_frame_base(screen,curr_events,curr_vals,**kwargs)

         # Blit text
        FONT_FEDERATION.render_to(screen, (150, 67), 'Spectrometer', ORANGE,style=0,size=44)
        FONT_FEDERATION.render_to(screen, (150, 117), 'AS7341', DARK_YELLOW,style=0,size=34)
        FONT_DIN.render_to(screen, (370, 117), str(self.i), WHITE,style=0,size=26)
        FONT_DIN.render_to(screen, (430, 117), str(self.frame_count), WHITE,style=0,size=26)
        summ=0
        for color_name,array in self.array_dict.items():
            summ+=array[-1]
        FONT_DIN.render_to(screen, (430, 137), f'total: {summ:,}', WHITE,style=0,size=26)
        FONT_DIN.render_to(screen, (430, 150), f'gain: {self.gain_dict[self.gain]}', WHITE,style=0,size=26)
        FONT_DIN.render_to(screen, (200, 180), f'flicker_det: {self.flicker_detection_enabled}', WHITE,style=0,size=26)

        # show menu
        if self.button_dict['preferences'].selected:
            FONT_DIN.render_to(screen, (150, 195), f'rolling tics: {self.rolling_tics}', WHITE,style=0,size=26)
            self.button_dict['edit'].blit_button(screen)

        elif self.button_dict['info'].selected:
            self.info_subpage(screen,curr_vals)

        return self.next_screen_name,self.kwargs