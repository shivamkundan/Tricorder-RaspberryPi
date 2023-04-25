from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN,FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW,  WHITE, SLATE
from serial_manager import get_gps
from images import SATELLITE, WORLD_MAP, ALT_ICON, SPD_ICON, DOT2, LAT_ICON
from global_functions import my_map

from pygame import draw as pdraw
# WORLD_MAP: 530 by 266

# lat/long limits for world map
left_lim=-167.3
right_lim=190.5
top_lim=84.7
bottom_lim=-56

# world map pic params
# PIC_TOP=250
PIC_TOP=175
PIC_LEFT=150

PIC_W=530
PIC_H=266
PIC_BOTTOM=PIC_TOP+PIC_H
PIC_RIGHT=PIC_LEFT+PIC_W

# top grid
row1=490
col1=170
col2=400

col3=col1+55
col4=col2+66

row2=row1+35

DOT2_W_DIV_2=10


class GPSSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        # ------ satellite icon ------ #
        self.SATELLITE_POS=(555,100)

        self.alt_pos=(col1,row1+5)
        self.spd_pos=(col2,row1+5)


        self.SATELLITE_TXT_POS=(self.SATELLITE_POS[0]+55,self.SATELLITE_POS[1]+20)

        self.lat=-1
        self.long=-1
        self.alt=-1
        self.spd=-1
        self.sat=-1


    def draw_location_lines(self,screen,x,y):
        if (self.sat>0):
            lw=2
            x_pos=PIC_LEFT+x-DOT2_W_DIV_2+lw/2
            pdraw.line(screen, SLATE, (x_pos,PIC_TOP), (x_pos,PIC_BOTTOM), width=lw)

            y_pos=PIC_TOP+y-DOT2_W_DIV_2-lw/2
            pdraw.line(screen, SLATE, (PIC_LEFT,y_pos), (PIC_RIGHT,y_pos), width=lw)

            # circle(surface, color, center, radius)


    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        FONT_FEDERATION.render_to(screen, (150, 92), 'GPS', ORANGE,style=0,size=65)

        self.lat,self.long,self.alt,self.spd,self.sat=get_gps()

        screen.blit(SATELLITE,self.SATELLITE_POS)
        screen.blit(ALT_ICON,self.alt_pos)
        screen.blit(SPD_ICON,self.spd_pos)


        FONT_DIN.render_to(screen, self.SATELLITE_TXT_POS, f"{self.sat}", WHITE,style=0,size=40)




        FONT_DIN.render_to(screen, (col3,row1), f'{round(self.alt,3)}m', WHITE,style=0,size=40)
        FONT_DIN.render_to(screen, (col3,row2), f'{round(self.alt*3.281,1)}ft', SLATE,style=0,size=24)

        FONT_DIN.render_to(screen, (col4,row1), f'{round(self.spd,3)}m/s', WHITE,style=0,size=40)
        FONT_DIN.render_to(screen, (col4,row2), f'{round(self.spd*2.237,3)}mph', SLATE,style=0,size=24)

        screen.blit(WORLD_MAP,(PIC_LEFT,PIC_TOP))
        # screen.blit(DOT2,(PIC_LEFT-DOT2_W_DIV_2,PIC_TOP-DOT2_W_DIV_2))    # this denotes where the world map starts
        # screen.blit(DOT2,(PIC_RIGHT-DOT2_W_DIV_2,PIC_BOTTOM-DOT2_W_DIV_2))    # ends


        row=610
        col=col1

        # screen.blit(LAT_ICON, (col-50,row))
        FONT_FEDERATION.render_to(screen, (col,row-25), "LAT", ORANGE,style=1,size=20)
        FONT_FEDERATION.render_to(screen, (col2,row-25), "LONG", ORANGE,style=1,size=20)



        FONT_DIN.render_to(screen, (col,row), f'{self.lat}', WHITE,style=0,size=34)
        y=round(my_map(self.lat,top_lim,bottom_lim,0,PIC_H),0)
        # FONT_HELVETICA_NEUE.render_to(screen, (col,row+40), f'lat px: {y}', WHITE,style=0,size=24)



        FONT_DIN.render_to(screen, (col2,row), f'{self.long}', WHITE,style=0,size=34)
        x=round(my_map(self.long,left_lim,right_lim,0,PIC_W),0)
        # FONT_HELVETICA_NEUE.render_to(screen, (435,595), f'long px: {x}', WHITE,style=0,size=24)


        self.draw_location_lines(screen,x,y)

        # if (self.sat>0):
        #     lw=2
        #     x_pos=PIC_LEFT+x-DOT2_W_DIV_2+lw/2
        #     pdraw.line(screen, SLATE, (x_pos,PIC_TOP), (x_pos,PIC_BOTTOM), width=lw)

        #     y_pos=PIC_TOP+y-DOT2_W_DIV_2-lw/2
        #     pdraw.line(screen, SLATE, (PIC_LEFT,y_pos), (PIC_RIGHT,y_pos), width=lw)

        # screen.blit(DOT2,(PIC_LEFT+x-20,PIC_TOP+y-20))

        return self.next_screen_name,self.kwargs
