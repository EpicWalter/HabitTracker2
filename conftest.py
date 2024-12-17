"""
The conftest module defines the fixtures for the unit tests in pytest. The actual test cases are organized in separate files.

Everything before yield statement represents the setup phase incl. db setup, adding habits and increments.
Unit test are executed after the setup phase
Everything after the yield statement represents the teardown phase.

"""

import pytest
from db import get_db, add_habit, increment_habit

@pytest.fixture
#setup phase
def test_db():
    test_db = get_db(":memory:")

    add_habit(test_db, "Morning Jog", "Go for a 30-minute run every morning", "Daily", "2024-01-01 09:00:00","2024-01-01 09:00:00")
    add_habit(test_db, "Read a Book", "Read 10 pages of a book daily", "Daily", "2024-01-01 09:00:00", "2024-01-02 07:00:00")
    add_habit(test_db, "Water the Plants", "Water indoor plants weekly", "Weekly", "2024-01-01 09:00:00")
    add_habit(test_db, "Review Finances", "Check bank accounts weekly", "Weekly", "2024-01-01 09:00:00","2024-01-15 10:00:00")
    add_habit(test_db, "Call Parents", "Have a weekly call with parents", "Weekly", "2024-01-01 09:00:00", "2024-01-04 21:00:00")

    #only "Read a Book" and "Review Finances" were already incremented
    increment_habit(test_db, "Morning Jog", "2024-01-01 09:00:00", 1)
    increment_habit(test_db, "Read a Book", "2024-01-01 07:00:00", 1)
    increment_habit(test_db, "Read a Book", "2024-01-02 07:00:00", 2)
    increment_habit(test_db, "Review Finances", "2024-01-01 10:00:00", 1)
    increment_habit(test_db, "Review Finances", "2024-01-08 10:00:00", 2)
    increment_habit(test_db, "Review Finances", "2024-01-15 10:00:00", 3)
    increment_habit(test_db, "Call Parents", "2024-01-04 21:00:00", 1)


    yield test_db
    #teardown phase
    test_db.close()