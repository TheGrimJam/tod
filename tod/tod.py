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
from config_settings import TARGET_PROJECT, API_KEY



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

	print('https://todoist.com/app/project/2253370271')
	print('-------------\n\n\n')

	## Projects and IDs
	PRINT_PROJECT_IDS = False
	if PRINT_PROJECT_IDS:
		for project in api.state['projects']:
			print(project['name'] + ": " + str(project['id']))

	TARGET_PROJECT = "Agenda" # NB: implement
	task_no = 0 # Number of tasks that are valid in API ordered. 
	for item in api.state['items']:
		if item['project_id'] == 2253370271:
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
		if item['project_id'] == 2253370271:
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

