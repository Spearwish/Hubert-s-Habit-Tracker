from database import get_db, db_search
from datetime import datetime, timedelta


def get_streak(db, task: str):
    """
    Function for retrieving task's biggest streak.
    :param db: The SQLite3 database connection object.
    :param task: The name of the habit for streak calculation.
    :return: int, maximum streak (in days).
    """
    max_streak = 0
    running_streak = 0
    cursor = db.cursor()

    db_data = db_search(db, "*", "deadlines", "WHERE task = ?", (task,))

    for data in db_data:
        if data[4]:
            running_streak += 1
            max_streak = running_streak if max_streak < running_streak else max_streak
        else:
            running_streak = 0

    cursor.close()

    return max_streak


def get_success_rate(db, task: str, duration: int = 30):
    """
    Function for getting success / completion rate of a concrete habit for the last "duration" days.
    :param db: The SQLite3 database connection object.
    :param task: The name of the habit for success rate calculation.
    :param duration: The time span in days for last X days of calculation, defaults to 30.
    :return: float ranging from 0.0 to 1.0 , success/ completion rate.
    """
    cursor = db.cursor()
    db_data = db_search(db, "*", "deadlines", "WHERE task = ?", (task,))

    duration = int(duration) if duration else 30

    current_time = datetime.now()
    from_date = current_time - timedelta(days=duration)

    # including only concerte habits deadlines which are partially or completely streched over a certain duration
    filtered_data = [
        data for data in db_data
        if (
                (from_date <= datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S") <= current_time)
                or
                (from_date <= datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S") <= current_time)
        )
    ]

    check_off_sum = sum(data[4] for data in filtered_data)

    cursor.close()
    try:
        success_rate = check_off_sum / len(filtered_data)
    except ZeroDivisionError:
        success_rate = 0.0

    return success_rate
