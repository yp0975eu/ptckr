from database import *
# access all parts of the database.py module include sqlite3


class Table(Database):
    """For creating the actual database tables.py"""

    __table_names = ("tasks", "entries", "currently_tracking_task", "currently_tracking_entry")

    def __init__(self):
        Database.__init__(self)

    def setup_tables(self):
        # to keep track of existing tables.py
        existing_tables = []

        # loop through defined tables.py
        for table in self.__table_names:

            # see if we have the tables.py already
            if not self.table_exist(table):

                # if we don't have the tables.py then create them
                try:
                    # this calls the method named: self.make_table_<table_name>
                    getattr(self, 'make_table_' + table)()
                except AttributeError as a_error:
                    print("Error making table. "
                          "Does table '{}' have a corresponding method 'make_table_{}()' ?".format(table, table))
                    print(a_error)
                    exit()
            else:
                # add to list of existing tables.py
                existing_tables.append(table)

        # return true if we needed to create tables.py else false if they already existed.
        return len(existing_tables) == 0 if True else False

    def table_exist(self, table):
        # SQL from http: // stackoverflow.com / a / 8827554
        sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = ?;"
        cur = self._cursor
        # turn into tuple
        value = table,
        cur.execute(sql, value)
        count = cur.fetchall()[0][0]
        return count == 1

    def make_table_tasks(self):
        sql = '''CREATE TABLE  IF NOT EXISTS tasks  (
         name             TEXT NOT NULL UNIQUE,
         created_at       TEXT NOT NULL,
         updated_at       TEXT NOT NULL
         );'''
        self.make_table(sql)

    def make_table_entries(self):
        sql = '''CREATE TABLE  IF NOT EXISTS entries  (
         task_id     INTEGER,
         start       TEXT NOT NULL,
         stop        TEXT NOT NULL,
         description TEXT NOT NULL,
         created_at       TEXT NOT NULL,
         updated_at       TEXT NOT NULL,
         FOREIGN KEY(task_id) REFERENCES tasks(ROWID)
         );'''
        self.make_table(sql)

    # Tracking table keeps track of currently selected task, start and end time
    def make_table_currently_tracking_task(self):
        sql = '''CREATE TABLE IF NOT EXISTS tracking_task (
         task_id INTEGER,
         created_at       TEXT NOT NULL,
         updated_at       TEXT NOT NULL,
         FOREIGN KEY(task_id) REFERENCES tasks(ROWID)
         );'''
        self.make_table(sql)

    # Tracking table keeps track of currently selected task, start and end time
    def make_table_currently_tracking_entry(self):
        sql = '''CREATE TABLE IF NOT EXISTS tracking_entry (
         tracking_id INTEGER,
         start INTEGER NOT NULL,
         stop INTEGER,
         created_at       TEXT NOT NULL,
         updated_at       TEXT NOT NULL,
         FOREIGN KEY(tracking_id) REFERENCES tracking_task(ROWID)
         );'''
        self.make_table(sql)

    # runs sql with no arguments
    def make_table(self, sql):
        try:
            cur = self._cursor
            cur.execute(sql)
            self._connection.commit()
        except sqlite3.OperationalError as o_err:
            print("Error Making Table", o_err)
            exit()
        except sqlite3.DatabaseError as db_err:
            print("Database Error while making table", db_err)
            exit()
