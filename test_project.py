import pytest

from habit import Habit
from database import get_db, insert_habit, check_off_habit, list_habits, delete_habit
from analyse import get_streak, get_success_rate
import os


class TestHabit:
    """
    Tests entire flow of habit: creation, storing, listing, checking off, analyzing, deleting.
    """

    def setup_method(self):
        self.test_db = get_db("test.db")

    def test_habit(self):
        habit = Habit("test_description_1", 1, 60)

        habit.store(self.test_db)
        assert len(list_habits(self.test_db, 1)) == 1
        assert len(list_habits(self.test_db)) == 1

        habit.check_off(self.test_db)
        assert get_streak(self.test_db, "test_description_1") == 1
        assert get_success_rate(self.test_db, "test_description_1", 9999) > 0

        habit.remove(self.test_db)
        assert len(list_habits(self.test_db, 1)) == 0
        assert len(list_habits(self.test_db)) == 0

    def test_db(self):
        insert_habit(self.test_db, "test_description_2", 2, 180, "2024-12-31")
        insert_habit(self.test_db, "test_description_3", 3, 180, "2024-12-31")
        assert len(list_habits(self.test_db, 2)) == 1
        assert len(list_habits(self.test_db, 3)) == 1
        assert len(list_habits(self.test_db)) == 2

        check_off_habit(self.test_db, "test_description_2", "2024-12-31 23:59:59")
        assert get_streak(self.test_db, "test_description_2") == 1
        check_off_habit(self.test_db, "test_description_2", "2025-01-02 00:00:01")
        assert get_streak(self.test_db, "test_description_2") == 2
        check_off_habit(self.test_db, "test_description_2", "2025-01-05 00:00:00")
        assert get_streak(self.test_db, "test_description_2") == 3
        check_off_habit(self.test_db, "test_description_2", "2025-01-09 00:00:01")
        assert get_streak(self.test_db, "test_description_2") == 3  # there is a gap (111-0-1...)

        assert get_success_rate(self.test_db, "test_description_2", 9999) > 0

        delete_habit(self.test_db, "test_description_2")
        assert len(list_habits(self.test_db, 2)) == 0
        assert len(list_habits(self.test_db, 3)) == 1
        assert len(list_habits(self.test_db)) == 1 # when a habit_period is not specified -> listing all habits

        delete_habit(self.test_db, "test_description_3")
        assert len(list_habits(self.test_db, 2)) == 0
        assert len(list_habits(self.test_db, 3)) == 0
        assert len(list_habits(self.test_db)) == 0


    def teardown_method(self):
        os.remove("test.db")
