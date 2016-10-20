from tasks import *


class Status(Database):

    """Keeps track of the status of the selected task and entries"""

    def __init__(self):
        Database.__init__(self)
        sql = """SELECT task_id, created_at, updated_at FROM tracking_task"""
        row = self.select_one_sql(sql)
        if row:

            # instantiate a task class
            task = Task()

            # load task by id
            task.get_task_by_id(row['task_id'])

            # set task to selected task
            self.__selected_task = task

    def add_tracking_task(self, task):
        self.remove_tracking_tasks()
        sql = """INSERT INTO tracking_task(task_id, created_at, updated_at) VALUES(?,?,?)"""
        task_id = task.get_row_id()
        created_at = update_at = datetime.datetime.now()
        values = (task_id, created_at, update_at)
        self.insert_sql(sql, values, "Selected task: {0}".format(task.get_name()))

    def add_tracking_entry(self, entry):
        pass

    def remove_tracking_tasks(self):
        sql = """DELETE  FROM tracking_task"""
        self.delete_sql(sql)

    def __str__(self):
        if self.__selected_task is not None:
            return "\nSelected task:" + self.__selected_task.__str__()
        else:
            return "No task selected"
