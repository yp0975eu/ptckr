from database import *
import datetime as Datetime


class Status(Database):

    """Keeps track of the status of the selected task and entries"""

    # shared variables for singleton method
    __selected_task = None
    __current_entry = None
    __entry_start = None

    def __init__(self):
        Database.__init__(self)

    def get_selected_task(self):
        if self.__selected_task is not None:
            return self.__selected_task
        else:
            sql = "SELECT rowid, task_id FROM tracking_task"
        pass

    def add_tracking_task(self, task):
        self.remove_tracking_tasks()
        sql = """INSERT INTO tracking_task(task_id, created_at, updated_at) VALUES(?,?,?)"""
        task_id = task.get_row_id()
        created_at = update_at = Datetime.datetime.now()
        values = (task_id, created_at, update_at)
        self.insert_sql(sql, values, "Selected task: {0}".format(task.get_name()))

    def add_tracking_entry(self, entry):
        pass

    def remove_tracking_tasks(self):
        sql = """DELETE  FROM tracking_task"""
        where = ""
        self.delete_sql(sql, where)

