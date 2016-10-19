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

            print("Error Making Table", o_err)

        except sqlite3.IntegrityError:

            print("Project '{}' already exists".format(values[0]))
