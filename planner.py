import json
import os
import sys

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            try:
                tasks = json.load(f)
                if isinstance(tasks, list):
                    return tasks
                return []
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "completed": False})
    save_tasks(tasks)
    print(f"Added task: {title}")

def done_task(index):
    tasks = load_tasks()
    try:
        # User index is 1-based
        idx = int(index) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = not tasks[idx].get("completed", False)
            save_tasks(tasks)
            status = "completed" if tasks[idx]["completed"] else "incomplete"
            print(f"Task {index} marked as {status}.")
        else:
            print(f"Error: Task index {index} out of range.")
    except ValueError:
        print(f"Error: Invalid task index '{index}'.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        status = "[x]" if task.get("completed") else "[ ]"
        title = task.get("title", "No Title")
        print(f"{i}. {status} {title}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python planner.py [add 'task name' | list | done <index>]")
        return

    command = sys.argv[1].lower()
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task title.")
        else:
            add_task(sys.argv[2])
    elif command == "list":
        list_tasks()
    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: Please provide a task index.")
        else:
            done_task(sys.argv[2])
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
