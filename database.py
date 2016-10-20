import sqlite3


class Database:
    """Managing connections and database."""

    # class variables available to all instances of Db
    _connection = None
    _cursor = None
    __database_file_name = 'projects.db'

    def __init__(self):
        try:
            self._connection = sqlite3.connect(self.__database_file_name)
            self._cursor = self._connection.cursor()

        except sqlite3.DataError as data_error:
            print("Cannot connect to database", data_error)
            exit()

    # runs sql with arguments
    def insert_sql(self, sql, values, success_message):
        try:

            self._cursor.execute(sql, values)

            self._connection.commit()

            # if there is no error then print the success message
            print(success_message)

        except sqlite3.OperationalError as o_err:

            print("Operational Error: ", o_err)

        except sqlite3.IntegrityError:

            print("'{}' already exists".format(values[0]))

    # returns one row
    def select_one_sql(self, sql, values=''):
        # localize the connection to return a Row
        try:
            con = self._connection
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql, values)
            return cur.fetchone()

        except sqlite3.OperationalError as o_err:

            print("Error Selecting", o_err)

        except sqlite3.ProgrammingError as o_err:

            print("Wrong number of args", values, o_err)

            # returns one row

    def select_many_sql(self, sql, values=''):
        # localize the connection to return a Row
        try:
            con = self._connection
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql, values)
            return cur.fetchall()

        except sqlite3.OperationalError as o_err:

            print("Error Selecting", o_err)

        except sqlite3.ProgrammingError as o_err:

            print("Wrong number of args", values, o_err)

    def delete_sql(self, sql, where=""):
        # localize the connection to return a Row
        try:

            cur = self._cursor
            cur.execute(sql, where)

        except sqlite3.OperationalError as o_err:

            print("Error Deleting", o_err)

        except sqlite3.ProgrammingError as o_err:

            print("Wrong number of args", where, o_err)
