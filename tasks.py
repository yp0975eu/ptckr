from database import *


class Task(Database):

    __row_id = None
    __name = None

    def __init__(self):
        Database.__init__(self)

    def get_all_tasks(self):
        # select * from tasks
        pass

    def get_task_by_id(self, task_id):
        sql = """SELECT rowid, name FROM tasks WHERE rowid = (?);"""
        # Convert to tuple
        values = task_id,
        row = self.select_one_sql(sql, values)

        if row:
            self.__row_id = row['rowid']
            self.__name = row['name']

    def create_task(self, task_name):
        sql = """INSERT INTO tasks(name) VALUES (?);"""
        # Convert to tuple
        values = task_name,
        success_message = "Creating Task '{}'".format(task_name)
        self.insert_sql(sql, values, success_message)

    def delete_task(self):
        pass

    def get_task_by_name(self, name):
        sql = """SELECT rowid, name FROM tasks WHERE name = (?);"""
        # Convert to tuple
        values = name,
        row = self.select_one_sql(sql, values)

        if row:
            self.__row_id = row['rowid']
            self.__name = row['name']

    def is_loaded(self):
        return self.__row_id is not None if True else False

    def __str__(self):
        if self.is_loaded():
            return "ID   : {0}\nName : {1}".format(self.__row_id, self.__name)
        else:
            return "No Task Loaded"
