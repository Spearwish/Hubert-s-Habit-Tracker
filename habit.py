from database import insert_habit, delete_habit, check_off_habit
from datetime import datetime

class Habit:
    """
    This is a lightweight data class serving as an intermediate before pushing data to the database.
    """
    a, b = ("hey", "be")
    def __init__(self, task: str, period: int, duration: int = 365):
        """
        Creates a new habit data object.
        :param: task: stores the description of a praticular habit.
        :param: period: stores arbitrary habit periodicity: daily (1) / every two days (2) / weekly (7) / ...
        :return: None
        """

        self.task = task
        self.period = abs(int(period))
        self.duration = abs(int(duration))
        self.start_date = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        """
        Returns a string representation of the habit data object.
        :return: A string in the format: "task: 'task', period: period, duration: duration".
        """
        return f"task: ‘{self.task}‘, period: {self.period}, duration: {self.duration}"

    def store(self, db):
        """
        Stores a habit data obejct in the database.
        :param db: The SQLite3 database connection object.
        :return: None
        """
        insert_habit(db, self.task, self.period, self.duration, self.start_date)

    def remove(self, db):
        """
        Removes a habit data obejct from the database.
        :param db: The SQLite3 database connection object.
        :return: None
        """
        delete_habit(db, self.task)

    def check_off(self, db, date: str = None):
        """
        Makes specified task/habit complete 0 -> 1 in a certain period. If no date is specifed it defaults to today's date.
        :param db: The SQLite3 database connection object.
        :return: None
        """
        check_off_habit(db, self.task, date)
