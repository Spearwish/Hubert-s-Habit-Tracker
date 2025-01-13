import sqlite3
from datetime import datetime, timedelta


def get_db(db_name: str = "habits.db"):
    """
    Initializes the SQLite3 database, calls create_tables() function and sets up a SQLite3 database connector.
    :param: db_name: The name of the SQLite3 database.
    :return: The SQLite3 database connection object.
    """
    db = sqlite3.connect(db_name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates two database tables (if they do not already exist). Habits with columns for id, task, period, start_date, duration
    and deadlines with columns id, task, from_date, to_date, checked_off, completetion_date.
    :param db: The SQLite3 database connection object.
    :return: None
    """
    habit_table_query = """
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        period INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        duration INTEGER NOT NULL
    )
    """

    deadline_table_query = """
    CREATE TABLE IF NOT EXISTS deadlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task INTEGER NOT NULL,
        from_date TEXT NOT NULL,
        to_date TEXT NOT NULL,
        checked_off INTEGER NOT NULL,
        completion_date TEXT,
        FOREIGN KEY (task) REFERENCES habits (id)
    )
    """

    cursor = db.cursor()
    cursor.execute(habit_table_query)
    cursor.execute(deadline_table_query)
    db.commit()
    cursor.close()


def db_search(db, target: str, table: str, addon: str, params):
    """
    Executes a SQL SELECT query on a specified table with params and returns the results.
    :param db: The SQLite3 database connection object.
    :param target: The column to be selected from the table.
    :param table: The name of the SQL table.
    :param addon: Additional SQL clauses, such as WHERE, ...
    :param params: Parameters to be passed to the SQL query for addon specification.
    :return: All rows returned by the query as a list of tuples. If the query matches no rows, it will return an empty list.
    """
    query = f"""SELECT {target} FROM {table} {addon}"""
    cursor = db.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()


def insert_habit(db, task: str, period: int, duration: int = 365, start_date: str = None):
    """
    Inserts a habit data: task, period and optional data: duration, start_date into the habits table.
    Creates rows in deadlines table according to period, duration and start_date.
    :param db: The SQLite3 database connection object.
    :param task: The description of a habit.
    :param period: The periodicity (in days).
    :param duration: For how long is the habit defined, defaults to 365 days.
    :param date: Custom start_date, defaults to today's date.
    :return: None
    """

    habit_table_query = """
    INSERT INTO habits (task, period, start_date, duration) VALUES (?, ?, ?, ?)
    """

    deadline_table_query = """
    INSERT INTO deadlines (task, from_date, to_date, checked_off) VALUES (?, ?, ?, 0)
    """

    cursor = db.cursor()
    cursor.execute(
        habit_table_query,
        (
            task,
            period,
            start_date,
            duration,
        )
    )

    habit_intervlas = duration // period + 1
    for interval in range(habit_intervlas):
        cursor.execute(
            deadline_table_query,
            (task,
             datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=interval * period),
             datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=(interval + 1) * period)
             )
        )

    db.commit()
    cursor.close()


def list_habits(db, habit_period: int = None):
    """
    Lists all available habits and return the result based on habit_period, defaults to listing everything.
    :param db: The SQLite3 database connection object.
    :param habit_period: The period used for filtering the habits.
    :return: List of tuples - database entries.
    """
    cursor = db.cursor()

    if habit_period:
        db_data = db_search(db, "*", "habits", "WHERE period = ?", (habit_period,))
    else:
        db_data = db_search(db, "*", "habits", "", None)

    cursor.close()
    return db_data


def delete_habit(db, task: str = None):
    """
    Deletes specific entries in database according to task name.
    :param db: The SQLite3 database connection object.
    :param task: The name of the habit database entries to be deleted.
    :return: None
    """
    cursor = db.cursor()

    habit_table_query = """DELETE FROM habits WHERE task = ?"""
    deadline_table_query = """DELETE FROM deadlines WHERE task = ?"""
    cursor.execute(habit_table_query, (task,))
    cursor.execute(deadline_table_query, (task,))

    db.commit()
    cursor.close()


def check_off_habit(db, task: str, date: str = None):
    """
    Makes specified task/habit complete 0 -> 1 in a certain period. If no date is specifed it defaults to today's date.
    :param db: The SQLite3 database connection object.
    :param task: The name of the habit to be checked off.
    :param date: (optional) The completion date specification.
    :return: None
    """
    cursor = db.cursor()

    db_data = db_search(db, "*", "deadlines", "WHERE task = ?", (task,))

    if date:
        current_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        current_time = datetime.now()
    for data in db_data:
        from_date = datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
        to_date = datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S")

        if from_date <= current_time <= to_date:
            id = data[0]
            break

    check_off_query = """
    UPDATE deadlines SET checked_off = 1, completion_date = ? WHERE id = ?
    """
    cursor.execute(check_off_query, (current_time, id))
    db.commit()

    cursor.close()
