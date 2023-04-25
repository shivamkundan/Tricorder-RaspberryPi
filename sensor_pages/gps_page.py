from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_DIN,FONT_HELVETICA_NEUE
from colors import ORANGE, DARK_YELLOW,  WHITE
from serial_manager import get_gps
from images import SATELLITE, WORLD_MAP, ALT_ICON, SPD_ICON


class GPSSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        # ------ satellite icon ------ #
        self.SATELLITE_POS=(170,190)
        self.alt_pos=(335,190)
        self.spd_pos=(535,190)


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
        # FONT_FEDERATION.render_to(screen, (150, 117), 'gps', DARK_YELLOW,style=0,size=34)


        self.lat,self.long,self.alt,self.spd,self.sat=get_gps()

        screen.blit(SATELLITE,self.SATELLITE_POS)
        screen.blit(ALT_ICON,self.alt_pos)
        screen.blit(SPD_ICON,self.spd_pos)


        FONT_HELVETICA_NEUE.render_to(screen, self.SATELLITE_TXT_POS, f"{self.sat}", WHITE,style=0,size=32)
        FONT_HELVETICA_NEUE.render_to(screen, (335+40,215), f'{self.alt}m', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, (535+51,215), f'{self.spd}m/s', WHITE,style=0,size=26)

        screen.blit(WORLD_MAP,(150,250))

        row=555
        col=195
        FONT_HELVETICA_NEUE.render_to(screen, (col,row), f'lat: {self.lat}', WHITE,style=0,size=26)

        FONT_HELVETICA_NEUE.render_to(screen, (435,555), f'long: {self.long}', WHITE,style=0,size=26)

        return self.next_screen_name,self.kwargs
