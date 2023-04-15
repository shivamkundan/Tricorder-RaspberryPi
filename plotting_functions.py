
from pygame import image
import numpy as np
from colors import BLACK

# ----- plotting libs ----- #
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from matplotlib import cm

# -------------- Plotting stuff -------------- #
COLOR = (0.75,0.75,0.75)
mpl.rcParams['font.size'] = 14
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

from fonts import *

# ==================== Plotting Functions ============================ #
def plot2img(fig,ax,canvas):
    ax.set_facecolor('black')
    # ax.patch.set_alpha(1)
    fig.patch.set_facecolor('black')
    # fig.patch.set_alpha(1)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    x=image.fromstring(raw_data, size, "RGB")
    x.set_colorkey(BLACK)
    # -
    return x

def pie_plot(fig,ax,canvas,color_list,pie_labels,curr_vals):
    ax.clear()
    COLOR = (0.75,0.75,0.75)
    mpl.rcParams['font.size'] = 12
    plt.style.use('dark_background')


    explode = (0.2, 0.2, 0.2, 0.2,0.2,0.2,0.2,0.2)
    patches,texts,autotexts=ax.pie(curr_vals,colors=color_list,
                                             labels=pie_labels,
                                             autopct='%1.1f%%',
                                             pctdistance=0.6,
                                             startangle=90,
                                             textprops={'color':'grey'},counterclock=False,
                                             radius=1.2,
                                             labeldistance=1.15,
                                             #explode=explode
                                    )

    others_pct=0
    for wedge,text,autotext in zip(patches,texts,autotexts):
        autotext.set_color('black')

    for item in texts:
        item.set_color('white')
        item.set_fontsize(12)

    return (plot2img(fig,ax,canvas))

def bar_plot(fig,ax,canvas,x_labels,color_list,curr_vals,ylabel=''):
    ax.clear()
    ax.cla()
    ax.set_xticks(np.arange(len(x_labels)))#, rotation=0,size=12)
    ax.set_xticklabels(x_labels, rotation=0,size=8)
    ax.set_ylabel(ylabel, fontsize=12)
    barWidth=0.4
    ax.bar(x_labels,curr_vals, align='center',color=color_list,width=barWidth)
    # plt.grid(True,color=COLOR, linestyle='-', linewidth=0.5)
    # plt.grid(axis='y',color=COLOR, linestyle='-', linewidth=0.5)

    return (plot2img(fig,ax,canvas))

def line_plot(fig,ax,canvas,color_list,x_array,array_dict):

    ax.clear()
    ax.cla()
    top=0
    i=0
    for name, color_array in array_dict.items():
        print (name,len(color_array))
        ax.plot(x_array,color_array,color=color_list[i])
        m=max(color_array)
        if top<m:
            top=m
        i+=1

    print('m,top:',m,top)
    ax.set_ylim(bottom=0,top=top)
    # plt.grid(True,color=COLOR, linestyle='-', linewidth=0.5)
    # plt.grid(axis='y',color=COLOR, linestyle='-', linewidth=0.5)

    return (plot2img(fig,ax,canvas))
