import questionary
from db import get_db
from habit import Habit
from analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    calculate_longest_streak,
    calculate_longest_streak_all,
)


def cli():
    """
    Command-line interface for the Habit Tracker.
    """
    try:
        db = get_db()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return

    print("Welcome to the Habit Tracker CLI!")
    print("Here you can manage, track, and analyze your current habits.")
    questionary.text("Press Enter to proceed to the main menu... ").ask()

    while True:
        main_choice = questionary.select(
            message="What do you want to do? / Main Menu",
            choices=["Manage habits", "Analyze habits", "Exit"],
        ).ask()

        if main_choice == "Manage habits":
            while True:
                manage_choice = questionary.select(
                    message="Select one of the following options:",
                    choices=[
                        "Add new habit",
                        "Increment existing habit",
                        "Delete existing habit",
                        "Go back",
                    ],
                ).ask()

                if manage_choice == "Add new habit":
                    while True:
                        name = questionary.text("What's the name of your habit?").ask()
                        if name.strip():
                            break
                        print("Habit name cannot be empty. Please provide a valid name.")

                    while True:
                        desc = questionary.text("What's the description of your habit?").ask()
                        if desc.strip():
                            break
                        print("Habit description cannot be empty. Please provide a valid description.")

                    period = questionary.select(
                        message="What is the periodicity of the habit?",
                        choices=["Daily", "Weekly"],
                    ).ask()

                    try:
                        habit = Habit(name, desc, period)
                        if habit.add(db):
                            print(f"Habit '{name}' created successfully.")
                        else:
                            print(f"Failed to create habit '{name}'. It might already exist.")
                    except Exception as e:
                        print(f"Database error while adding habit: {e}")

                elif manage_choice == "Increment existing habit":
                    name = questionary.text("What's the name of your habit?").ask()
                    try:
                        habit = Habit.load(db, name)
                        habit.increment_streak(db)
                        print(f"Habit '{habit.name}' incremented successfully to {habit.current_streak}.")
                    except ValueError:
                        print(f"Error: Habit '{name}' does not exist.")
                    except Exception as e:
                        print(f"Database error while incrementing habit: {e}")

                elif manage_choice == "Delete existing habit":
                    name = questionary.text("Enter the name of the habit to delete: ").ask()
                    try:
                        habit = Habit.load(db, name)
                        confirm = questionary.confirm(
                            f"Are you sure you want to delete the habit '{habit.name}' and all its data? This action cannot be undone."
                        ).ask()

                        if confirm:
                            Habit.delete(db, name)
                            print(f"Habit '{name}' and its associated events have been deleted.")
                        else:
                            print("Habit deletion cancelled.")
                    except ValueError:
                        print(f"Error: Habit '{name}' does not exist.")
                    except Exception as e:
                        print(f"Database error while deleting habit: {e}")

                elif manage_choice == "Go back":
                    break

        elif main_choice == "Analyze habits":
            while True:
                analysis_choice = questionary.select(
                    message="Choose an analysis option:",
                    choices=[
                        "Show all tracked habits",
                        "Show all daily habits",
                        "Show all weekly habits",
                        "Show longest streak for a specific habit",
                        "Show longest streak across all habits",
                        "Go back",
                    ],
                ).ask()

                if analysis_choice == "Show all tracked habits":
                    try:
                        all_habits = get_all_habits(db)
                        if all_habits:
                            print("Tracked habits:")
                            for habit in all_habits:
                                print(
                                    f"Habit: {habit['name']}, Periodicity: {habit['periodicity']}, Current Streak: {habit['current_streak']}"
                                )
                        else:
                            print("No habits are currently being tracked.")
                    except Exception as e:
                        print(f"Database error while fetching tracked habits: {e}")

                elif analysis_choice == "Show all daily habits":
                    try:
                        daily_habits = get_habits_by_periodicity(db, "daily")
                        if daily_habits:
                            print("Daily habits:")
                            for habit in daily_habits:
                                print(f" - {habit}")
                        else:
                            print("No daily habits are currently being tracked.")
                    except Exception as e:
                        print(f"Database error while fetching daily habits: {e}")

                elif analysis_choice == "Show all weekly habits":
                    try:
                        weekly_habits = get_habits_by_periodicity(db, "weekly")
                        if weekly_habits:
                            print("Weekly habits:")
                            for habit in weekly_habits:
                                print(f" - {habit}")
                        else:
                            print("No weekly habits are currently being tracked.")
                    except Exception as e:
                        print(f"Database error while fetching weekly habits: {e}")

                elif analysis_choice == "Show longest streak for a specific habit":
                    habit_name = questionary.text("Enter the name of the habit: ").ask()
                    try:
                        longest_streak = calculate_longest_streak(db, habit_name)
                        print(f"The longest streak for habit '{habit_name}' is {longest_streak} days.")
                    except ValueError:
                        print(f"Error: Habit '{habit_name}' does not exist.")
                    except Exception as e:
                        print(f"Database error while fetching the longest streak: {e}")

                elif analysis_choice == "Show longest streak across all habits":
                    try:
                        longest_streak_habit = calculate_longest_streak_all(db)
                        if longest_streak_habit:
                            print(f"The habit with the longest streak is '{longest_streak_habit['habit']}' with a streak of {longest_streak_habit['longest_streak']} days.")
                        else:
                            print("No data available for habit streaks.")
                    except Exception as e:
                        print(f"Database error while fetching the longest streak across all habits: {e}")

                elif analysis_choice == "Go back":
                    break

        elif main_choice == "Exit":
            print("Thanks for using the Habit Tracker CLI.")
            break


if __name__ == "__main__":
    cli()
