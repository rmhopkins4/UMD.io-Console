import calendar
import requests
import os
import json
from datetime import datetime

day_map = {
    'M': ['Monday'],
    'Tu': ['Tuesday'],
    'W': ['Wednesday'],
    'Th': ['Thursday'],
    'F': ['Friday'],
    'MW': ['Monday', 'Wednesday'],
    'MTh': ['Monday', 'Thursday'],
    'MF': ['Monday', 'Friday'],
    'TuW': ['Tuesday', 'Wednesday'],
    'TuTh': ['Tuesday', 'Thursday'],
    'TuF': ['Tuesday', 'Friday'],
    'WTh': ['Wednesday', 'Thursday'],
    'WF': ['Wednesday', 'Friday'],
    'ThF': ['Thursday', 'Friday'],
    'MTuW': ['Monday', 'Tuesday', 'Wednesday'],
    'MTuTh': ['Monday', 'Tuesday', 'Thursday'],
    'MTuF': ['Monday', 'Tuesday', 'Friday'],
    'MWTh': ['Monday', 'Wednesday', 'Thursday'],
    'MWF': ['Monday', 'Wednesday', 'Friday'],
    'TuWTh': ['Tuesday', 'Wednesday', 'Thursday'],
    'TuWF': ['Tuesday', 'Wednesday', 'Friday'],
    'WThF': ['Wednesday', 'Thursday', 'Friday'],
    'MTuWTh': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
    'MTuWF': ['Monday', 'Tuesday', 'Wednesday', 'Friday'],
    'MWThF': ['Monday', 'Wednesday', 'Thursday', 'Friday'],
    'TuWThF': ['Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'MTuWThF': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
}

# Create the initial schedule
schedule = {}


def get_schedule_commands(*args):

    if len(args) >= 1:
        tokens = args
    else:

        print("""
    Schedule commands:
        view                View current schedule
        add                 Add a course to the schedule and view the revised schedule
        remove              Remove a course from the schedule
        save                Save the schedule 
        load                Load a saved schedule
        end                 Exit the schedule builder
        """)

        user_input = input("    Enter a schedule command: ")
        tokens = user_input.split()

        if len(tokens) < 1:
            get_schedule_commands()
            return

    command = tokens[0]

    # view
    if command == 'view':
        # Validate command
        if len(tokens) > 1:
            print(f"Invalid arguments: {tokens[1:]}. Try 'view'")
            return

        # Call the function to display the schedule
        print_schedule()

    # add <course_id> <section_number>
    elif command == 'add':
        # Validate command
        if len(tokens) != 3:
            print(f"Invalid command. Try 'add <course_id> <section_number>")
            return

        # Call the function to add to the schedule and then view it.
        add_section_info(tokens[1], tokens[2])
        print_schedule()

    # remove <course_id>
    elif command == 'remove':
        # Validate command
        if len(tokens) != 2:
            print(f"Invalid command. Try 'remove <course_id>'")
            return

        # Call the function to remove from the schedule.
        remove_course(tokens[1])

    # save
    elif command == 'save':
        # Validate command
        if len(tokens) > 2:
            print(f"Invalid arguments: {tokens[1:]}. Try 'save [<filename>]'")
            return

        # Call function to save schedule
        if len(tokens) > 1:
            save_schedule(filename=tokens[1])
        else:
            save_schedule()

    # load
    elif command == 'load':
        # Validate command
        if len(tokens) > 1:
            print(f"Invalid arguments: {tokens[1:]}. Try 'load'")
            return

        # Call function to load schedule
        schedule = load_schedule()

    # end
    elif command == 'end':
        print("    Exiting schedule builder. \n")
        return

    else:
        print('Invalid command.\n')
        get_schedule_commands()


def save_schedule(filename=datetime.now().strftime("%Y-%m-%d")):
    script_dir = os.path.dirname(os.path.abspath(
        __file__))  # Get the script directory
    # Save schedules relative to the script location
    directory = os.path.join(script_dir, 'schedules')
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as file:
        json.dump(schedule, file)
    print(f"    Schedule saved to {filename}!\n")


def load_schedule():
    script_dir = os.path.dirname(os.path.abspath(
        __file__))  # Get the script directory
    # Load schedules relative to the script location
    directory = os.path.join(script_dir, 'schedules')
    files = os.listdir(directory)

    if not files:
        print("No schedules found.")
        return

    print("\n       Available schedules:")
    for i, filename in enumerate(files):
        print(f"            {i+1}. {filename}")

    selection = input(
        "\n       Enter the number of the schedule to load (or 'cancel' to cancel): ")
    if selection.lower() == 'cancel':
        return

    try:
        index = int(selection) - 1
        filename = files[index]
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            loaded_data = json.load(file)

            # clear schedule
            schedule.clear()
            # reload schedule
            # Convert keys to integers
            schedule.update({int(k): v for k, v in loaded_data.items()})
            print(f"       Loaded schedule {filename}!\n")

    except (ValueError, IndexError):
        print("Invalid selection.")
        return


def convert_time_to_schedule(time_str):
    time_parts = time_str.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1][:2])
    period = time_parts[1][2:].lower()

    if period == 'pm' and hour != 12:
        hour += 12
    elif period == 'am' and hour == 12:
        hour = 0

    return hour * 12 + minute // 5


def print_schedule(schedule=schedule):
    print("  Time  |  Monday   |  Tuesday  | Wednesday | Thursday  |  Friday   | Saturday  | Sunday ")
    print("--------+-----------+-----------+-----------+-----------+-----------+-----------+--------")

    # Find the first and last event times
    event_times = schedule.keys()
    first_event_time = min(event_times) if event_times else 0
    last_event_time = max(event_times) if event_times else 0

    for time in range(first_event_time, last_event_time + 1):
        time_formatted = f"{time // 12:02d}:{(time % 12) * 5:02d}"
        events = schedule.get(time, {})
        event_strings = []

        for day in calendar.day_name:
            event = events.get(day, "")
            truncated_event = event[:9] if len(event) > 9 else event
            event_strings.append(truncated_event.ljust(9))

        print(f" {time_formatted}  | {' | '.join(event_strings)} ")
    print("")


def add_event(schedule, day, start_time, end_time, event):
    # Convert time_str to digit
    start_time = convert_time_to_schedule(start_time)
    end_time = convert_time_to_schedule(end_time)

    for time in range(start_time, end_time + 1):
        if time not in schedule:
            schedule[time] = {}
        if day not in schedule[time]:
            schedule[time][day] = event


def add_section_info(course_id, section_id):
    # Construct the URL to retrieve the section information
    url = f'https://api.umd.io/v1/courses/{course_id}/sections/{section_id}'

    response = requests.get(url)

    if response.status_code == 200:
        section_info = response.json()[0]

        course = section_info['course']
        meetings = section_info['meetings']
        for meeting in meetings:
            days = meeting['days']
            start_time = meeting['start_time']
            end_time = meeting['end_time']
            for day in day_map.get(days):
                add_event(schedule, day, start_time, end_time, course)

    else:
        print('Error occurred while retrieving section information:',
              response.status_code)


def remove_course(course_id):
    keys_to_remove = []
    for key, value in schedule.items():
        for day, course in value.items():
            if course.lower() == course_id.lower():
                keys_to_remove.append((key, day))

    for key, day in keys_to_remove:
        del schedule[key][day]

    if keys_to_remove:
        print(f'Removed course: {course_id.upper()}\n')
    else:
        print(f'Course does not exist!\n')
