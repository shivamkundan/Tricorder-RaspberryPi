'''! @file fly_page_vars.py This file contains pre-computed vals for fly_page (to speed up execution). Source computation is in the comments at the end.'''

# ============================= abs params ============================= #

# ---------------------------------------- #
# vert gauge indicator params
INDICATOR_RECTS_COLOR	  =(0,0,0,127)
INDICATOR_SMALL_FONT_SIZE =15
INDICATOR_Y_DIFF		  =25
border_size      =6  # this is for alt and spd column drawings

# vert gauge size
ALTITUDE_RECT_WIDTH  =40
ALTITUDE_RECT_HEIGHT =300

# vert gauge pos
ALTITUDE_RECT_Y_POS  =180

# ---------------------------------------- #
# screen safe-area params (i.e. blank area)
START_Y =130
START_X =150
WIDTH   =530
HEIGHT  =450

# ---------------------------------------- #
# bottom grid params
info_row1_title=590
row_spacing    =55
info_col1      =170
col_increment  =170

# bottom grid text size
INFO_FONT_SIZE =20

# ---------------------------------------- #
# compass + enterprise heading indicator
HEADING_INDICATOR_POS =(340,445)
ENT_TOP_POS			  =(400,500)

# ---------------------------------------- #
# top grid icons position
WIND_SOCK_POS		  =(550,66)
SATELLITE_POS	      =(450,WIND_SOCK_POS[1])

# gps related text pos
LAT_LNG_TXT_SIZE =18
LAT_TXT_POS  	 =(390,WIND_SOCK_POS[1])
LONG_TXT_POS 	 =(390,WIND_SOCK_POS[1]+5+LAT_LNG_TXT_SIZE)


# ====================================================================== #
# Precomputed vals in alphabetical order
ALTITUDE_RECT_X_POS=        625
ALTITUDE_TXT_POS=           (620, 355)
ART_HORIZON_MARKINGS_POS=   (275, 215)
ENT_BACK_POS=               (347, 341)
ent_size_x=                 170
ent_size_y=                 94
h1=                         184
h2=                         224
h3=                         264
h4=                         304
h5=                         381
h6=                         421
h7=                         461
HUMID_ICON_POS=             (340, 590)
HUMID_TXT_POS=              (370, 600)
info_col2=                  340
info_col3=                  510
info_row1_value=            600
info_row2_title=            645
info_row2_value=            655
IR_ICON_POS=                (508, 645)
IR_TXT_POS=                 (548, 655)
LIGHT_ICON_POS=             (168, 645)
LIGHT_TXT_POS=              (208, 655)
MID_TXT_Y_POS=              355
PRESSURE_ICON_POS=          (510, 590)
PRESSURE_TXT_POS=           (540, 600)
SATELLITE_TXT_POS=          (505, 86)
SPEED_RECT_HEIGHT=          300
SPEED_RECT_WIDTH=           40
SPEED_RECT_X_POS=           155
SPEED_RECT_Y_POS=           180
SPEED_TXT_POS=              (150, 355)
TEMP_TXT_POS=               (200, 600)
THERM_POS=                  (170, 590)
UV_ICON_POS=                (338, 645)
UV_TXT_POS=                 (378, 655)
WIND_TXT_POS=               (605, 86)
x0=                         155
x1=                         625


# # ============================================================================= #
# ORIG RAW COMPUTATIONS

# # ============================================================================= #
# # ------ some stuff ------ #
# MID_TXT_Y_POS=START_Y+HEIGHT//2
# ALTITUDE_RECT_X_POS=START_X+475
# ALTITUDE_TXT_POS=(ALTITUDE_RECT_X_POS-5,MID_TXT_Y_POS)

# SPEED_RECT_X_POS=START_X+5
# SPEED_RECT_Y_POS=ALTITUDE_RECT_Y_POS
# SPEED_TXT_POS=(SPEED_RECT_X_POS-5,MID_TXT_Y_POS)
# SPEED_RECT_WIDTH=ALTITUDE_RECT_WIDTH
# SPEED_RECT_HEIGHT=ALTITUDE_RECT_HEIGHT

# h1=ALTITUDE_RECT_Y_POS+4
# h2=h1+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE
# h3=h2+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE
# h4=h3+INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE

# h7=ALTITUDE_RECT_Y_POS+ALTITUDE_RECT_HEIGHT-INDICATOR_SMALL_FONT_SIZE-4
# h6=h7-(INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE)
# h5=h6-(INDICATOR_Y_DIFF+INDICATOR_SMALL_FONT_SIZE)

# x0=SPEED_RECT_X_POS
# x1=ALTITUDE_RECT_X_POS

