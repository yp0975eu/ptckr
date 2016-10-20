from database import *
import datetime


class Task(Database):

    def __init__(self):
        Database.__init__(self)
        self._row_id = None
        self._name = None
        self._created_at = None
        self._updated_at = None

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
        created_at = updated_at = datetime.datetime.now()
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

    def __str__(self):
        if self.is_loaded():
            return "\nID   : {0}\nName : {1}\nCreated at: {2}\nUpdated at: {3}".format(
                self._row_id,
                self._name,
                self._created_at,
                self._updated_at)
        else:
            return "No Task Loaded"
