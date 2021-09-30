#!/usr/bin/env python3
"""
A command line todoist application. There's already one of these, but this one is simple.
"""

__author__ = "Gavin McCormack"
__version__ = "1.0.0"
__license__ = "MIT"


import todoist
import inspect
import pdb
import sys
import os

def toddyboy(): # Functionwrap to make load_entry_point happy
	# Ve like ze variables long yes. Makes us feel like the terminator yes.
	API_KEY_ENVIRONMENT_VARIABLE_NAME='TOD_API_KEY'
	TARGET_PROJECT_ENVIRONMENT_VARIABLE_NAME='TOD_TARG_PROJECT'

	API_KEY = os.environ.get(API_KEY_ENVIRONMENT_VARIABLE_NAME)
	TARGET_PROJECT = int(os.environ.get(TARGET_PROJECT_ENVIRONMENT_VARIABLE_NAME))

	# Setup if not run before
	# Having an active configuration seems like overkill
	if not API_KEY or not TARGET_PROJECT:
		print("Please set environment variables TOD_API_KEY and TOD_TARG_PROJECT")
		print("Or check they are available for the executing user")
		exit()


	mode, task = "", ""


	# Basic "You done wrong" feedback
	# Because you did do wrong, din't you.
	if len(sys.argv) > 1:
		mode = sys.argv[1]

	# Thou hast failed at the first hurdle
	if sys.argv[1] not in ['add','del','list']:
		print("Please use one of ( add, del, list ) as the first parameter")
		exit()

	# Ye, mightier than yer peers have been brought low by the trickery of the second
	if len(sys.argv) > 2 and sys.argv[1] != "list":
		task = sys.argv[2]
	elif sys.argv[1] == "add":
		print("Please provide a string for the task title")
		exit()
	elif sys.argv[1] == "del":
		print("Please provide an integer, or comma separated list in the second position")
		exit()


	api = todoist.api.TodoistAPI(API_KEY)
	api.sync()

	def tod_list():
		""" It lists tasks innit """
		print('-------------')

		print('https://todoist.com/app/project/%s' % TARGET_PROJECT)
		print('-------------\n\n\n')

		## Projects and IDs
		PRINT_PROJECT_IDS = False
		if PRINT_PROJECT_IDS:
			for project in api.state['projects']:
				print(project['name'] + ": " + str(project['id']))

		TARGET_PROJECT_NAME = "Agenda" # NB: implement
		task_no = 0 # Number of tasks that are valid in API ordered. 
		for item in api.state['items']:
			if item['project_id'] == int(TARGET_PROJECT):
				in_history = item['in_history'] == 0
				is_deleted = item['is_deleted'] == 0
				if in_history and is_deleted:
					task_no += 1
					print('\u001b[32m[%s] \u001b[0m- %s \n' % (task_no, item['content'] ))


		print('\n\n\n-------------\n\n\n')

	if mode == "list":
		tod_list()


	## Add
	if mode == "add":
		print('-------------')
		print('Adding task...\n')
		print('\u001b[32m %s\u001b[0m- \n' % task)

		task1 = api.items.add(task, project_id=TARGET_PROJECT)
		api.commit()
		print("... Done")
		print('-------------\n\n\n')
		tod_list()



	## Delete
	if sys.argv[1] == "del":
		print('-------------')
		print("Attempting delete...")
		if "," in task:
			target_task_no = [int(x) for x in task.split(",") ] # Cumbersome
		else:
			target_task_no = [int(task)]
		task_no = 0 # Number of tasks that are valid in API order. 
		success = False
		deleted_tasks = [] # NB: imp
		for item in api.state['items']:
			if item['project_id'] == TARGET_PROJECT:
				in_history = item['in_history'] == 0
				is_deleted = item['is_deleted'] == 0

				if in_history and is_deleted:
					task_no += 1
					if task_no in target_task_no:
						deleted_tasks += [task_no]
						item.complete()
						api.commit()
						success = True
		if success:
			print(deleted_tasks)
			print("... Done")
			print('-------------\n\n\n')
		else:
			print("... Did not find task to delete")
		tod_list()


if __name__ == "__main__":
	toddyboy()