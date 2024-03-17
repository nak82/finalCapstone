"""Capstone Project -
Lists, Functions,
and String Handling"""

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user(username_password):
    # Add a new user to the user.txt file
    new_username = input("New Username: ")

    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
        return

    # Request input of a new password
    new_password = input("New Password: ")

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")

def add_task(task_list, username_password):
    '''Allow a user to add a new task to task.txt file'''
    # Prompt a user for the following:
    # - A username of the person whom the task is assigned to,
    # - A title of a task,
    # - A description of the task, and
    # - the due date of the task.
    task_username = input("Name of person assigned to task: ")

    # Check if the user exists
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date.
    curr_date = date.today()

    # Add the data to the file task.txt and include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all(task_list):
    # Reads the tasks from tasks.txt file and prints to the console
    for idx, t in enumerate(task_list, start=1):
        disp_str = f"Task {idx}:\n"
        disp_str += f"Title: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"  # Added this line
        print("*" * 30)
        print(disp_str)


def edit_task(task):
    print("Editing Task:")
    print("1. Edit Username")
    print("2. Edit Due Date")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        new_username = input("Enter the new username: ")
        task['username'] = new_username
        print("Username updated successfully.")
    elif choice == '2':
        new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
        try:
            due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            task['due_date'] = due_date_time
            print("Due date updated successfully.")
        except ValueError:
            print("Invalid date format. Please use the format specified.")
    else:
        print("Invalid choice.")

def view_mine(task_list, curr_user):
    '''Reads the tasks from task.txt file and prints to the console,
    showing only tasks assigned to the current user'''
    for idx, task in enumerate(task_list, start=1):
        if task['username'] == curr_user:
            disp_str = f"Task {idx}:\n"
            disp_str += f"Title: \t\t {task['title']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task['description']}\n"
            disp_str += f"Completed: \t {'Yes' if task['completed'] else 'No'}\n"
            print("*" * 30)
            print(disp_str)

            action = input("Enter 'c' to mark the task as complete, 'e' to edit, or any other key to skip: ").lower()

            if action == 'c':
                if not task['completed']:
                    task['completed'] = True
                    print("Task marked as complete.")
                    save_tasks_to_file(task_list)
                else:
                    print("Task is already marked as complete.")
            elif action == 'e':
                if not task['completed']:
                    edit_task(task)
                    save_tasks_to_file(task_list)
                else:
                    print("Cannot edit a completed task.")

def save_tasks_to_file(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def display_statistics(username_password, task_list):
    '''Display statistics about the number of users and tasks'''
    num_users = len(username_password)
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")

    if num_users > 0:
        # Calculate additional statistics if there are users
        num_completed_tasks = sum(task['completed'] for task in task_list)
        num_uncompleted_tasks = num_tasks - num_completed_tasks
        num_overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())
        percentage_incomplete = (num_uncompleted_tasks / num_tasks) * 100
        percentage_overdue = (num_overdue_tasks / num_tasks) * 100

        print("-----------------------------------")
        print(f"Number of completed tasks: \t {num_completed_tasks}")
        print(f"Number of uncompleted tasks: \t {num_uncompleted_tasks}")
        print(f"Number of overdue tasks: \t {num_overdue_tasks}")
        print(f"Percentage of incomplete tasks: \t {percentage_incomplete:.2f}%")
        print(f"Percentage of overdue tasks: \t {percentage_overdue:.2f}%")
    print("-----------------------------------")

def generate_task_report(task_list):
    '''Generate task overview report and save it to task_overview.txt'''
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())
    percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
    percentage_overdue = (overdue_tasks / total_tasks) * 100

    with open("task_overview.txt", "w") as report_file:
        report_file.write(f"Task Overview Report\n")
        report_file.write("-----------------------------------\n")
        report_file.write(f"Total number of tasks: {total_tasks}\n")
        report_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        report_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        report_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        report_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
        report_file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")


def generate_user_report(username_password, task_list):
    '''Generate user overview report and save it to user_overview.txt'''
    num_users = len(username_password)
    num_tasks = len(task_list)

    with open("user_overview.txt", "w") as report_file:
        report_file.write(f"User Overview Report\n")
        report_file.write("-----------------------------------\n")
        report_file.write(f"Total number of users: {num_users}\n")
        report_file.write(f"Total number of tasks: {num_tasks}\n")

        if num_users > 0:
            for username, password in username_password.items():
                user_tasks = [task for task in task_list if task['username'] == username]
                num_user_tasks = len(user_tasks)
                
                report_file.write("-----------------------------------\n")
                report_file.write(f"User: {username}\n")
                report_file.write(f"Total number of tasks assigned: {num_user_tasks}\n")
                
                if num_user_tasks > 0:
                    completed_user_tasks = sum(task['completed'] for task in user_tasks)
                    uncompleted_user_tasks = num_user_tasks - completed_user_tasks
                    overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())
                    percentage_user_incomplete = (uncompleted_user_tasks / num_user_tasks) * 100
                    percentage_user_overdue = (overdue_user_tasks / num_user_tasks) * 100

                    report_file.write(f"Percentage of total tasks assigned: {(num_user_tasks / num_tasks) * 100:.2f}%\n")
                    report_file.write(f"Percentage of tasks completed: {(completed_user_tasks / num_user_tasks) * 100:.2f}%\n")
                    report_file.write(f"Percentage of tasks to be completed: {(uncompleted_user_tasks / num_user_tasks) * 100:.2f}%\n")
                    report_file.write(f"Percentage of tasks overdue: {(overdue_user_tasks / num_user_tasks) * 100:.2f}%\n")
                else:
                    report_file.write("No tasks assigned.\n")

# Displaying a menu for user interaction with various options:
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)
    elif menu == 'a':
        add_task(task_list, username_password)
    elif menu == 'va':
        view_all(task_list)
    elif menu == 'vm':
        view_mine(task_list, curr_user)
    elif menu == 'gr' and curr_user == 'admin':
        generate_task_report(task_list)
        generate_user_report(username_password, task_list)
        print("Reports generated successfully.")
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics(username_password, task_list)
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")

    