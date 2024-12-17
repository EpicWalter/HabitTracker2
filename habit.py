from db import add_habit, increment_habit, load_habit, delete_habit
from datetime import datetime, timedelta


class Habit:
    def __init__(self, name: str, description: str, periodicity: str):
        """
        Habit class represents a habit with its attributes and methods.

        :param name: name of the habit
        :param description: A brief description of the habit.
        :param periodicity: Defines the interval in which the habit is to be completed.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_streak = 0 #is set to zero when creating a instance of the habit class
        self.last_increment_date = None #is set to None when creating a instance of the habit class

    def increment_streak(self, db, increment_date=None):
        """
        Increment or reset the streak based on the increment data and periodicity.
        Calls increment_habit() which updates the habits and increments table.
        :param db: The database connection object.
        :param increment_date: Optional parameter that can be used to write unit test. Otherwise it is set to the current date.
        """
        if increment_date is None:
            increment_date = datetime.now()

        if not self.last_increment_date: #if the habit was not completed before the streak is set to one
            self.current_streak = 1
        else:
            time_difference = increment_date.date() - self.last_increment_date.date()
            if self.periodicity.lower() == "daily" and time_difference == timedelta(days=1): #checks if it was incremented one day before day (date time does not matter)
                self.current_streak += 1
            elif self.periodicity.lower() == "weekly" and time_difference == timedelta(weeks=1): #checks if the last increment was one week ago (date time does not matter)
                self.current_streak += 1 #increases the current streak by 1
            else:
                self.current_streak = 1  #otherwise the streak is reset to 1

        self.last_increment_date = increment_date

        increment_habit(db, self.name, increment_date.strftime("%Y-%m-%d %H:%M:%S"), self.current_streak) #persists the changes in db


    def load(db, name):
        """
        Loads habit data for a requested habit from database and initializes a Habit object with it.
        :param db: The database connection object.
        :param name: Name of the requested Habit object.
        :return: A Habit object.
        """
        data = load_habit(db, name)
        habit = Habit(data["name"], data["description"], data["periodicity"])
        habit.current_streak = data["current_streak"]
        habit.last_increment_date = datetime.strptime(data["last_increment_date"], "%Y-%m-%d %H:%M:%S") if data["last_increment_date"] else None
        return habit

    def add(self, db):
        """
        Inserts habit's details into database by calling the corresponding function from the db module.
        :param db: The database connection object.
        :return: True if the habit is successfully added to the database.
        """
        add_habit(db, self.name, self.description, self.periodicity, self.created_at)
        return True

    def delete(db, name):
        """
        Deletes data for a given habit from database by calling the corresponding function in the db module.
        :param db: The database connection object.
        :param name: The name of the habit to be deleted.
        :return: None
        """
        delete_habit(db, name)