# # ------ some pos calcs ------ #
# ART_HORIZON_MARKINGS_POS=(START_X+WIDTH//2-ART_HORIZON_MARKINGS.get_rect().size[0]//2,START_Y+HEIGHT//2-ART_HORIZON_MARKINGS.get_rect().size[1]//2)
# WIND_TXT_POS=(WIND_SOCK_POS[0]+50+5,WIND_SOCK_POS[1]+20)
# SATELLITE_TXT_POS=(SATELLITE_POS[0]+50+5,SATELLITE_POS[1]+20)

# info_row1_value=info_row1_title+10

# info_row2_title=info_row1_title+row_spacing
# info_row2_value=info_row2_title+10


# info_col2=info_col1+col_increment
# info_col3=info_col2+col_increment

# # ------ thermometer icon ------ #
# THERM_POS=(info_col1,info_row1_title)
# TEMP_TXT_POS=(info_col1+30,info_row1_value)

# # ------ humidity icon ------ #
# HUMID_ICON_POS=(info_col2,info_row1_title)
# HUMID_TXT_POS=(info_col2+30,info_row1_value)

# # ------ pressure icon ------ #
# PRESSURE_ICON_POS=(info_col3,info_row1_title)
# PRESSURE_TXT_POS=(info_col3+30,info_row1_value)

# # ------ light icon ------ #
# LIGHT_ICON_POS=(info_col1-2,info_row2_title)
# LIGHT_TXT_POS=(info_col1+38,info_row2_value)

# # ------ UV icon ------ #
# UV_ICON_POS=(info_col2-2,info_row2_title)
# UV_TXT_POS=(info_col2+38,info_row2_value)

# # ------ IR icon ------ #
# IR_ICON_POS=(info_col3-2,info_row2_title)
# IR_TXT_POS=(info_col3+38,info_row2_value)

# # ------ ent back ------ #
# ent_size_x=ENT_BACK_TRACE.get_rect().size[0]
# ent_size_y=ENT_BACK_TRACE.get_rect().size[1]
# ENT_BACK_TRACE=pygame.transform.scale(ENT_BACK_TRACE, (int(round(ent_size_x*0.8,0)), int(round(ent_size_y*0.8,0))))
# ENT_BACK_POS=(START_X+WIDTH//2-ENT_BACK_TRACE.get_rect().size[0]//2,START_Y+HEIGHT//2-ENT_BACK_TRACE.get_rect().size[1]//2+23)
# # ============================================================================= #

# calculated_val_names=[
# "MID_TXT_Y_POS", "ALTITUDE_RECT_X_POS", "ALTITUDE_TXT_POS", "SPEED_RECT_X_POS", "SPEED_RECT_Y_POS", "SPEED_TXT_POS", \
# "SPEED_RECT_WIDTH", "SPEED_RECT_HEIGHT", "h1", "h2", "h3", "h4", "h7", "h6", "h5", "x0", "x1", "ART_HORIZON_MARKINGS_POS", "WIND_TXT_POS", \
# "SATELLITE_TXT_POS", "info_row1_value", "info_row2_title", "info_row2_value", "info_col2", "info_col3", "THERM_POS", "TEMP_TXT_POS", \
# "HUMID_ICON_POS", "HUMID_TXT_POS", "PRESSURE_ICON_POS", "PRESSURE_TXT_POS", "LIGHT_ICON_POS", "LIGHT_TXT_POS", "UV_ICON_POS", "UV_TXT_POS", \
# "IR_ICON_POS", "IR_TXT_POS", "ent_size_x", "ent_size_y", "ENT_BACK_POS"
# ]

# calculated_vals=[
# MID_TXT_Y_POS, ALTITUDE_RECT_X_POS, ALTITUDE_TXT_POS, SPEED_RECT_X_POS, SPEED_RECT_Y_POS, SPEED_TXT_POS, \
# SPEED_RECT_WIDTH, SPEED_RECT_HEIGHT, h1, h2, h3, h4, h7, h6, h5, x0, x1, ART_HORIZON_MARKINGS_POS, WIND_TXT_POS, \
# SATELLITE_TXT_POS, info_row1_value, info_row2_title, info_row2_value, info_col2, info_col3, THERM_POS, TEMP_TXT_POS, \
# HUMID_ICON_POS, HUMID_TXT_POS, PRESSURE_ICON_POS, PRESSURE_TXT_POS, LIGHT_ICON_POS, LIGHT_TXT_POS, UV_ICON_POS, UV_TXT_POS, \
# IR_ICON_POS, IR_TXT_POS, ent_size_x, ent_size_y, ENT_BACK_POS
# ]

# for name,var in zip(calculated_val_names,calculated_vals):
#     print (f"{name}= \t\t{var}")

# print (f"len:{len(calculated_val_names)}, {len(calculated_vals)}")