# Task-manager-CLI with Priority Modification

The functions for the app have been written in `task.py` file.

### 1. Install Node.js

This project requires Node.js and npm to be implemented.

### 2. Create Create symbolic link to the executable file

#### On Windows

To create a symbolic link on Windows, you'll need to run the following command in either the Windows Command Prompt, or Windows Powershell **with administrator privileges**. 

**Command Prompt:**

```
> mklink task task.bat
```

**Powershell:**

```
> cmd /c mklink task task.bat
```

## Specification

1. The app can be run in the console with `./task`.

2. The app reads from and writes to task.txt for pending tasks along with its priority. 

3. It reads from and writes to completed.txt for completed tasks which includes the task name only.

4. Priority can be any integer _greater than_ or _equal to_ 1. 1 being the highest priority

5. If two task have the same priority, the task that was added first should be displayed first.

6. The files will always be sorted in order of the priority, ie, the task with the highest priority will be first item in the file.

## Usage

### 1. Help

Executing the command without any arguments, or with a single argument help prints the CLI usage.

```
$ .\task help
Usage :-
$ .\task add 2"hello world"    # Add a new item with priority 2 and text "hello world" to the list
$ .\task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ .\task deL INDEX            # Delete the incomplete item with the given index
$ .\task done INDEX           # Mark the incomplete item with the given index as complete
$ .\task help                 # Show usage
$ .\task report               # Statistics
```

### 2. List all pending items

Use the ls command to see all the items that are not yet complete, in ascending order of priority.

Example:

```
$ .\task ls
1. change light bulb [2]
2. water the plants [5]
```
index starts from 1, this is used to identify a particular task to complete or delete it.

### 3. Add a new item

```
$ .\task add 5"the thing i need to do"
Added task: "the thing i need to do" with priority 5
```
The task is added to the task.txt file in the following format.
   ```
   p task
   ```
   where `p` is the priority and `task` is the task description.
   The lower the number, the higher the priority.

### 4. Delete an item

Use the deL command to remove an item by its index.

```
$ .\task deL 3
Deleted item with index 3
```

Attempting to delete a non-existent item should display an error message.

```
$ .\task deL 5
Error: item with index 5 does not exist. Nothing deleted.
```

### 5. Mark a task as completed

Use the done command to mark an item as completed by its index.

```
$ .\task done 1
Marked item as done.
```
The task is added to the completed.txt in the following format. It is also removed from task.txt
   ```
   task
   ```
   where task is the task description.


Attempting to mark a non-existed item as completed will display an error message.

```
$ .\task done 5
Error: no incomplete item with index 5 exists.
```

### 6. Generate a report

Show the number of complete and incomplete items in the list.

```
$ .\task report
Pending : 2
1. this is a pending task [1]
2. this is a pending task with priority [4]

Completed : 3
1. completed task
2. another completed task
3. yet another completed task
```

## Run Automated Tests

The Jest module has been used to create test cases for the command line application. Run the following command to use the test file
```
$ npm test
```
----------------------------------------------------------------------------------------------------------------------------------
