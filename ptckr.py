import sys
from tables import Table
from tasks import Task

FILENAME = 0
COMMAND = 1
FIRST_ARG = 2
SECOND_ARG = 3


class Menu:
    top_menu = (
        {'command': "init", "desc": '\tinit\n\t\tDef: Initializes a project in current directory'},
        {'command': "help", "desc": '\thelp\n\t\tDef: Shows this help menu'},
        {'command': 'create', 'desc': '\tcreate <task>\n\t\tDef: Creates a new task'},
        {'command': 'select', 'desc': '\tselect <task>\n\t\tDef: Select a task to track'},
        {'command': 'status', 'desc': '\tstatus\n\t\tDef: Shows current selected task'},
        {'command': 'start', 'desc': '\tstart\n\t\tDef: Starts tracking time'},
        {'command': 'stop', 'desc': '\tstop\n\t\tDef: Stops tracking time'},
        {'command': "view", "desc": '\tview [-t]\n\t\tDef: Shows entries for currently selected task.'
                                      ' Use -t to view all tasks'},
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

                tasks = Task()
                tasks.create_task(task_name)

            else:
                Menu.show_help()

        elif sys.argv[COMMAND] == 'select':

            # if select is the command and we have exactly
            # one more arg for a total of 3, then try to load
            # a task from the database, else print help
            if len(sys.argv) == 3:

                arg1 = sys.argv[FIRST_ARG]

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

                # if the task was able to be loaded enter in into
                # the activate task by entering it into the
                # selected table and getting ready
                # for creating entries
                if task.is_loaded():

                    print(task)

                else:
                    print("Could not load task '{0}'".format(arg1))

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'status':

            if len(sys.argv) == 2:

                print('Show current selected task here')

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'start':

            if len(sys.argv) == 2:

                # if a task is selected then
                print('Start tracking time for currently selected task')

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'stop':

            if len(sys.argv) == 2:

                # if a task is selected then
                print('Stop tracking time for currently selected task')
                print('Enter Message for currently selected task')
                print('Message saved entry header')

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'view':
            if len(sys.argv) == 2:
                print('Viewing all entries under currently selected task')
            elif len(sys.argv) == 3 and sys.argv[FIRST_ARG] == "-t":
                print('view all tasks')
            else:
                Menu.show_help()
        else:
            print("Don't know that one. Try one of these:")
            Menu.show_help()
    elif len(sys.argv) <= 1:
        Menu.show_help()
        # Task().get_task_by_id(1123)
