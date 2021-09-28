#!/usr/bin/env python3
"""
A command line todoist application. There's already one of these, but this one is simple.
"""

__author__ = "Gavin McCormack"
__version__ = "0.1.0"
__license__ = "MIT"


import todoist
import inspect
import pdb
import sys
import pathlib
import os


# Ve like ze variables long yes. Makes us feel like the terminator yes.
API_KEY_ENVIRONMENT_VARIABLE_NAME='TOD_API_KEY'
TARGET_PROJECT_ENVIRONMENT_VARIABLE_NAME='TOD_TARG_PROJECT'

API_KEY = os.environ.get(API_KEY_ENVIRONMENT_VARIABLE_NAME)
TARGET_PROJECT = os.environ.get(TARGET_PROJECT_ENVIRONMENT_VARIABLE_NAME)

print(API_KEY, TARGET_PROJECT)

# Setup if not run before
if not API_KEY or TARGET_PROJECT:
	print("Please navigate to -wherever you get a todoist api key- and input it here:")
	API_KEY = input()
	print("Please input project ID:")
	TARGET_PROJECT = input()
	os.environ[API_KEY_ENVIRONMENT_VARIABLE_NAME] = API_KEY
	os.environ[TARGET_PROJECT_ENVIRONMENT_VARIABLE_NAME] = TARGET_PROJECT


mode, task = "", ""

if len(sys.argv) > 0:
	mode = sys.argv[1]
else:
	print("Please provide an 'add' or 'del' parameter in the first position")
if len(sys.argv) > 1 and sys.argv[1] != "list":
	print(sys.argv[2])
	task = sys.argv[2]
elif sys.argv[1] == "list":
	pass
else:
	print("Please provide a string for the task title")

if not ( mode or task ):
	print("Exiting")
	exit()

api = todoist.api.TodoistAPI(API_KEY)
api.sync()

if mode == "list":
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
		if item['project_id'] == TARGET_PROJECT:
			in_history = item['in_history'] == 0
			is_deleted = item['is_deleted'] == 0
			if in_history and is_deleted:
				task_no += 1
				print('\u001b[32m[%s] \u001b[0m- %s \n' % (task_no, item['content'] ))


	print('\n\n\n-------------\n\n\n')



## Add
if mode == "add":
	print('-------------')
	print('Adding task...\n')
	print('\u001b[32m %s\u001b[0m- \n' % task)

	task1 = api.items.add(task, project_id=PROJECT_ID)
	api.commit()
	print("... Done")
	print('-------------\n\n\n')



## Delete
if sys.argv[1] == "del":
	print("Trying delete task...")
	target_task_no = int(task)
	task_no = 0 # Number of tasks that are valid in API order. 
	success = False
	for item in api.state['items']:
		#print(task_no, target_task_no)
		if item['project_id'] == TARGET_PROJECT:
			in_history = item['in_history'] == 0
			is_deleted = item['is_deleted'] == 0
			if in_history and is_deleted:
				task_no += 1
				if target_task_no == task_no:					
					item.complete()
					api.commit()
					success = True
	if success:
		print("... Done")
		print('-------------\n\n\n')
	else:
		print("... Did not find task to delete")

