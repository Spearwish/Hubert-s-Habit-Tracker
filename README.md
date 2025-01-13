# Hubert's Habit Tracker

A Python 3.7+ habit tracking app designed to help users build good habits and tear down the bad ones by tracking their progress and analyzing their performance over time. "Certified" reading tips included.

## What is it?
The user will be presented with the basic CLI, that will enable the following options for habit management and analysis: 
- A - Adding a habit. 
- C - Completing a task in a given period. 
- D - Deleting a habit. 
- L - Listing habits. 
- M - Getting the longest run streak of all defined habits. 
- R - Getting success rate of a habit. 
- S - Getting the longest run streak of a concrete habit.
- U - Getting struggling habits. 
- X - Exiting.

## Installation
1. Clone the repository:
```shell
git clone <repository-url>
cd habit_tracker
```
2. Install the dependencies:
```shell
pip install -r requirements.txt
```

## Usage
1. Start the app:
```shell
python main.py
```
2. and follow instructions on screen.

## Tests
Run unit tests to validate the functionality:
```shell
pytest .
```

## Predefined habits
1. Track your habits - every day.
2. Go to bed on time - every day.
3. Exercise or stretch - every other day.
3. Read two book chapters - every week.
5. Tidy up - every week.

## Documentation
- All methods and functions are documented using Python docstrings.