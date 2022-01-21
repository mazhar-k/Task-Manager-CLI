#! usr/bin/env python

# modules required
import os
from os import dup2
from pathlib import Path
import sys
import datetime

# Create file paths
base_dir = os.getcwd()
task_path = os.path.join(base_dir, "task.txt")
completed_path = os.path.join(base_dir, "completed.txt")

# help function
def help():
    usage = '''Usage :-
$ .\task add 2 hello world     # Add a new item with priority 2 and text "hello world" to the list
$ .\task ls                    # Show incomplete priority list items sorted by priority in ascending order
$ .\task del NUMBER   # Delete the incomplete item with the given priority number
$ .\task done NUMBER  # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ .\task help                  # Show usage
$ .\task report                # Statistics`'''
    sys.stdout.buffer.write(usage.encode('utf8'))


# function to add task in the task list
def add(arg_list):
    # Check if priority is a 2 digit number and divide arg_list accordingly
    p, task = [arg_list[:2], arg_list[2:]] if arg_list[1].isdigit() else [arg_list[0], arg_list[1:]]
    
    # Write priority and task string to task.txt file
    f = open(task_path, 'a')
    f.write(p)
    f.write(" ")
    f.write(task)
    f.write('\n')
    f.close()
    task = '"'+task+'"'
    print(f"Added task: {task} with priority {p}")

    # Function to update and sort dictionary of pending tasks with priorities
    dsort  = task_dict()

    f = open(task_path, 'a')
    f.seek(0)
    f.truncate()
    for pr, tk in dsort.items():
        # Code if 2 tasks have same priority
        if type(tk) == list:   
            for t in tk:
                f.write(str(pr))
                f.write(" ")
                f.write(t)
                f.write('\n')
        else:
            f.write(str(pr))
            f.write(" ")
            f.write(tk)
            f.write('\n')
    f.close()

# Function to print the list of tasks
def ls():
    
    try:
        # Update and sort pending task dictionary
        d1 = task_dict()

        # print index, task and priority for each task
        for i, (p, tk) in enumerate(d1.items()):
            if type(tk) == list:   
                for t in tk:
                    print(f"{i+1}. {t} [{p}]")
                    print("\n")
            else:
                sys.stdout.buffer.write(f"{i+1}. {tk} [{p}]".encode('utf8'))
                sys.stdout.buffer.write("\n".encode('utf8'))

    except Exception as e:
        raise e

    else:
        # Check if file is empty
        if os.stat(task_path).st_size == 0:
            sys.stdout.buffer.write("There are no pending tasks!".encode("utf8"))


# Function to mark a task as completed
def done(arg_list):
    index = arg_list[0]

    try:
        # Update and sort pending task dictionary
        dsort = task_dict()

        index = int(index)

        # Create dictionary with index and task strings fron sorted dictionary
        key_list = [x for x in range(1, len(dsort)+1)]
        d2 = dict(zip(key_list, dsort.values()))

        # Add task to completed.txt
        f = open(completed_path, 'a')
        task = d2[index]
        f.write(task)
        f.write('\n')
        f.close()
        print("Marked item as done.")

        # delete task from task.txt
        with open(task_path, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            if index > len(d2):
                d2[index] # raise exception
            else:
                f.truncate()  
                for line in lines:
                    if line[2:].strip('\n') != d2[index]:
                        f.write(line)
    except:
        sys.stdout.buffer.write(f"Error: no incomplete item with index #{index} exists.".encode("utf8"))

# Function to create report
def report():

    try:
        # Update and sort dictionary
        dsort = task_dict()

        # Output number of pending tasks and list them
        sys.stdout.buffer.write(f'Pending : {len(dsort)}\n'.encode("utf8"))
        for i, (p, t) in enumerate(dsort.items()):
            sys.stdout.buffer.write(f"{i+1}. {t} [{p}]\n".encode("utf8"))
        
        sys.stdout.buffer.write("\n".encode("utf8"))

        # Create the file before read mode
        fle = Path(completed_path)
        fle.touch(exist_ok=True)

        # Update dictionary of completed tasks with indexes
        f = open(completed_path, 'r')
        for i, line in enumerate(f):
            line = line.strip('\n')
            completed_dict.update({(i+1): line})

        # Output number of completed tasks and list them
        sys.stdout.buffer.write(f'Completed : {len(completed_dict)}\n'.encode("utf8"))
        for i,(p, t) in enumerate(completed_dict.items()):
            sys.stdout.buffer.write(f"{i+1}. {t}\n".encode("utf8"))

    except Exception as e:
        raise e

def deL(arg_list):
    index = arg_list[0]
    
    try:
        dsort = task_dict()
        index = int(index)

        # Create dictionary with index and task strings fron sorted dictionary
        key_list = [x for x in range(1, len(dsort)+1)]
        d2 = dict(zip(key_list, dsort.values()))

        with open(task_path, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            if index > len(d2):
                d2[index] # raise exception
            else:
                f.truncate()  
                for line in lines:
                    # Check if priority is a 2 digit number and divide line accordingly
                    tk = line[3:] if line[1].isdigit() else line[2:]

                    if tk.strip('\n') != d2[index]: 
                        f.write(line)
        
        print(f"Deleted task #{index}")

    except Exception as e:
        print(f"Error: task with index #{index} does not exist. Nothing deleted.")


# Utility function used to create, update and sort a dictionary of tasks and priority
def task_dict():

    try:

        priority = []
        tasks = []
        # dictionary for tasks with same priority
        same_pr = []

        # Create the file before read mode
        fle = Path(task_path)
        fle.touch(exist_ok=True)
        
        f = open(task_path, 'r')
        for i, line in enumerate(f):
            line = line.strip('\n')

            prt, tk = [line[:2], line[3:]] if line[1].isdigit() else [line[0], line[2:]]

            priority.append(prt)
            tasks.append(tk)
            pending_dict.update({int(prt): tk})         

        # Solution for Same Priority in tasks
        for i, p in enumerate(priority):
            if priority.count(p) > 1:
                same_pr.append(tasks[i])
                pending_dict.update({int(p): same_pr})

        return dict(sorted(pending_dict.items()))

    except Exception as e:
        sys.stdout.buffer.write("There are no pending tasks!".encode("utf8"))

# Main Program
if __name__ == '__main__':
    try:
        pending_dict = {}
        completed_dict = {}
        args = sys.argv

        # Handle errors for incomplete arguments

        if(args[1] == 'add' and len(args[2:]) == 0):
            sys.stdout.buffer.write(
                "Error: Missing tasks string. Nothing added!".encode('utf8')
            )

        elif(args[1] == 'done' and len(args[2:]) == 0):
            sys.stdout.buffer.write(
                "Error: Missing NUMBER for marking tasks as done.".encode('utf8')
            )

        elif(args[1] == 'deL' and len(args[2:]) == 0):
            sys.stdout.buffer.write(
                "Error: Missing NUMBER for deleting tasks.".encode('utf8')
            )
        else:
            # Call respective function
            globals()[args[1]](*args[2:])

    except Exception as e:
        help()
