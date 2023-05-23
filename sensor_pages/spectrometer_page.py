'''! @brief For visualizing AS7341 spectrometer readings.
@file spectrometer_page.py Contains definition for SpecPage class.
'''

from fonts import FONT_FEDERATION, FONT_DIN
from colors import ORANGE,DARK_YELLOW,WHITE
from page_templates import PageWithoutGauge
from global_functions import get_text_dimensions, my_map
import pygame.event as e
from serial_manager import get_spectrometer
import logging
# from pygame.draw import rect
import pygame

class SpecPage(PageWithoutGauge):
    '''! For visualizing AS7341 spectrometer readings.'''
    def __init__(self,name):
        '''! Constructor'''
        color_list=['violet','indigo','blue','cyan','green','yellow','orange','red']
        color_labels=['Violet\n415nm','Indigo\n445nm/','Blue\n480nm','Cyan\n515nm','Green\n555nm','Yellow\n590nm','Orange\n630nm','Red\n680nm']
        ## Holds integer <-> text mappings for gain settings
        self.gain_dict={'-1':'-1','0':'0.5X','1':'1X','2':'2X','3':'4X','4':'8X','5':'16X','6':'32X','7':'64X','8':'128X','9':'256X','10':'512X'}
        ## Default gain is set to -1
        self.gain='-1'
        ## Value for 'clear'
        self.clear=0
        ## Value for Near-IR
        self.nir=0
        ## Flicker detection status
        self.flicker_detection_enabled='-1'
        ## Channel names for AS7341,
        self.channels=['c_415nm','c_445nm','c_480nm','c_515nm','c_555nm','c_590nm','c_630nm','c_680nm','clear','nir']
        ## Number of frames between updates.
        self.num_tics=5
        self.weighted_color=(0,0,0)
        self.scaled_color=(0,0,0)
        self.closest_match_color=(0,0,0)
        super().__init__(name,color_list,color_labels)


    def info_subpage(self,screen,curr_vals):
        '''! Text display for all spectrometer channels.'''
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


    def scale_rgb(self,in_val):
        '''! Scales to 8-bit color
        @param in_val Unscaled (R,G,B) tuple.
        '''
        for level in [32,64,128,256,512,1024,2048,4096,8192,16384,32768,65535]:
            if (in_val<=level):
                max_val=level
                break

        out_val=int(round(my_map(in_val,0,max_val,0,255),0))
        # print (f"in_val:{in_val}, out_val:{out_val}")
        return out_val

    def scale_rgb2(self,in_val):
        '''! Scales to 8-bit color
        @param in_val Unscaled (R,G,B) tuple.
        '''
        R=in_val[0]
        G=in_val[1]
        B=in_val[2]

        for level in [32,64,128,256,512,1024,2048,4096,8192,16384,32768,65535]:
            # if (in_val<=level):
            #     max_val=level
            #     break
            if ((R <= level) and (G <= level) and (R <= level)):
                max_val=level
                break

        # elif ((R <= L2) and (G <= L2) and (R <= L2)):
        #     max_val=L2+1

        # elif ((R <= L3) and (G <= L3) and (R <= L3)):
        #     max_val=L3+1

        # elif ((R <= L4) and (G <= L4) and (R <= L4)):
        #     max_val=L3+1

        # elif ((R <= L5) and (G <= L5) and (R <= L5)):
        #     max_val=L5+1

        out_val_R=int(round(my_map(R,0,max_val,0,255),0))
        out_val_G=int(round(my_map(G,0,max_val,0,255),0))
        out_val_B=int(round(my_map(B,0,max_val,0,255),0))

        out_val=(out_val_R,out_val_G,out_val_B)


        print (f"#2: in_val:{in_val}, out_val:{out_val}")
        return out_val

    def match_color(self,x,screen):
        '''! Finds closest matching color in database'''
        try:
            R = int(x['c_680nm']) # Red
            G = int(x['c_555nm']) # Green
            B = int(x['c_480nm']) # Blue

            Y = int(x['c_590nm']) # Yellow
            O = int(x['c_630nm']) # Orange


            C = int(x['c_515nm']) # Cyan
            I = int(x['c_445nm']) # Indigo

            V = int(x['c_415nm']) # Violet



            print (R,G,B)

            # print(f"plain r,g,b: {self.scale_rgb(R)} {self.scale_rgb(G)} {self.scale_rgb(B)}")
            print(f"plain r,g,b: {self.scale_rgb2((R,G,B))}")

            R_p = self.scale_rgb((R+O+Y)/3)
            G_p = self.scale_rgb(G)
            B_p = self.scale_rgb((B+I+C+V)/4)

            print (R_p,G_p,B_p)

            weighted_color=(R_p,G_p,B_p)
            print (f"weighted_color:{weighted_color}")


            scaled_color=(self.scale_rgb(R),self.scale_rgb(G),self.scale_rgb(B))

            # pygame.draw.rect(screen, pygame.Color(R_p,G_p,B_p), (160,160+80, 80, 30))

            return weighted_color, scaled_color

        except Exception as e:
            print (e)
            return (0,0,0),(0,0,0)




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

            self.weighted_color, self.scaled_color=self.match_color(x,screen)

        pygame.draw.rect(screen, self.scaled_color, (100,160, 80, 30))
        pygame.draw.rect(screen, self.weighted_color, (2,160, 80, 30))


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