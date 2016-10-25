from database import *


class Task(Database):

    def __init__(self, row=''):
        Database.__init__(self)
        self._row_id = None
        self._name = None
        self._created_at = None
        self._updated_at = None
        if row:
            self.set_task_attributes(row)

    def get_task_by_id(self, task_id):
        sql = """SELECT rowid, name, created_at, updated_at FROM tasks WHERE rowid = (?);"""

        # Convert to tuple
        values = task_id,

        row = self.select_one_sql(sql, values)

        if row:
            self.set_task_attributes(row)

    def create_task(self, task_name):
        sql = """INSERT INTO tasks(name, created_at, updated_at) VALUES (?,?,?);"""
        # Convert to tuple
        created_at = updated_at = Database.get_timestamp()

        values = (task_name, created_at, updated_at)

        success_message = "Creating Task '{}'".format(task_name)

        self.insert_sql(sql, values, success_message)

    def delete_task(self):
        pass

    def get_task_by_name(self, name):
        sql = """SELECT rowid, name, created_at, updated_at FROM tasks WHERE name = (?);"""
        # Convert to tuple
        values = name,
        row = self.select_one_sql(sql, values)

        if row:
            self.set_task_attributes(row)

    def set_task_attributes(self, row):
        if isinstance(row, sqlite3.Row):
            self._row_id = row['rowid']
            self._name = row['name']
            self._created_at = row['created_at']
            self._updated_at = row['updated_at']

    def get_row_id(self):
        return self._row_id

    def get_name(self):
        return self._name

    def is_loaded(self):
        return self._row_id is not None if True else False

    def update_timestamp(self):

        sql = """UPDATE tasks SET updated_at = ? WHERE rowid = ?"""
        # Convert to tuple
        updated_at = Database.get_timestamp()

        values = (updated_at, self._row_id)

        success_message = "Updated Timestamp To '{}'".format(updated_at)

        self.insert_sql(sql, values, success_message)

    def __str__(self):
        if self.is_loaded():
            return "\nTask Name : {0}\nCreated At: {1}\nUpdated At: {2}".format(
                self._name,
                self._created_at,
                self._updated_at
            )
        else:
            return "No Task Loaded"


class TrackingTask(Task):

    def __init__(self):
        Task.__init__(self)
        sql = """SELECT task_id, created_at, updated_at FROM tracking_task"""
        row = self.select_one_sql(sql)
        if row:
            self.get_task_by_id(row['task_id'])

    def add_tracking_task(self, task):

        self.remove_tracking_task()

        sql = """INSERT INTO tracking_task(task_id, created_at, updated_at) VALUES(?,?,?)"""

        task_id = task.get_row_id()

        created_at = update_at = Database.get_timestamp()

        values = (task_id, created_at, update_at)

        self.insert_sql(sql, values, "Now Tracking: {0}".format(task.get_name()))

    def remove_tracking_task(self):
        sql = """DELETE FROM tracking_task"""
        self.delete_sql(sql)


class Tasks(Database):
    """Instantiates all tasks we currently have"""

    def __init__(self):
        Database.__init__(self)
        self.__all_tasks = self.load_tasks()

    def get_all_task(self):
        return self.__all_tasks

    def load_tasks(self):
        all_tasks = []

        sql = """SELECT rowid, name, created_at, updated_at FROM tasks"""

        rows = self.select_many_sql(sql)

        if rows:
            for row in rows:
                all_tasks.append(Task(row))

        return all_tasks

    def __str__(self):
        return "{0} tasks".format(len(self.__all_tasks))
