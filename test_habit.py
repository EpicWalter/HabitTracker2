"""
This module groups all the unit tests for the habit class.
"""

from datetime import datetime, timedelta
from conftest import test_db
from db import add_habit
from habit import Habit
import sqlite3
import pytest


def test_increment_streak_no_last_date(test_db):
    #"Water the Plants" has no last_increment_date initially
    habit = Habit.load(test_db, "Water the Plants")
    assert habit.last_increment_date is None #implicitly also tests the load() method
    assert habit.current_streak == 0

    #current_increment should now be 1
    habit.increment_streak(test_db)
    assert habit.current_streak == 1
    assert habit.last_increment_date is not None

def test_increment_streak_daily_exact_one_day(test_db):
    #"Read a Book" currently has a last_increment_date and a streak of 2
    habit = Habit.load(test_db, "Read a Book")
    assert habit.current_streak == 2

    #last_increment_date is "2024-01-02 07:00:00"
    last_inc_date = habit.last_increment_date
    next_day = last_inc_date + timedelta(days=1)  #exactly one day later

    habit.increment_streak(test_db, increment_date=next_day)
    #Streak should now be 3 if daily and incremented exactly after one day
    assert habit.current_streak == 3


def test_increment_streak_daily_too_early(test_db):
    #"Read a Book" after previous test is at streak 2 and incremented last on next_day
    habit = Habit.load(test_db, "Read a Book")
    current_streak = habit.current_streak
    assert current_streak == 2

    #incrementing on the same date/time again (too early)
    habit.increment_streak(test_db, increment_date=habit.last_increment_date)
    #Streak should reset to 1 since no day difference
    assert habit.current_streak == 1


def test_increment_streak_daily_too_late(test_db):
    #incrementing after more than one day should reset to 1.
    habit = Habit.load(test_db, "Morning Jog")
    #Current streak value is 1
    last_inc_date = habit.last_increment_date
    two_days_later = last_inc_date + timedelta(days=2)

    habit.increment_streak(test_db, increment_date=two_days_later)
    #More than one day gap means reset to 1
    assert habit.current_streak == 1


def test_increment_streak_weekly_exact_one_week(test_db):
    # "Review Finances" has a streak of 3, last increment was exactly one week before
    habit = Habit.load(test_db, "Review Finances")
    assert habit.periodicity.lower() == "weekly"
    assert habit.current_streak == 3

    # Increment exactly one week later
    last_inc_date = habit.last_increment_date
    one_week_later = last_inc_date + timedelta(weeks=1)

    habit.increment_streak(test_db, increment_date=one_week_later)
    #Streak should now be 4 because it's exactly a week apart
    assert habit.current_streak == 4


def test_increment_streak_weekly_too_early(test_db):
    # "Call Parents" was incremented once and is weekly
    habit = Habit.load(test_db, "Call Parents")
    assert habit.current_streak == 1

    # Now increment after just a few days, not a full week
    last_inc_date = habit.last_increment_date
    too_early = last_inc_date + timedelta(days=2)
    habit.increment_streak(test_db, increment_date=too_early)
    # Streak resets to 1 since not a full week apart
    assert habit.current_streak == 1


def test_increment_streak_weekly_too_late(test_db):
    # Incrementing after more than one week should reset to 1.
    habit = Habit.load(test_db, "Call Parents")
    current_streak = habit.current_streak

    # Increment after 2 weeks
    too_late = habit.last_increment_date + timedelta(weeks=2)
    habit.increment_streak(test_db, increment_date=too_late)
    # Streak resets to 1 because the gap is more than one week
    assert habit.current_streak == 1


def test_add_habit(test_db):
    #Create a Habit instance
    habit = Habit(name="Evening Walk", description="Go for a 15-minute walk every evening", periodicity="Daily",)

    #Add the habit to the database
    assert habit.add(test_db) is True

    # Verify the habit exists in the database
    cur = test_db.cursor()
    cur.execute("SELECT * FROM habits WHERE name = ?", ("Evening Walk",))
    result = cur.fetchone()

    assert result is not None
    assert result[0] == "Evening Walk"
    assert result[1] == "Go for a 15-minute walk every evening"


def test_delete_habit(test_db):
    # Add a habit to the database to set up the test
    add_habit(
        test_db,
        "Morning Run",
        "Run for 20 minutes every morning",
        "Daily",
        "2024-01-10 07:00:00"
    )

    # Verify the habit exists in the database before deletion
    cur = test_db.cursor()
    cur.execute("SELECT * FROM habits WHERE name = ?", ("Morning Run",))
    result = cur.fetchone()
    assert result is not None

    # Delete the habit
    Habit.delete(test_db, "Morning Run")

    #Verify the habit no longer exists in the database
    cur.execute("SELECT * FROM habits WHERE name = ?", ("Morning Run",))
    result = cur.fetchone()
    assert result is None