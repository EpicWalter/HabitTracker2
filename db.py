"""
The database module groups all database interactions. The provided functions can then be used by other modules.
"""

import sqlite3

def get_db(name="main.db"):
    """
    Establishes a connection to the SQLite database and calls the create_tables() function.

    :param name: The name of the database file (default is "main.db").
    :return: A connection object to the SQLite database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    """
    Creates the required tables if they do not exist already. Otherwise does nothing.

    habits: Stores details about habits, including name, description, periodicity, creation date,
    current streak, and the last increment date.

    increments: Stores records of habit increments, including the timestamp, habit name,
    and streak value at the time of the increment.

    :param db: The database connection object.
    :return: None
    """
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits ( 
        name TEXT PRIMARY KEY, 
        description TEXT,
        periodicity TEXT,
        created_at TEXT,
        current_streak INT,
        last_increment_date TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS increments (
            incremented_at TEXT, 
            habitName TEXT,
            streak INTEGER,
            FOREIGN KEY (habitName) REFERENCES habit(name))""")
    db.commit()


def add_habit(db, name, description, periodicity, created_at, last_increment_date=None): #last_increment_date can be added for testing purposes
    """
    Add a new habit to the database.
    Last increment date can be added for testing purposes.
    The current streak is initialized to 0 by default.

    :param db: The database connection object.
    :param name: The name of the habit.
    :param description: A brief description of the habit.
    :param periodicity: The periodicity of the habit, either "Daily" or "Weekly".
    :param created_at: When the habit was created.
    :param last_increment_date: When the habit was incremented last. Defaults to None.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?)", (name, description, periodicity, created_at, 0, last_increment_date))
    db.commit()


def increment_habit(db, name, event_timestamp, streak):
    """
    Inserts a new increment event into the increments table and updates the habit table to reflect the new streak value.

    :param db: The database connection object.
    :param name: The name of the habit.
    :param event_timestamp: The timestamp of the increment event.
    :param streak: The updated streak value to be recorded for the habit.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO increments (incremented_at, habitName, streak) VALUES (?, ?, ?)", (event_timestamp, name, streak))
    cur.execute("""UPDATE habits SET current_streak = ?, last_increment_date = ? WHERE name = ?""", (streak, event_timestamp, name))
    db.commit()



def load_habit(db, name):
    """
    Load habit details from the database for a given habit name.

    :param db: The database connection object.
    :param name: The name of the habit to be retrieved.
    :return: A dictionary containing the habit's details.
    :raises ValueError: If the habit with the specified name does not exist in the database.
    """
    cursor = db.cursor()
    cursor.execute("SELECT name, description, periodicity, current_streak, last_increment_date FROM habits WHERE name "
                   "= ?", (name,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"Habit '{name}' does not exist.")

    return {
        "name": result[0],
        "description": result[1],
        "periodicity": result[2],
        "current_streak": result[3],
        "last_increment_date": result[4]
    }


def delete_habit(db, name):
    """
    Delete all database records for a given habit from the increments and habits table.

    :param db: The database connection object.
    :param name: The name of the habit to be deleted.
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM increments WHERE habitName = ?", (name,))
    cur.execute("DELETE FROM habits WHERE name = ?", (name,))
    db.commit()