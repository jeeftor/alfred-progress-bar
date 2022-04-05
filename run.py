# -*- coding: utf-8 -*-

import sys

from workflow import Workflow3
from workflow.background import is_running, run_in_background

import os


def string_from_count(c):
	"""Returns a fancy string to show in the workflow from the count item"""

	# Python 2 Versions
	# blue  = "\\U0001F535\\U0000FE0F"
	# white = "\\U000026AA\\U0000FE0F"
	# black = "\\U000026AB\\U0000FE0F"
	# big_black	   = "\\U00002B1B\\U0000FE0F"
	# big_white	   = "\\U00002B1C\\U0000FE0F"
	# white_in_black = "\\U0001F532\\U0000FE0F"
	# black_in_white = "\\U0001F533\\U0000FE0F"


	blue  = u"\U0001F535\U0000FE0F"
	white = u"\U000026AA\U0000FE0F"
	black = u"\U000026AB\U0000FE0F"
	big_black	   = u"\U00002B1B\U0000FE0F"
	big_white	   = u"\U00002B1C\U0000FE0F"
	white_in_black = u"\U0001F532\U0000FE0F"
	black_in_white = u"\U0001F533\U0000FE0F"


	ret = black_in_white + black + black + black + black + big_white + black + black + black + black + black

	mod = 2 * (5 - (c % 5))

	return ret[mod:][0:10]

def string_from_percent(current_value, number_of_steps = 10, max_value = 100):


	blue  = u"\U0001F535\U0000FE0F"
	white = u"\U000026AA\U0000FE0F"
	black = u"\U000026AB\U0000FE0F"

	# steps_done = int(float(int(current_value)) / max_value * number_of_steps)
	steps_left = max(0,int(float(int(max_value - current_value)) / max_value  * number_of_steps))
	steps_done = max(0,number_of_steps - steps_left)

	done_color = blue
	not_done_color = white

	ret = done_color * steps_done + not_done_color * steps_left + " {} {}".format(steps_left, steps_done)
	return ret

def main(wf):

	#Check if first time
	try:
		count = int(os.environ['count'])
		first_time = False
	except:
		count = 0
		first_time = True
	

	if first_time:

		wf.rerun = 0.5
		wf.add_item('Starting background process')
		run_in_background('bg', ['python3', wf.workflowfile('bg.py')])

	else:

		if is_running('bg'):
			"""Update status"""
			wf.rerun = 0.5
			wf.add_item("Background process is running",string_from_count(count))
			wf.add_item("Count " + str(count) + "Out of 20", string_from_percent(count, number_of_steps = 10, max_value = 7) )
			count += 1
		else:
			"""Last case"""
			data = wf.stored_data('bg_result').decode()

			wf.add_item("Process Finished","Result: " + data, icon="Checkmark.png")


	wf.setvar('count',count)

	wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow3()
	log = wf.logger
	sys.exit(wf.run(main))