import json
import os
import sys


GITTER_TASKS_PATH = os.path.expanduser('~/gitter-tasks.json')
MAIN_BRANCH = 'master'


def main():
   argv = sys.argv[1:]
   
   command = argv[0]
   args = argv[1:]
   
   if command == '--help':
      print_help()
      
   else: # other command
      if command == 'register':
         tasks = json_read()
          
         task_name, task_id = args
         if task_name in tasks:
            print('Sorry, task with name "' + task_name + '" already exist.')
         else:
            tasks['tasks'][task_name] = task_id
            print('Task "' + task_name + '" regestered successfully.')
            
         last_name_save(task_name, tasks)
         json_write(tasks)

      elif command == 'purge':
         tasks = json_read()
          
         task_name = args[0]
         task_name = normalize_task_name(task_name)
         tasks['tasks'].pop(task_name)
            
         last_name_save(task_name)
         json_write(tasks)
         print('Task "' + task_name + '" removed.')

      elif command == 'list':
         tasks = json_read()
         
         print('Last task: ' + str(tasks['last']) + '\n')
         for task_name in tasks['tasks']:
            print(str(task_name) + ' == ' + str(tasks['tasks'][task_name]))
         
         if not tasks['tasks']:
            print('No tasks saved.')
     
      elif command == 'go':
         task_name = args[0]
         task_name = normalize_task_name(task_name)
         last_name_save(task_name)
         task_id = get_task_id(task_name)
         os.system('git checkout ' + get_branch_name(task_name, task_id))
         
      elif command == 'gb':
         task_name = args[0]
         task_name = normalize_task_name(task_name)
         last_name_save(task_name)
         task_id = get_task_id(task_name)
         os.system('git branch ' + get_branch_name(task_name, task_id))
         
      elif command == 'commit':
         task_name = args[0]
         task_name = normalize_task_name(task_name)
         last_name_save(task_name)
         task_id = get_task_id(task_name)
         message = args[1]
         os.system('git commit -m "' + get_commit_name(task_name, task_id) + message + '"')
         
      elif command == 'merge':
         task_name = args[0]
         task_name = normalize_task_name(task_name)
         last_name_save(task_name)
         task_id = get_task_id(task_name)
         os.system('git checkout '+MAIN_BRANCH+' && git merge --no-ff ' + get_branch_name(task_name, task_id))
       
       
def print_help():
  print("""
Run `python gitter.py {command}`, where command:

   # MANAGE
   register {task_name} {task_id} - binds task id to task name, means register new task
   purge {task_name} -------------- delete registration data about this task
   list --------------------------- list all saved tasks and last task
   
   # BRANCH
   go {task_name} ----------------- git checkout to task branch
   gb {task_name} ----------------- create new branch (git branch) for task
   
   # COMMITS
   commit {task_name} {message} --- creates new commit for task
   merge {task_name} -------------- git checkout to main branch, and then git merge task with --no-ff param
   
   # INFO
   Tasks are saved in """ + GITTER_TASKS_PATH + """
            """)
  

def json_write(data):
   if not os.path.exists(GITTER_TASKS_PATH):
      tasks_file = open(GITTER_TASKS_PATH, 'w+')
      tasks_file.write('{}')
      tasks_file.close()
      json_empty()
      
   tasks_file = open(GITTER_TASKS_PATH, 'r+')
   # clear file content
   tasks_file.close()
   json_empty()
   
   tasks_file = open(GITTER_TASKS_PATH, 'r+')
   tasks_file.write(json.dumps(data))
   tasks_file.close()
   
def json_read():
   if not os.path.exists(GITTER_TASKS_PATH):
      json_empty()

   tasks_file = open(GITTER_TASKS_PATH, 'r+')
   tasks_text = tasks_file.read()
   tasks = json.loads(tasks_text)
 
   # clear file content
   tasks_file.close()
   json_empty()
   
   tasks_file = open(GITTER_TASKS_PATH, 'r+')
   tasks_file.write(json.dumps(tasks))
   tasks_file.close()
   
   return tasks

def json_empty():
   tasks_file = open(GITTER_TASKS_PATH, 'w+')
   #tasks_file.write('{}')
   tasks_file.write('{"tasks":{},"last":""}')
   tasks_file.close()
   
def last_name_save(task_name, tasks=None):
   if task_name != '@':
      if not tasks:
         tasks = json_read()
      tasks['last'] = task_name
      json_write(tasks)


def normalize_task_name(task_name):
   tasks_state = json_read()
   tasks = tasks_state['tasks']
   
   if task_name == '@':
      task_name = tasks_state['last']
   
   if task_name in tasks:
      return task_name
   else:
      print('Task "' + task_name + '" not registered yet.')
      quit()
   
  
def get_task_id(task_name):
   tasks_state = json_read()
   tasks = tasks_state['tasks']
   
   if task_name == '@':
      task_name = tasks_state['last']
   
   if task_name in tasks:
      return tasks[task_name]
   else:
      print('Task "' + task_name + '" not registered yet.')
      quit()
      

def get_branch_name(task_name, task_id):
   return 'rm' + task_id + '_' + task_name
   
def get_commit_name(task_name, task_id):
   return '#' + task_id + ' - '
   
      

main()