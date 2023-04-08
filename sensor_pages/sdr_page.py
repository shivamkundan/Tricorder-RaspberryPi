import pygame

from page_templates import PageTemplate
from fonts import FONT_FEDERATION, ORANGE
from image_assets import NAV_BUTTONS

# -------------- Freqshow code -------------- #
import controller
import model
import ui

class SoftwareDefinedRadioPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='MenuHomePage'

        self.button_list+=NAV_BUTTONS
        self.init_freq=433.0
        self.fscontroller,self.fsmodel=self.init_sdr()

        try:
            self.fsmodel.set_center_freq(self.init_freq)
        except:
            pass
    def init_sdr(self):
        try:
            fsmodel = model.FreqShowModel(680,720)
            fscontroller = controller.FreqShowController(fsmodel)
        except Exception as e:
            print ('SDR not connected')
            fsmodel=None
            fscontroller =None

        return fscontroller, fsmodel



    def next_frame(self,screen,curr_events,**kwargs):

        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)

        self.blit_all_buttons(screen)
        pressed_button=self.handle_events(screen,curr_events)

        if pressed_button!=None:
            print (pressed_button.name)
            if pressed_button.name=='right_arrow':
                print ("right_arrow")
                self.fscontroller.toggle_main()

        if self.fscontroller==None:
            self.init_sdr()

        if self.fscontroller!=None:
            for event in pygame.event.get():

                if (event.type == pygame.FINGERUP or event.type==pygame.MOUSEBUTTONUP):
                    if (event.type == pygame.FINGERUP):
                        mouse_pos=(int(event.x*screen.get_width()),int(event.y*screen.get_height()))
                    else:
                        mouse_pos=pygame.mouse.get_pos()
                    self.fscontroller.current().click(mouse_pos)
            self.fscontroller.current().render(screen)





        FONT_FEDERATION.render_to(screen, (150, 67), 'Software Defined Radio', ORANGE,style=0,size=34)
        FONT_FEDERATION.render_to(screen, (150, 67+34+10), '24 - 1766 MHz', ORANGE,style=0,size=26)
        # FONT_FEDERATION.render_to(screen, (150, 67+34+10), 'SDR RTL2832 w/R820T', ORANGE,style=0,size=40)


        return self.next_screen_name,self.kwargs