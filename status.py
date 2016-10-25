from tasks import *
from entry import *


class Status(Database):

    """Keeps track of the status of the selected task and entries"""

    def __init__(self):
        Database.__init__(self)

        # initialize attributes to None
        self.__tracking_task = None

        self.__tracking_entry = None

        self.__all_entries = []

        # see if we are tracking a task in our tracking_task table
        tracking_task = TrackingTask()

        if tracking_task.is_loaded():

            # set task to selected task

            self.__tracking_task = tracking_task

            # load all completed entries
            entry = Entry()

            entries = entry.get_all_entries(self.__tracking_task.get_row_id())

            for entry_row in entries:
                self.__all_entries.append(Entry(entry_row))

            # load tracking entry
            tracking_entry = TrackingEntry()

            if tracking_entry.is_loaded():

                self.__tracking_entry = tracking_entry

    def is_tracking_task(self):
        return self.__tracking_task is not None

    def is_tracking_entry(self):
        return self.__tracking_entry is not None

    def get_tracking_task(self):
        return self.__tracking_task

    def get_tracking_entry(self):
        return self.__tracking_entry

    def get_all_entries(self):
        return self.__all_entries

    def __str__(self):
        task = self.__tracking_task.__str__()

        if self.is_tracking_entry():
            entry = self.__tracking_entry.__str__()
        else:
            entry = "Not tracking an entry"

        return "\nSelected task ------------\n{0}\n{1}".format(task, entry)

