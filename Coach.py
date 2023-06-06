import datetime
import random
# Function to load pending tasks from the data file
def load_pending_tasks():
    try:
        with open("data.txt", "r") as file:
            tasks = file.readlines()
        tasks = [task.strip() for task in tasks]
        return tasks
    except FileNotFoundError:
        return []

# Function to save pending tasks to the data file
def save_pending_tasks(tasks):
    with open("data.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Function to load progress from the progress file
def load_progress():
    try:
        with open("progress.txt", "r") as file:
            progress = file.read().strip()
            if progress:
                return int(progress)
            else:
                return 0
    except FileNotFoundError:
        return 0


# Function to save progress to the progress file
def save_progress(progress):
    with open("progress.txt", "w") as file:
        file.write(str(progress))

# Function to calculate Goggins points based on completion time
def calculate_goggins_points(completion_time):
    current_time = datetime.datetime.now()
    time_difference = current_time - completion_time

    if time_difference <= datetime.timedelta(hours=3):
        return 1000
    elif time_difference <= datetime.timedelta(days=1):
        return 400
    else:
        return 0

# Function to display achievements based on Goggins points
def display_achievements(progress):
    if progress >= 20000:
        print("Congratulations! You have achieved Goggins' Praise.")
    else:
        print(f"Keep going! Your progress: {progress} Goggins points.")

def fetch_random_paragraph():
    with open("goggins.txt", "r") as file:
        paragraphs = file.read().split("\n\n")  # Assumes paragraphs are separated by two newlines
        random_paragraph = random.choice(paragraphs)
        formatted_paragraph = random_paragraph.replace("\n", ".\n")
        return formatted_paragraph


def main():
    # Fetch a random paragraph from the goggins.txt file
    paragraph = fetch_random_paragraph()
    print(paragraph)

    # Load pending tasks and progress
    tasks = load_pending_tasks()
    progress = load_progress()

    # Process pending tasks
    if tasks:
        print("Pending tasks:")
        for task in tasks:
            print(task)

        completion_tasks = []
        for task in tasks:
            completion = input(f"Have you completed the task: {task}? (y/n): ")
            if completion.lower() == "y":
                completion_tasks.append(task)
                points = calculate_goggins_points(datetime.datetime.strptime(task.split('|')[0], '%Y-%m-%d %H:%M:%S'))
                progress += points
                print(f"Congratulations! You earned {points} Goggins points.")

        # Remove completed tasks from pending tasks
        tasks = [task for task in tasks if task not in completion_tasks]

        # Save updated pending tasks and progress
        save_pending_tasks(tasks)
        save_progress(progress)

        # Display achievements
        display_achievements(progress)

    # Add new tasks
    while True:
        new_task = input("Enter a new task (or 'q' to quit): ")
        if new_task.lower() == "q":
            break

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tasks.append(f"{timestamp}|{new_task}")
        save_pending_tasks(tasks)

        print("Task added successfully. Progress and tasks saved.")

    print("All the best with completing tasks. See You soon. Exiting program.")

# Run the main function
if __name__ == "__main__":
    main()
