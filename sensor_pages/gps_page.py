from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN,FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW,  WHITE, SLATE
from serial_manager import get_gps
from images import SATELLITE, WORLD_MAP, ALT_ICON, SPD_ICON, DOT2
from global_functions import my_map

# WORLD_MAP: 530 by 266

# lat/long limits for world map
left_lim=-167.3
right_lim=190.5
top_lim=84.7
bottom_lim=-56

# world map pic params
PIC_TOP=250
PIC_LEFT=150
PIC_W=530
PIC_H=266

PIC_BOTTOM=PIC_TOP+PIC_H
PIC_RIGHT=PIC_LEFT+PIC_W


class GPSSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        # ------ satellite icon ------ #
        self.SATELLITE_POS=(170,100)
        self.alt_pos=(170,190)
        self.spd_pos=(400,190)


        self.SATELLITE_TXT_POS=(self.SATELLITE_POS[0]+55,self.SATELLITE_POS[1]+20)

        self.lat=-1
        self.long=-1
        self.alt=-1
        self.spd=-1
        self.sat=-1


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 67), 'GPS', ORANGE,style=0,size=40)

        self.lat,self.long,self.alt,self.spd,self.sat=get_gps()

        screen.blit(SATELLITE,self.SATELLITE_POS)
        screen.blit(ALT_ICON,self.alt_pos)
        screen.blit(SPD_ICON,self.spd_pos)


        FONT_HELVETICA_NEUE.render_to(screen, self.SATELLITE_TXT_POS, f"{self.sat}", WHITE,style=0,size=32)

        row1=180
        col1=170+35

        row2=215
        col2=200+46


        FONT_DIN.render_to(screen, (col1,row1), f'{round(self.alt,3)}m', WHITE,style=0,size=40)
        FONT_DIN.render_to(screen, (col1,row2), f'{round(self.alt*3.281,1)}ft', SLATE,style=0,size=24)

        FONT_DIN.render_to(screen, (col2,row1), f'{round(self.spd,3)}m/s', WHITE,style=0,size=40)
        FONT_DIN.render_to(screen, (col2,row2), f'{round(self.spd*2.237,3)}mph', SLATE,style=0,size=24)

        screen.blit(WORLD_MAP,(PIC_LEFT,PIC_TOP))
        screen.blit(DOT2,(PIC_LEFT-5,PIC_TOP-5))    # this denotes where the world map starts
        screen.blit(DOT2,(PIC_RIGHT-5,PIC_BOTTOM-5))    # ends


        row=555
        col=195


        FONT_HELVETICA_NEUE.render_to(screen, (col,row), f'lat: {self.lat}', WHITE,style=0,size=34)
        y=round(my_map(self.lat,top_lim,bottom_lim,0,266),0)
        FONT_HELVETICA_NEUE.render_to(screen, (col,row+40), f'lat px: {y}', WHITE,style=0,size=24)



        FONT_HELVETICA_NEUE.render_to(screen, (435,555), f'long: {self.long}', WHITE,style=0,size=34)
        x=round(my_map(self.long,left_lim,right_lim,0,530),0)
        FONT_HELVETICA_NEUE.render_to(screen, (435,595), f'long px: {x}', WHITE,style=0,size=24)

        screen.blit(DOT2,(PIC_LEFT+x-5,PIC_TOP+y-5))

        return self.next_screen_name,self.kwargs
