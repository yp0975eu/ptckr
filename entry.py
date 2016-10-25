from database import *
import datetime as Datetime


class Entry(Database):
    """Handles entries once they are complete"""

    __dateFormat = "%Y-%m-%d %H:%M:%S"

    # row: can pass in a row for instantiating an entry object
    # if there is no row then the object is empty and can be crated by
    # calling
    def __init__(self, row=None):
        Database.__init__(self)
        if row is None:
            self._task_id = None
            self._start = None
            self._stop = None
            self._description = None
            self._created_at = None
            self._updated_at = None
            self._elapsed_time = None
        # elif isinstance(row, TrackingEntry):
        #     self.__task_id = row.get_task_id()
        #     self.__start = row.get_start()
        #     self.__created_at = self.__updated_at = self.__stop = Datetime.datetime.now()
        else:
            self.set_attributes(row)

    def get_all_entries(self, task_id):
        sql = """SELECT rowid, task_id, start, stop, description, created_at, updated_at
        FROM entries
        WHERE task_id = ?"""
        values = task_id,
        return self.select_many_sql(sql, values)

    def insert_new_entry(self):
        self.set_description()
        sql = """INSERT INTO entries(task_id, start, stop, description, created_at, updated_at) Values(?,?,?,?,?,?)"""
        values = (self._task_id, self._start, self._stop, self._description, self._created_at, self._updated_at)
        self.insert_sql(sql, values, "Entry Saved")

    def delete_entry(self):
        pass

    def update_entries(self):
        # sql = """SELECT rowid, created_at, updated_at FROM tasks"""
        # usql = """UPDATE tasks
        # SET  created_at=?, updated_at=?
        # WHERE rowid=?"""
        # rows = self.select_many_sql(sql)
        # for row in rows:
        #
        #     ca = self.update_time_format(row['created_at'])
        #     up = self.update_time_format(row['updated_at'])
        #     values = (ca, up, row['rowid'])
        #     self.insert_sql(usql, values, "Updated Timestamps")
        pass

    # def update_time_format(self, time):
    #     tformat = Datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    #     return tformat.__format__("%Y-%m-%d %H:%M:%S")

    # for instantiating entry objects from a database row form the entry table
    def set_attributes(self, row):
        self._task_id = row["task_id"]
        self._start = row["start"]
        self._stop = row["stop"]
        self._description = row["description"]
        self._created_at = row["created_at"]
        self._updated_at = row["updated_at"]
        self._elapsed_time = self.get_elapse_time()

    def set_description(self):
        print("Enter a description for this entry")
        description = input("> ")
        self._description = description

    def get_elapse_time(self):
        t1 = Datetime.datetime.strptime(self._start, self.__dateFormat)
        t2 = Datetime.datetime.strptime(self._stop, self.__dateFormat)
        delta = t1 - t2
        return abs(delta)

    def __str__(self):
        time = self.get_elapse_time()
        return "\nEntry: {0}\nStarted at: {1}\nStopped at: {2}\nElapsed {3}".format(
            self._description,
            self._start,
            self._stop,
            time
        )


class TrackingEntry(Entry):
    def __init__(self):
        Entry.__init__(self)
        self._rowid = None
        sql = """SELECT rowid, task_id, start, stop FROM tracking_entry"""
        row = self.select_one_sql(sql)
        if row:
            self.set_attributes(row)

    def is_loaded(self):
        return self._rowid is not None

    def start_tracking(self, task):
        # check if there is a currently tracked entry already
        sql = """INSERT INTO tracking_entry(task_id, start, stop) VALUES(?,?,?)"""

        task_id = task.get_row_id()

        start = Database.get_timestamp()
        stop = None

        values = (task_id, start, stop)

        message = "Creating entry for task: {0}\nEntry started at: {1}"\
            .format(task.get_name(), start)

        self.insert_sql(sql, values, message)

        task.update_timestamp()

    # when we are done tracking an entry and want to
    # enter an new entry into the db table:entry
    def stop_tracking(self):

        self._stop = self._created_at = self._updated_at = Database.get_timestamp()

        self.insert_new_entry()

        self.remove_tracking_entry()

    def remove_tracking_entry(self):
        sql = """DELETE FROM tracking_entry"""
        self.delete_sql(sql)

    def set_attributes(self, row):
        self._rowid = row["rowid"]
        self._task_id = row["task_id"]
        self._start = row["start"]
        self._stop = row["stop"]

    def get_rowid(self):
        return self._rowid

    def get_task_id(self):
        return self._task_id

    def get_start(self):
        return self._start

    def __str__(self):
        if self.is_loaded():
            return "\nEntry Started At: {0}".format(self._start)
        else:
            return "No entry started, to start tracking use command: start"
