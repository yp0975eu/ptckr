import sys
from Database import Db

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
    db = Db()
    if len(sys.argv) >= 2:

        if sys.argv[COMMAND] == 'init':

            # If there is more that one arg, the command prints and error and does nothing
            if len(sys.argv) == 2:

                print("Project initialized.")

            else:

                # display error if we have more args then needed
                print("Incorrect number of arguments")

                Menu.show_help()

        elif sys.argv[COMMAND] == 'help':

            Menu.show_help()

        elif sys.argv[COMMAND] == 'create':

            if len(sys.argv) == 3:

                task_name = sys.argv[FIRST_ARG]
                print('Creating task {}'.format(task_name))

            else:

                Menu.show_help()

        elif sys.argv[COMMAND] == 'select':

            if len(sys.argv) == 3:

                task_name = sys.argv[FIRST_ARG]
                print('Selecting task {}'.format(task_name))

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
