'''!
Dummy page for ensuring clean exit.
'''
import pygame
import logging
import time, datetime
from page_templates import PageTemplate
from paths_and_utils import FULL_SCREEN_RES
from sys import exit

start_time_overall=time.time()

def wrap_up():
	'''Prints a nice goodbye message and elapsed time'''
	print ('\nLive long & prosper... bye!')
	t=elapsed_time(print_res=True)

def elapsed_time(print_res=False):
	'''Calculates total runtime from start of program'''
	end_time=round(time.time()-start_time_overall,2)
	elapsed_time=(datetime.timedelta(seconds=round(end_time)))
	if (print_res):
		logging.info (f'time elapsed: {elapsed_time} s')
	return elapsed_time

class ExitPage(PageTemplate):
	'''Faux page for clean exit'''
	def __init__(self,name):
		super().__init__(name)

	def next_frame(self,screen,curr_events,**kwargs):
		#  Disbale fullscreen
		if pygame.display.get_window_size()==FULL_SCREEN_RES:
			logging.info ('disabling full screen')
			pygame.display.toggle_fullscreen()

		wrap_up()
		pygame.quit()
		exit()