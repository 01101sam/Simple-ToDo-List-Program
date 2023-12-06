- Main Menu

# Functions

- [x] add
- [x] list
- [x] mark
- [x] today
    - [x] tag
    - [x] mark
    - [x] untag
    - [x] return
- [x] about
- [x] quit

## Bonus

- [x] list_completed
- [x] remove
- [x] move
- [x] edit
- [x] help (Included in `Command` framework)
    - [x] search (Included in `Command` framework)
- [x] version (Included in `Command` framework)
- [x] clear

---

# Banner

```markdown
+-----------+
| Main menu |
+-----------+
```

# Usage

## Add

### Example

```markdown
+------------------------+
| Main menu -> Add to-do |
+------------------------+

Please input new task: Buy milk
Added task: 'Buy milk'
Press Enter to return.
```

### Error example

```markdown
+------------------------+
| Main menu -> Add to-do |
+------------------------+

Please input new task:
Task should not be empty. Input again.
Please input new task:
Task should not be empty. Input again.
Please input new task: Finish project
Added task: 'Finish project'
Press Enter to return.
```

## List

### Example

```markdown
+--------------------------+
| Main menu -> List to-dos |
+--------------------------+
You have 0 to-dos:
No to-dos outstanding.

Press Enter to return.
```

### Have item example

```markdown
+--------------------------+
| Main menu -> List to-dos |
+--------------------------+
You have 2 to-dos:
0: Buy Milk
1: Finish project

Press Enter to return.
```

## Mark

### Example

```markdown
+-----------------------------+
| Main menu -> Mark Completed |
+-----------------------------+
You have 0 to-dos:
No to-dos outstanding.

Nothing to mark, return to main menu.
Press Enter to return.
```

```markdown
+-----------------------------+
| Main menu -> Mark Completed |
+-----------------------------+
You have 2 to-dos:
0: Buy milk
1: Finish project

Please input completed task number: 0
Completed task #0: 'Buy milk'
Press Enter to return.
```

### Error example

```markdown
+-----------------------------+
| Main menu -> Mark Completed |
+-----------------------------+
You have 2 to-dos:
0: Buy milk
1: Finish project

Please input completed task number: ABC
Error. Expected a number input.
Press Enter to return.
```

```markdown
+-----------------------------+
| Main menu -> Mark Completed |
+-----------------------------+
You have 2 to-dos:
0: Buy milk
1: Finish project

Please input completed task number: 3
Error. Out of range task number.
Press Enter to return.
```

## Today

### Example

> Note: There's a sub-menu

- tag
- mark
- untag
- return

```markdown
+------------------------------+
| Main menu -> Tasks for today |
+------------------------------+
You have 0 tasks for today:
No task is assigned for today.

Command options: ['tag', 'mark', 'untag', 'return'].
Please input your command: help
Invalid command. Please input again.
Please input your command: quit
Invalid command. Please input again.
Please input your command: tag
```

```markdown
+------------------------------+
| Main menu -> Tasks for today |
+------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study for exam

Command options: ['tag', 'mark', 'untag', 'return'].
```

### Tag

```markdown
+--------------------------------------------+
| Main menu -> Tasks for today -> Tag a task |
+--------------------------------------------+
Potential task for tagging.
0: Buy milk
1: Finish project
2: Study notes

Please input task number to tag: 1
Added task #1 into today list.
```

#### Error example

```markdown
+--------------------------------------------+
| Main menu -> Tasks for today -> Tag a task |
+--------------------------------------------+
Potential task for tagging.
0: Buy milk
1: Finish project
2: Study notes

Please input task number to tag: ABC
Error. Expected a number input.
```

```markdown
+--------------------------------------------+
| Main menu -> Tasks for today -> Tag a task |
+--------------------------------------------+
Potential task for tagging.
0: Buy milk
1: Finish project
2: Study notes

Please input task number to tag: -1
Error. Expected a number input.
```

```markdown
+--------------------------------------------+
| Main menu -> Tasks for today -> Tag a task |
+--------------------------------------------+
Potential task for tagging.
0: Buy milk
1: Finish project
2: Study notes

Please input task number to tag: 99
Error. Out of range task number.
```

#### Dupe example

```markdown
+--------------------------------------------+
| Main menu -> Tasks for today -> Tag a task |
+--------------------------------------------+
Potential task for tagging.
0: Buy milk
2: Study notes

Please input task number to tag: 1
Error. The task is already in the today list.
```

### Un Tag

```markdown
+----------------------------------------------+
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 0 tasks for today:
No task is assigned for today.

No task to untag.
```

```markdown
+----------------------------------------------+
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input task number to untag: 0
Removed task #0 in today list.
```

#### Error example

```markdown
+----------------------------------------------+
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input task number to untag: ABC
Error. Expected a number input.
```

```markdown
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input task number to untag: -1
Error. Expected a number input.
```

```markdown
+----------------------------------------------+
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input task number to untag: 99
Error. Task number out of range.
```

```markdown
+----------------------------------------------+
| Main menu -> Tasks for today -> Untag a task |
+----------------------------------------------+
You have 1 tasks for today:
2: Study notes

Please input task number to untag: 0
Error. The task is not in the today list.
```

### Mark

```markdown
+---------------------------------------------------+
| Main menu -> Tasks for today -> Mark a today task |
+---------------------------------------------------+
You have 0 tasks for today:
No task is assigned for today.

Nothing to mark, return to today menu.
```

```markdown
+---------------------------------------------------+
| Main menu -> Tasks for today -> Mark a today task |
+---------------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input completed task number: 0
Completed task #0: 'Buy milk'.
```

#### Error example

```markdown
+---------------------------------------------------+
| Main menu -> Tasks for today -> Mark a today task |
+---------------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input completed task number: ABC
Error. Expected a number input.
Press Enter to return.
```

```markdown
+---------------------------------------------------+
| Main menu -> Tasks for today -> Mark a today task |
+---------------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input completed task number: 3
Error. Out of range task number.
Press Enter to return.
```

```markdown
+---------------------------------------------------+
| Main menu -> Tasks for today -> Mark a today task |
+---------------------------------------------------+
You have 2 tasks for today:
0: Buy milk
2: Study notes

Please input completed task number: 1
Error. The task is not in the today list.
```

### Return

```markdown
+------------------------------+
| Main menu -> Tasks for today |
+------------------------------+
You have 1 tasks for today:
1: Study notes

Command options: ['tag', 'mark', 'untag', 'return'].
Please input your command: return

Return to main menu.
Press Enter to return.
```

## About

When the user enters ‘about’ in the command menu, a detailed introduction of the application should be displayed.
\
The introduction should include:

1. Detail instructions about how to use the app.
2. Full name of the programmer.
3. Student ID of the programmer.

## Quit

```markdown
Goodbye, {username}. You have {} to-dos and completed {} tasks.
```
