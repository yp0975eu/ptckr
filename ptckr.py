import sys
from tables import Table
from tasks import *
from status import Status
from entry import *

FILENAME = 0
COMMAND = 1
FIRST_ARG = 2
SECOND_ARG = 3


class Menu:
    top_menu = (
        {'command': "init", "desc": '\tinit\n\t\tDef: Initializes a project in current directory'},
        {'command': "help", "desc": '\thelp\n\t\tDef: Shows this help menu'},
        {'command': 'create', 'desc': '\tcreate <task>\n\t\tDef: Creates a new task'},
        {'command': 'select', 'desc': '\tselect <task>\n\t\tDef: Select a task to track or remove a tracking task'},
        {'command': 'status', 'desc': '\tstatus\n\t\tDef: Shows current selected task'},
        {'command': 'start', 'desc': '\tstart\n\t\tDef: Starts tracking time'},
        {'command': 'stop', 'desc': '\tstop\n\t\tDef: Stops tracking time'},
        {'command': "show", "desc":
            '\tshow -t|-e\n\t\tDef: -e shows entries for currently selected task. Use -t to view all tasks'}
    )

    project_menu_options = ['Start Time', 'End Time', 'View Entries ']

    @staticmethod
    def show_help():
        print('\n{0} : {1}'.format('command'.ljust(10), 'usage'))
        print('-----------------------------------------------')
        for option in Menu.top_menu:
            print('{0} : {1}\n'.format(option['command'].ljust(10), option['desc']))
        quit()


if __name__ == '__main__':

    # The Database file is created each time Db is initialized.
    # if filename doesn't exist
    # calling init method sets up the tables.py

    if len(sys.argv) >= 2:

        if sys.argv[COMMAND] == 'init':

            # If there is more that one arg, the command prints and error and does nothing
            # if init is called more than once, then do nothing.
            if len(sys.argv) == 2:

                tables = Table()
                # if table exist then we have already initialized
                if tables.setup_tables():
                    print("Project initialized.")
                else:
                    print("Project already initialized.")

            else:

                # display error if we have more args then needed
                print("Incorrect number of arguments")

                Menu.show_help()

        elif sys.argv[COMMAND] == 'help':

            Menu.show_help()

        # if we don't have a project initialized and the create command is used then
        # initialize the tables.py and then proceed to use the create command
        elif sys.argv[COMMAND] == 'create':

            if len(sys.argv) == 3:

                tables = Table()

                tables.setup_tables()

                task_name = sys.argv[FIRST_ARG]

                # task names cannot start with dashes
                if task_name[0] is not "-":

                    task = Task()

                    task.create_task(task_name)

                else:
                    print("Task names cannot start with dashes")

            else:
                Menu.show_help()

        elif sys.argv[COMMAND] == 'select':

            # if select is the command and we have exactly
            # one more arg for a total of 3, then try to load
            # a task from the database, else print help
            if len(sys.argv) == 3:

                arg1 = sys.argv[FIRST_ARG]

                # only process dashes as directives, prevent processing as leading dashes in a task name
                # if arg1[0] == '-':
                #
                #     if arg1 == '-r':
                #
                #         status = Status()
                #
                #         if status.is_tracking_task():
                #
                #             tracking_task = TrackingTask()
                #
                #             tracking_task.remove_tracking_task()
                #
                #             print("Removing tracking task")
                #
                #         else:
                #             print("No task loaded")
                #     else:
                #         print("Directive not recognized")
                #
                # else:
                # initiate a new task

                task = Task()

                # see if we have a string with all digits
                # or a string with alphanum
                # if digits then try to get by id
                # if alphanum then try by name
                if arg1.isdigit():

                    task.get_task_by_id(arg1)

                else:

                    task.get_task_by_name(arg1)

                # if the task was able to be loaded
                # activate task by entering it into the
                # selected table. Ready to track entries
                if task.is_loaded():

                    tracking_task = TrackingTask()

                    tracking_task.add_tracking_task(task)

                else:
                    print("Could not load task '{0}'".format(arg1))

            else:
                Menu.show_help()

        elif sys.argv[COMMAND] == 'status':

            if len(sys.argv) == 2:

                status = Status()
                print(status)

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'start':

            if len(sys.argv) == 2:

                status = Status()

                if status.is_tracking_task():

                    task = status.get_tracking_task()

                    if status.is_tracking_entry():

                        print('You have an open entry')
                        print('To close an entry use command:\n$ stop')
                        print('To start a new entry use command:\n$ start')

                    else:

                        # if a task is selected then add to currently_tracking_table

                        tracking_entry = TrackingEntry()

                        tracking_entry.start_tracking(task)

                else:
                    print('Start tracking a task using command \nselect <taskname>')

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'stop':

            if len(sys.argv) == 2:

                status = Status()

                if status.is_tracking_entry():

                    tracking_entry = status.get_tracking_entry()

                    tracking_entry.stop_tracking()

                else:
                    print('You don\'t have any open entries')
                    print('To start a new entry use command: start')
            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'show':

            if len(sys.argv) == 3 and sys.argv[FIRST_ARG] == "-t":

                tasks = Tasks()
                print(tasks)

                for task in tasks.get_all_task():
                    print(task)

            elif len(sys.argv) == 3 and sys.argv[FIRST_ARG] == "-e":

                # Timedelta set to 0
                total_time = Datetime.timedelta()

                # get current tracking task
                status = Status()
                task = status.get_tracking_task()

                # all finished entries
                entries = status.get_all_entries()

                # header for print out
                print('\n------- All Entries For: {0} ---------'.format(task.get_name()))

                for entry in entries:

                    #
                    total_time += entry.get_elapse_time()
                    print(entry)

                print('\n------------- Summary ---------{0}\nTotal Entries: {1}\nTotal Time: {2} (h:m:s)'
                      '\n-------------------------------\n--------------------------------------------'
                      .format(task, len(entries), total_time))

            else:
                Menu.show_help()

        else:
            print("Don't know that one. Try one of these:")
            Menu.show_help()

    elif len(sys.argv) <= 1:
        # Menu.show_help()
        # Task().get_task_by_id(1123)
        # e = Entry()
        # e.update_entries()
        status = Status()



