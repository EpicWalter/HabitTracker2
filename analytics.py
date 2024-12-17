
"""
The analytics module provides various analytics functions that return data about the users habits.
"""

def get_all_habits(db):
    """
    Retrieve all tracked habits with all their data.
    Returns a list of dictionaries, where each dictionary represents a habit.

    :param db: The database connection object.
    :return: A list of dictionaries, where each dictionary represents a habit with the following keys:
             - "name": The name of the habit.
             - "description": A brief description of the habit.
             - "periodicity": The periodicity of the habit ("Daily" or "Weekly").
             - "created_at": The timestamp when the habit was created.
             - "current_streak": The current streak value of the habit.
             - "last_increment_date": The timestamp of the last increment or None if not set.
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity, created_at, current_streak, last_increment_date FROM habits")
    results = cur.fetchall()
    return [
        {
            "name": row[0],
            "description": row[1],
            "periodicity": row[2],
            "created_at": row[3],
            "current_streak": row[4],
            "last_increment_date": row[5]
        }
        for row in results
    ]


def get_habits_by_periodicity(db, periodicity):
    """
    Retrieve the names of habits filtered by their periodicity from the database.

    :param db: The database connection object.
    :param periodicity: The periodicity to filter habits by (e.g., "daily", "weekly").
    :return: A list of strings, where each string is the name of a habit with the specified periodicity.
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habits WHERE LOWER(periodicity) = ?", (periodicity.lower(),))
    results = cur.fetchall()
    return [row[0] for row in results]

def calculate_longest_streak(db, habit_name):
    """
    Calculates the longest streak for a given habit by querying the increments table to find
    the maximum streak value.

    :param db: The database connection object.
    :param habit_name: The name of the habit for which the longest streak is calculated.
    :return: An integer representing the longest streak for the specified habit.
            Returns 0 if no streak records exist.
    """
    cur = db.cursor()
    cur.execute("SELECT MAX(streak) FROM increments WHERE habitName = ?", (habit_name,))
    result = cur.fetchone()
    return result[0] if result else 0 #unify implementation style with the other functions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



def calculate_longest_streak_all(db):
    """
    Finds the habit(s) with the longest streak across all habits by querying the increments table.

    :param db: The database connection object.
    :return: A list of dictionaries, each containing:
             - "habit": The name of the habit.
             - "longest_streak": The highest streak value recorded for that habit.
             Returns an empty list if no streak data exists in the database.
    """
    cur = db.cursor()
    try: #using WHERE and returning a list of habits allows to handle the case where there is not only one habit with the highest habit streak
        cur.execute("""
            SELECT habitName, streak
            FROM increments
            WHERE streak = (SELECT MAX(streak) FROM increments) 
        """)
        results = cur.fetchall()

        if not results:
            return []  # Return an empty list if no results

        # Access rows as tuples using positional indices
        return [{"habit": row[0], "longest_streak": row[1]} for row in results]

    except Exception as e:
        print(f"Database error while fetching the longest streak across all habits: {e}")
        return []
