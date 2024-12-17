"""
This module groups all the unit tests for the analytics module.
"""

from analytics import get_all_habits, get_habits_by_periodicity, calculate_longest_streak, calculate_longest_streak_all
import pytest

def test_get_all_habits(test_db):
    habits = get_all_habits(test_db)
    # We know from the fixture we added 5 habits
    assert len(habits) == 5

    # Check that each habit has the expected keys
    for habit in habits:
        assert "name" in habit
        assert "description" in habit
        assert "periodicity" in habit
        assert "created_at" in habit
        assert "current_streak" in habit
        assert "last_increment_date" in habit

def test_get_habits_by_periodicity(test_db):
    # Test filtering for daily habits
    daily_habits = get_habits_by_periodicity(test_db, "daily")
    assert len(daily_habits) == 2
    assert "Morning Jog" in daily_habits
    assert "Read a Book" in daily_habits

    # Test filtering for weekly habits
    weekly_habits = get_habits_by_periodicity(test_db, "weekly")
    assert len(weekly_habits) == 3
    assert "Water the Plants" in weekly_habits
    assert "Review Finances" in weekly_habits
    assert "Call Parents" in weekly_habits


def test_calculate_longest_streak(test_db):
    assert calculate_longest_streak(test_db, "Morning Jog") == 1
    assert calculate_longest_streak(test_db, "Read a Book") == 2
    assert calculate_longest_streak(test_db, "Water the Plants") == None #Since it wasn't incremented yet and has no entry in the increments table
    assert calculate_longest_streak(test_db, "Review Finances") == 3
    assert calculate_longest_streak(test_db, "Call Parents") == 1

def test_calculate_longest_streak_all(test_db):

    # The habit with the longest streak should be "Call Parents" with a streak of 4
    result = calculate_longest_streak_all(test_db)
    """
    assert result is not None
    assert result["habit"] == "Review Finances"
    assert result["longest_streak"] == 3
    """
    assert isinstance(result, list)  # Ensure the result is a list
    assert len(result) == 1  # Expect only one habit in the result

    # Verify the habit details
    expected_result = {"habit": "Review Finances", "longest_streak": 3}
    assert result[0] == expected_result  # Verify the result matches the expected output