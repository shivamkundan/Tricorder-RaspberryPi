#!/usr/bin/python3

import pygame,sys,time
from enum import Enum
from pygame.sprite import Sprite
import pygame.gfxdraw
import pygame.freetype
from image_assets import *
from fonts import *
import numpy as np


# ---- arc parameters ---- #
radius=35
# offset=75
RAD_CONSTANT=0.0174533
# RAD_CONSTANT=0.0175

def get_text_dimensions(text='',font_style=FONT_DIN,font_color=WHITE,style=0,font_size=28):
    val_txt=font_style.render(text,fgcolor=font_color,size=font_size)
    x=list(val_txt)
    w=x[1][2]
    h=x[1][3]
    surf=x[0]
    return surf,w,h

def my_map(x,in_min,in_max,out_min,out_max): 
  return (float(x) - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class AA_Gauge():
    def __init__(self,
        screen,
        curr_val=None,
        in_min=0,
        in_max=100,
        radius=30,
        origin=(50,50),
        weight=3,
        color=RED,
        empty_arc_color=GREY,
        CURR_FONT=FONT_HELVETICA_NEUE,
        main_font_size=28,
        FONT_COLOR=WHITE,
        solid_bg_color=BLACK,
        range_color=DARK_GREY,
        range_font=FONT_HELVETICA_NEUE,
        range_font_size=24,
        suffix='',
        print_num=True,
        solid_bg=False,
        draw_empty_arc=True,
        print_range=True,
        print_title=True,
        title='',
        title_font_size=18,
        title_font=FONT_FEDERATION,
        title_font_color=LIGHT_GREY,
        auto_lims=True,
        offset=45):

        self.screen=screen
        self.curr_val=curr_val
        self.in_min=in_min
        self.in_max=in_max
        self.weight=weight
        self.offset=offset
        self.init_radius(radius)
        self.gauge_radius=self.radius
        self.init_origin()
        self.update_boundries()
        
        self.max_val=180+2*offset


        self.color=color
        self.empty_arc_color=empty_arc_color
        self.suffix=suffix
        self.print_num=print_num
        self.solid_bg=solid_bg
        self.draw_empty_arc=draw_empty_arc
        self.CURR_FONT=CURR_FONT
        self.main_font_size=main_font_size
        self.FONT_COLOR=FONT_COLOR
        self.solid_bg_color=solid_bg_color
        self.print_range=print_range
        self.range_font=range_font
        self.range_font_size=range_font_size
        self.range_color=range_color
        self.print_title=print_title
        self.title=title
        self.title_font_size=title_font_size
        self.title_font=title_font
        self.title_font_color=title_font_color
        self.auto_lims=auto_lims


    def init_origin(self):
        self.origin_x=self.radius+self.weight
        self.origin_y=self.radius+self.weight
        self.origin= (self.origin_x,self.origin_y)

    def init_radius(self,new_radius):
        self.radius=new_radius
        self.d=self.radius*2
        # self.weight=self.gauge_radius//self.weight_ratio

    def set_origin(self,new_xy):
        self.init_origin(new_xy)
        self.update_boundries()

    def set_radius(self,new_radius):
        self.init_radius(new_radius)
        self.update_boundries()

    def update_boundries(self):
        w=self.weight
        r=self.radius
        d=self.d-1
        x=self.origin_x
        y=self.origin_y
        j=(2*self.offset/360)*(r+w)
        # self.bounding_rect=[(x-(r+w//2)),(y-(r+w//2)),(d+w//2),(d+w//2)]
        self.bounding_rect=[0,0,(d+w*2),(d+w*2)]

    def adjust_gauge_lims(self):
        lower_lims=[0,0.1,1,10,100,1000,10000,100000]
        upper_lims=[0.1,1,10,100,1000,10000,100000,1000000]
        for low,up in zip(lower_lims,upper_lims):
            if low<=self.curr_val<up:
                self.in_max=up

    def update_val(self,new_val):
        self.curr_val=new_val
        if self.auto_lims:
            self.adjust_gauge_lims()

    def blit_gauge(self,new_val,print_val=None):

        # ----------------- arc params ----------------- #
        radius=self.radius
        # j=int((self.offset/360)*(radius))
        size=((self.d+self.weight),(self.d+self.weight*2))
        surf = pygame.Surface(size)
        # surf.fill(BLUE)
        # ----------------- draw background ----------------- #
        if (self.solid_bg):
            pygame.draw.rect(surf, self.solid_bg_color, self.bounding_rect)
            surf.fill(self.solid_bg_color)

        # ------------- Empty Arc Params ------------- #
        # draw empty arc
        # arc(surface, x, y, r, start_angle, stop_angle, color)

        x=size[0]//2
        y=size[1]//2-self.weight//2
        start_angle=(180-self.offset)
        end_angle=(360+self.offset)

        # rangee=np.linspace(0,255,self.weight//2)


        empty_radius_range=range(radius-self.weight//4,radius+self.weight//4)
        radius_range=range(radius-self.weight//2,radius+self.weight//2)

       # ------------- Draw Arc ------------- #
        if new_val is not None:
            try:
                new_val=float(new_val)
            except Exception as e:
                new_val=-2
                print ('aa_arc_gauge: ',e)

            if print_val!=None:
                orig=print_val
            else:
                orig=round(new_val,2)

            # print ('new_val: ',new_val)
            # print(type(new_val))
            self.update_val(new_val)
            curr_val_scaled=my_map(self.curr_val,self.in_min,self.in_max,start_angle,end_angle)

            # --- draw empty arc --- #
            if (self.draw_empty_arc):
                for curr_r in empty_radius_range:
                    try:
                        pygame.gfxdraw.arc(surf, x,y, curr_r,int(round(curr_val_scaled,2)), end_angle, self.empty_arc_color)
                    except OverflowError as e:
                        print (e)
                        print (curr_val_scaled)
                    except ValueError as e:
                        print (e)
                        print (curr_val_scaled)

            jj=np.linspace(start_angle, curr_val_scaled, 255)
            alpha_vals=np.linspace(20,255,len(jj))
            
            arc_angles=[]
            if (len(jj)>2):
                for index in range((len(jj)-1)):
                    start_ang=int(jj[index])
                    end_ang=int(jj[index+1])
                    ccooll=(self.color[0], self.color[1], self.color[2], int(alpha_vals[index+1]))
                    arc_angles.append([start_ang,end_ang,ccooll])

            for item in arc_angles:
                s=item[0]
                e=item[1]
                c=item[2]
                for curr_r in radius_range:
                    try:
                        pygame.gfxdraw.arc(surf, x, y , curr_r,s, e, c)
                    except OverflowError as o:
                        print (o)
                        print (curr_val_scaled)

        # ------------- Print Range ------------- #
        if (self.print_range):
            r_div_2=radius//2
            range_y_pos=(radius*2+self.weight//2)

            txt_surf,w,h=get_text_dimensions(f'{self.in_min:,}',font_style=self.range_font,font_color=self.range_color,style=0,font_size=self.range_font_size)
            surf.blit(txt_surf,(10,range_y_pos-h))

            txt_surf,w,h=get_text_dimensions(f'{self.in_max:,}',font_style=self.range_font,font_color=self.range_color,style=0,font_size=self.range_font_size)
            surf.blit(txt_surf,(int(size[0]-self.weight-w),range_y_pos-h))


        # ------------- Print Curr Value 

        if (self.print_num):
            if len(str(orig).split('.'))>1:
                t0=str(orig).split('.')[0]
                t1=str(orig).split('.')[1]
                if t1=='0':
                    t1=''
                else:
                    t1='.'+t1
            else:
                t0=orig
                t1=''

            curr_val_surf,w,h=get_text_dimensions(text="{}".format(t0),font_style=self.CURR_FONT,font_color=WHITE,style=0,font_size=self.main_font_size)
            decimal_surf,w2,h2=get_text_dimensions(text=f'{t1}',font_style=self.CURR_FONT,font_color=WHITE,style=0,font_size=self.main_font_size//2-1)
            suffix_surf,w3,h3=get_text_dimensions(text="{}".format(self.suffix),font_style=self.CURR_FONT,font_color=WHITE,style=0,font_size=self.main_font_size//2-1)

            total_len=w+max(w2,w3)

            if t1=='':
                h_correction= -h3
            else:
                h_correction=0

            curr_x=self.bounding_rect[0]+radius+self.weight//2-total_len//2
            curr_y=self.bounding_rect[1]+radius+self.weight//2-h//2
            surf.blit(curr_val_surf,(curr_x,curr_y))

            space=5

            surf.blit(decimal_surf,(curr_x+w+space,self.bounding_rect[1]+radius+self.weight//2-h//2))


            surf.blit(suffix_surf,(curr_x+w+space,self.bounding_rect[1]+radius+self.weight//2-h//2+h2+1+h_correction))

        # ------------- Print Title
        if (self.print_title) and self.title!='':
            # self.title='VIS'
            txt_surf,w,h=get_text_dimensions(text=self.title,font_style=self.title_font,font_color=self.title_font_color,style=1,font_size=self.title_font_size)
            surf.blit(txt_surf,(self.bounding_rect[0]+radius+self.weight//2-w//2,self.bounding_rect[1]+r_div_2+self.weight//2-h//2))

        return surf

def fps_manager(clock,screen,fps_array):

    curr_fps=round(clock.get_fps(),2)

    if curr_fps>0:
        fps_array=np.append(fps_array,curr_fps)

    if (3<curr_fps<70):
        fps_txt=FONT_20.render("{} fps".format(curr_fps), 1, WHITE)
        _,_,w,h=fps_txt.get_bounding_rect()
        screen.blit(fps_txt,((screen_w//2-w//2,1)))

    try:
        minn=round(np.min(fps_array),2)
        maxx=round(np.max(fps_array),2)
        avg=round(np.mean(fps_array),2)
        median=round(np.median(fps_array),2)
        total=len(fps_array)

        fps_txt=FONT_20.render("min:{}  max:{}  avg:{}  median:{} total:{}".format(minn,maxx,avg,median,total), 1, WHITE)
        _,_,w,h=fps_txt.get_bounding_rect()
        screen.blit(fps_txt,(3,screen_h-2*h))
    except:
        pass

    return fps_array

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key==ord('q'))):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':

    # pygame initialization
    screen_w=400
    screen_h=400
    pygame.init()
    screen = pygame.display.set_mode((screen_w, screen_h),pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT)
    clock = pygame.time.Clock()

    # gauge-related variables
    origin=(screen_w//2,screen_h//2)
    in_min=1
    in_max=10

    padding_x=0 # padding between actual bounding rect and final rect
    padding_y=0

    color_list=[RED,
                DARK_RED,
                YELLOW,
                DARK_YELLOW,
                ORANGE,
                GREEN,
                BLUE,
                GRID_BLUE,
                BLUE_GREY,
                MISTY_BLUE,
                PURPLE,
                VIOLET,
                CREAM]

    color_names_list=['RED',
                        'DARK_RED',
                        'YELLOW',
                        'DARK_YELLOW',
                        'ORANGE',
                        'GREEN',
                        'BLUE',
                        'GRID_BLUE',
                        'BLUE_GREY',
                        'MISTY_BLUE',
                        'PURPLE',
                        'VIOLET',
                        'CREAM']


    color_txt=FONT_20.render('{}'.format(color_list[0]),1,WHITE)

    # other variables
    max_fps=0
    min_fps=100000
    downcount=False
    fps_array=np.array([])

    # init the gauge
    G=AA_Gauge(screen,0,radius=100,weight=8,in_max=in_max,print_num=True,solid_bg=False,solid_bg_color=YELLOW,color=RED,draw_empty_arc=True,empty_arc_color=(96,96,96,120),origin=origin,suffix='Lux',main_font_size=50)


    while 1:
        # determine range
        if downcount:
            my_range=reversed(range(in_min,in_max+1))
        else:
            my_range=range(in_min,in_max+1)


        for curr_val in my_range:
            curr_val+=1/curr_val
            # print (curr_val)
            clock.tick()
            screen.fill(BLACK)
            handle_events()

            gauge_img=G.blit_gauge(curr_val)

            bounding_rect=gauge_img.get_bounding_rect()
            # print (j)

            pos=(screen_w//4-G.radius//2,screen_h//4-G.radius//2)

            screen.blit(gauge_img,pos)

            left=pos[0]-padding_x
            top=pos[1]-padding_y
            width=bounding_rect[2]+2*padding_x
            height=bounding_rect[3]+2*padding_y
            rekt=[left,top,width,height]

            pygame.gfxdraw.rectangle(screen, rekt, WHITE)



            if (curr_val%25==0):
                my_color=curr_val%len(color_list)
                G.color=color_list[my_color]
                # print ('my_color: ',my_color,color_names_list[my_color])
                color_txt=FONT_36.render('{}'.format(color_names_list[my_color]),1,WHITE)

                # if downcount:
                #     G.weight-=10
                #     G.update_boundries()
                #     G.set_radius(G.radius-10)
                # else:
                #     G.weight+=10
                #     G.update_boundries()
                #     G.set_radius(G.radius+10)


            screen.blit(color_txt,(3,screen_h-100))


            fps_array=fps_manager(clock,screen,fps_array)
            pygame.display.update()
            time.sleep(1)

        downcount=not downcount
        time.sleep(2)


    pygame.quit()
    exit()