from habit import Habit
from database import get_db, list_habits
from analyse import get_streak, get_success_rate
from datetime import datetime
import random

# Feel free to add other reading tips.
tips = ["Recharge yourself efficiently - Why We Sleep by Matthew Walker.",
        "Focused work is a good work - Deep Work by Cal Newport.",
        "Understand the habits - The Power of Habit by Charles Duhigg.",
        "Master your productivity - Getting Things Done by David Allen.",
        "Skip the reading today - try meditation instead.",
        ]


def validate_input(db, input: str):
    """
    Verifies if input - task name exists in the database.
    :param db: The SQLite3 database connection object.
    :param input: The task name for database comparasion.
    :return: True if the input exists in the database, otherwise False.
    """
    habits = list_habits(db)
    for habit in habits:
        if habit[1] == input:
            return True
    return False


def int_input(caption: str):
    """
    Input function that forces user to input whole positive non-zero number.
    :param caption: Prompt message displayed to the user.
    :return: Validated user input as a string.
    """
    while True:
        user_input = input(caption)
        if user_input.isdigit() and int(user_input) > 0:
            return user_input
        else:
            print("Invalid input, enter a whole positive non-zero number.")


def cli():
    """
    Interactive user interface for the habit app.
    :return: None
    """
    db = get_db()

    print("A - adding a habit")
    print("C - completing a task in a given period")
    print("D - deleting a habit")
    print("L - listing habits")
    print("M - getting the longest run streak of all defined habits")
    print("R - getting success rate of a habit")
    print("S - getting the longest run streak of a concrete habit")
    print("U - getting struggling habits")
    print("X - exit")

    while True:
        valid_input = False
        user_input = input("\nMake your choice please:\n").upper()

        if user_input in ("C", "D", "R", "S"):
            while True:
                habit_task = input("Enter the task name:\n")
                valid_input = validate_input(db, habit_task)
                if valid_input:
                    break
                elif habit_task == "QUIT":
                    break
                else:
                    print("There is no such task name in database. Type QUIT to make another choice.")

        if user_input == "A":
            habit_task = input("Enter a description:\n")
            habit_period = int_input("Enter a periodicity - in days:\n")
            habit_duration = int_input("Enter a duration - in days:\n")

            try:
                habit = Habit(habit_task, habit_period, habit_duration)
                habit.store(db)
                print(f"Habit '{habit_task}' successfully added.")
            except Exception as e:
                print(f"Failure while adding the habit: {e}")

        elif user_input == "C" and valid_input:
            date = input("Enter the date in following format: 'YYYY-MM-DD' or skip for todays date:\n")
            try:
                habit = Habit(habit_task, 0, 0)
                habit.check_off(db, date)
                print(f"Habit '{habit_task}' successfully checked off.")
            except Exception as e:
                print(f"Failure while checking off the habit: {e}")

        elif user_input == "D" and valid_input:
            habit = Habit(habit_task, 0, 0)
            habit.remove(db)
            print(f"Habit '{habit_task}' successfully deleted.")

        elif user_input == "L":
            try:
                habit_period = input("Optional: Enter a periodicity to narrow search or 'SKIP' for full search:\n")
                result = list_habits(db, habit_period)
                print(result if result else "There is nothing to display.")
            except Exception as e:
                print(f"Failure while listing the habits: {e}")

        elif user_input == "M":
            max_streak, habit_name = max(
                ((get_streak(db, habit[1]), habit[1]) for habit in list_habits(db)),
                key=lambda x: x[0]
            )
            print(f"The maximum streak is {max_streak}x for habit '{habit_name}'.")

        elif user_input == "R" and valid_input:
            try:
                habit_duration = input("Optional: Enter a history duration or 'SKIP' for querying only last month:\n")
                print(f"The success rate is {get_success_rate(db, habit_task, habit_duration) * 100:.2f} % "
                      f"for a habit '{habit_task}'.")
            except Exception as e:
                print(f"Failure while getting the success rate of the habit: {e}")

        elif user_input == "S" and valid_input:
            print(f"The longest run streak is {get_streak(db, habit_task)} for a habit '{habit_task}'.")

        elif user_input == "U":
            habit_success_rates = [(habit, get_success_rate(db, habit[1], 30)) for habit in list_habits(db)]

            sorted_habits = sorted(habit_success_rates, key=lambda x: x[1])
            worst_habits = sorted_habits[:3]

            print(f"{len(worst_habits)} Worst Habit{'s' if len(worst_habits) > 1 else ''} (Lowest Success Rate{'s' if len(worst_habits) > 1 else ''}):")
            if worst_habits:
                for habit, success_rate in worst_habits:
                    print(f"Habit: {habit[1]}, Success Rate: {success_rate * 100:.2f} %")
            else:
                print("You did not list any habits.")

            print("Reading tip for a better productivity:")
            print(random.choice(tips))

        elif user_input == "X":
            print("Thank you for using Habit tracker app.")
            break

        elif not valid_input:
            print("Choose L for listing habits in database.")

        else:
            print("Invalid choice.")

    db.close()


if __name__ == "__main__":
    cli()
