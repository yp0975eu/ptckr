from database import *


class Task(Database):

    def __init__(self):
        Database.__init__(self)

    def get_all_tasks(self):
        # select * from tasks
        pass

    def get_task_by_id(self, id):
        pass

    def create_task(self, task_name):
        sql = """INSERT INTO tasks(name) VALUES (?);"""
        # Convert to tuple
        values = task_name,
        success_message = "Creating Task '{}'".format(task_name)
        self.insert_sql(sql, values, success_message)

    def delete_task(self):
        pass

    def get_task_by_name(self, name):
        pass
