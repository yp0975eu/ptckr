# Project Time Tracker

Required :
- Python 3
- Sqlite3


How A Project is Organized:
- Project
- - Task
- - - Entry

###How to get started:
1. To create a project use the `init` command from the root directory
    This initializes a database in your root directory.
2. Create a task with `create <taskname>`
3. Select the task with `select <taskname>|<task_id>`
4. See all tasks with `show -t`
5. Start tracking time with `start`
6. Stop tracking time with `stop`
7. Show all entries in a task with `show -e`
8. Check tracking status with `status`

# Features Not Implemented
- [ ] Implement deleting of tasks and cascade deletion of entries
- [ ] Implement deleting of entries
- [ ] Implement updating a completed entry's start, stop, description 
- [ ] Printing report for project, breakdowns by task
