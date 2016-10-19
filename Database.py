import sqlite3


class Db:
    __connection = None
    __cursor = None
    __database_file_name = ".projects.db"
    __table_names = ("tasks", "entries", "currently_tracking")

    # setup project database
    def __init__(self):
        try:
            self.__connection = sqlite3.connect(self.__database_file_name)
            self.__cursor = self.__connection.cursor()
        except sqlite3.DataError as data_error:
            print("Cannot connect to database", data_error)
            exit()

    def setup_tables(self):
        # to keep track of existing tables
        existing_tables = []

        # loop through defined tables
        for table in self.__table_names:

            # see if we have the tables already
            if not self.table_exist(table):

                # if we don't have the tables then create them
                try:
                    # this calls the method named: self.make_table_<table_name>
                    getattr(self, 'make_table_' + table)()
                except AttributeError as a_error:
                    print("Error making table. "
                          "Does table '{}' have a corresponding method 'make_table_{}()' ?".format(table, table))
                    print(a_error)
            else:
                # add to list of existing tables
                existing_tables.append(table)

        # return true if we needed to create tables else false if they already existed.
        return len(existing_tables) == 0 if True else False

    def table_exist(self, table):
        # SQL from http: // stackoverflow.com / a / 8827554
        sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = ?;"
        cur = self.__cursor
        # turn into tuple
        value = table,
        cur.execute(sql, value)
        count = cur.fetchall()[0][0]
        return count == 1

    def make_table_tasks(self):
        # id removed because sqlite3 makes an id automatically
        # id          INTEGER NOT NULL PRIMARY KEY,
        sql = '''CREATE TABLE  IF NOT EXISTS tasks  (
         name             TEXT NOT NULL
         );'''
        self.make_table(sql)

    def make_table_entries(self):
        sql = '''CREATE TABLE  IF NOT EXISTS entries  (
         task_id     INTEGER,
         start       TEXT NOT NULL,
         stop        TEXT NOT NULL,
         description TEXT NOT NULL,
         FOREIGN KEY(task_id) REFERENCES tasks(ROWID)
         );'''
        self.make_table(sql)

    # Tracking table keeps track of currently selected task, start and end time
    def make_table_currently_tracking(self):
        sql = '''CREATE TABLE IF NOT EXISTS currently_tracking (
         entry_id INTEGER,
         start INTEGER NOT NULL,
         stop INTEGER,
         FOREIGN KEY(entry_id) REFERENCES entries(ROWID)
         );'''
        self.make_table(sql)

    # runs sql with no arguments
    def make_table(self, sql):
        try:
            cur = self.__cursor
            cur.execute(sql)
            self.__connection.commit()
        except sqlite3.OperationalError as o_err:
            print("Error Making Table", o_err)
        except sqlite3.DatabaseError as db_err:
            print("Database Error while making table", db_err)

    def insert_project(self, project_name):
        sql = """INSERT INTO projects(name) VALUES (?);"""
        # Convert to tuple
        values = project_name,
        success_message = "Creating Project '{}'".format(project_name)
        self.insert_sql(sql, values, success_message)

    # runs sql with arguments
    def insert_sql(self, sql, values, success_message):
        try:
            self.__cursor.execute(sql, values)
            self.__connection.commit()

            # if there is no error then print the success message
            print(success_message)
        except sqlite3.OperationalError as o_err:
            print("Error Making Table", o_err)
        except sqlite3.IntegrityError:
            print("Project '{}' already exists".format(values[0]))
