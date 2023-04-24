from page_templates import PageTemplate
from fonts import FONT_FEDERATION, FONT_HELVETICA_NEUE,FONT_DIN
from colors import DARK_YELLOW,SLATE,WHITE,ORANGE
import pygame
import os
from buttons import NAV_BUTTONS
from paths_and_utils import IMG_PATH
from serial_manager import set_tsl_scl_disconnect,get_imu_orientation,get_imu_ang_vel,get_imu_lin_acc,get_imu_acc, get_imu_mag,get_imu_grav
import logging
from images import COMPASS, ENT_BACK, ENT_SIDE, DOT, XYZ_3D_ROT, XYZ_3D


compass_pos=(275,190)
roll_pos=(150,535)
pitch_pos=(440,460)

# -------------- #
START_X=400
START_Y=333
OUTER_RADIUS=150
END_X=START_X+OUTER_RADIUS
END_Y=START_Y+OUTER_RADIUS
ACC_ORIGIN=(START_X,START_Y)

DOT_RADIUS=40
DOT_POS_X=START_X-DOT_RADIUS/2
DOT_POS_Y=START_Y-DOT_RADIUS/2
# -------------- #

POS_X=(544,395)
POS_Y=(510,215)
POS_Z=(330,518)

def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    # pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)

class IMUSensorPage(PageTemplate):
    def __init__(self,name):
        super().__init__(name)
        self.prev_page_name='menu_home_page'

        self.button_list+=NAV_BUTTONS

        self.curr_subpage=0
        self.subpages_list=["ORIENTATION","LINEAR ACC","ANGULAR VELOCITY","GRAVITY","ACCELEROMETER","MAGNETOMETER"]
        self.num_pages=len(self.subpages_list)

        self.heading=-1
        self.roll=-1
        self.pitch=-1

        self.ang_vel_x=-1
        self.ang_vel_y=-1
        self.ang_vel_z=-1

        self.lin_acc_x=-1
        self.lin_acc_y=-1
        self.lin_acc_z=-1

        self.mag_x=-1
        self.mag_y=-1
        self.mag_z=-1

        self.acc_x=-1
        self.acc_y=-1
        self.acc_z=-1

        self.grav_x=-1
        self.grav_y=-1
        self.grav_z=-1

    def on_enter(self):
        logging.info(f"entering {self.__class__.__name__}")
        set_tsl_scl_disconnect()

    def blit_page_num(self,screen):
        FONT_FEDERATION.render_to(screen, (30, 100), str(self.curr_subpage+1)+'/'+str(self.num_pages), SLATE,style=0,size=28)
        FONT_FEDERATION.render_to(screen, (370, 640), str(self.curr_subpage+1)+'/'+str(self.num_pages), DARK_YELLOW,style=0,size=18)


    def blit_orientation(self,screen):


        self.heading,self.pitch,self.roll=get_imu_orientation()


        blitRotate2(screen, COMPASS, compass_pos, -1*int(round(float(self.heading),0)))
        blitRotate2(screen, ENT_BACK, roll_pos, int(round(float(self.roll),0)))
        blitRotate2(screen, ENT_SIDE, pitch_pos, -1*int(round(float(self.pitch),0)))

        FONT_DIN.render_to(screen, (260,160), f'Heading', DARK_YELLOW,style=0,size=26)
        FONT_DIN.render_to(screen, (525,530), f'Pitch', DARK_YELLOW,style=0,size=26)
        FONT_DIN.render_to(screen, (362,566), f'Roll', DARK_YELLOW,style=0,size=26)

        FONT_HELVETICA_NEUE.render_to(screen, (260,160+30), f'{self.heading}°', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, (525,530+30), f'{self.pitch}°', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, (362,566+30), f'{self.roll}°', WHITE,style=0,size=26)

    def blit_linear_acc(self,screen):

        self.lin_acc_x,self.lin_acc_y,self.lin_acc_z=get_imu_lin_acc()

        FONT_HELVETICA_NEUE.render_to(screen, (260,160+30), f'{self.lin_acc_x}', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, (525,530+30), f'{self.lin_acc_y}', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, (362,566+30), f'{self.lin_acc_z}', WHITE,style=0,size=26)

        pygame.draw.circle(screen, WHITE, ACC_ORIGIN, 150, 3)
        pygame.draw.circle(screen, WHITE, ACC_ORIGIN, 100, 3)
        pygame.draw.circle(screen, WHITE, ACC_ORIGIN, 50, 3)

        scale=10
        offset_x=int(round(float(self.lin_acc_x)*scale,0))
        offset_y=int(round(float(self.lin_acc_y)*scale,0))
        screen.blit(DOT,(DOT_POS_X-offset_x,DOT_POS_Y-offset_y))


    def blit_angular_velocity(self,screen):

        self.ang_vel_x,self.ang_vel_y,self.ang_vel_z=get_imu_ang_vel()

        FONT_HELVETICA_NEUE.render_to(screen, POS_X, f'{self.ang_vel_x}rad/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Y, f'{self.ang_vel_y}rad/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Z, f'{self.ang_vel_z}rad/s', WHITE,style=0,size=26)


        screen.blit(XYZ_3D_ROT,(180,180))

    def blit_gravity(self,screen):

        # e.post(REQUEST_IMU_GRAV)
        self.grav_x,self.grav_y,self.grav_z=get_imu_grav()

        FONT_HELVETICA_NEUE.render_to(screen, POS_X, f'{self.grav_x}m/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Y, f'{self.grav_y}m/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Z, f'{self.grav_z}m/s', WHITE,style=0,size=26)
        screen.blit(XYZ_3D, (180, 180))


    def blit_accelerometer(self,screen):

        self.acc_x,self.acc_y,self.acc_z=get_imu_acc()

        FONT_HELVETICA_NEUE.render_to(screen, POS_X, f'{self.acc_x}m/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Y, f'{self.acc_y}m/s', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Z, f'{self.acc_z}m/s', WHITE,style=0,size=26)
        screen.blit(XYZ_3D, (180, 180))

    def blit_magnetometer(self,screen):

        self.mag_x,self.mag_y,self.mag_z=get_imu_mag()

        FONT_HELVETICA_NEUE.render_to(screen, POS_X, f'{self.mag_x}μT', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Y, f'{self.mag_y}μT', WHITE,style=0,size=26)
        FONT_HELVETICA_NEUE.render_to(screen, POS_Z, f'{self.mag_z}μT', WHITE,style=0,size=26)
        screen.blit(XYZ_3D, (180, 180))


    def increment_subpage(self):
        if self.curr_subpage<self.num_pages:
            self.curr_subpage+=1
    def decrement_subpage(self):
        if self.curr_subpage>0:
            self.curr_subpage-=1

    def next_frame(self,screen,curr_events,**kwargs):
        self.next_screen_name=self.name
        self.kwarg_handler(kwargs)
        self.blit_all_buttons(screen)


        for event in curr_events:
            if event.type==pygame.KEYUP:
                if (event.key == pygame.K_RIGHT):
                    curr_events.remove(event)
                    self.increment_subpage()

                if (event.key == pygame.K_LEFT):
                    curr_events.remove(event)
                    self.decrement_subpage()

        pressed_button=self.handle_events(screen,curr_events)
        if pressed_button!=None:

            if pressed_button.name=='right_arrow':
                self.increment_subpage()
            if pressed_button.name=='left_arrow':
                self.decrement_subpage()




        # print (f"curr_subpage: {self.curr_subpage}")

        FONT_FEDERATION.render_to(screen, (150, 67), 'IMU', ORANGE,style=0,size=40)
        FONT_FEDERATION.render_to(screen, (150, 117), self.subpages_list[self.curr_subpage], DARK_YELLOW,style=0,size=24)
        self.blit_page_num(screen)


        # row=190
        # col=190
        # screen.blit(self.axes_alt, (col, row))

        # col+=200
        # screen.blit(self.axes_alt, (col, row))




        if self.curr_subpage==0:
            self.blit_orientation(screen)
        elif self.curr_subpage==1:
            self.blit_linear_acc(screen)
        elif self.curr_subpage==2:
            self.blit_angular_velocity(screen)
        elif self.curr_subpage==3:
            self.blit_gravity(screen)
        elif self.curr_subpage==4:
            self.blit_accelerometer(screen)
        elif self.curr_subpage==5:
            self.blit_magnetometer(screen)



        #
        # REQUEST_IMU_LIN_ACC
        #
        #
        #


        # row+=190
        # col=190
        # screen.blit(self.axes_alt, (col, row))

        # col+=300
        # screen.blit(self.axes_alt, (col, row))

        return self.next_screen_name,self.kwargs
