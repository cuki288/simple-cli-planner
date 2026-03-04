import unittest
import os
import json
import planner

# Use a separate test file to avoid messing up real data
planner.TASKS_FILE = 'test_tasks.json'

class TestPlanner(unittest.TestCase):

    def setUp(self):
        # Clear the file before each test
        if os.path.exists(planner.TASKS_FILE):
            os.remove(planner.TASKS_FILE)

    def tearDown(self):
        # Remove the file after each test
        if os.path.exists(planner.TASKS_FILE):
            os.remove(planner.TASKS_FILE)

    def test_add_task(self):
        planner.add_task("Test task 1")
        tasks = planner.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Test task 1")

    def test_list_tasks(self):
        planner.add_task("Task A")
        planner.add_task("Task B")
        tasks = planner.load_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["title"], "Task A")
        self.assertEqual(tasks[1]["title"], "Task B")

    def test_done_task(self):
        planner.add_task("Incomplete Task")
        tasks = planner.load_tasks()
        self.assertFalse(tasks[0]["completed"])
        
        # Mark as done
        planner.done_task("1")
        tasks = planner.load_tasks()
        self.assertTrue(tasks[0]["completed"])
        
        # Toggle back to incomplete
        planner.done_task("1")
        tasks = planner.load_tasks()
        self.assertFalse(tasks[0]["completed"])

    def test_load_tasks_corrupted_json(self):
        # Write corrupted JSON
        with open(planner.TASKS_FILE, 'w') as f:
            f.write("not a json")
        tasks = planner.load_tasks()
        self.assertEqual(tasks, [])

    def test_load_tasks_not_a_list(self):
        # Write JSON that is an object, not a list
        with open(planner.TASKS_FILE, 'w') as f:
            f.write('{"key": "value"}')
        tasks = planner.load_tasks()
        self.assertEqual(tasks, [])

    def test_list_tasks_missing_title(self):
        # Manually add a task without a title
        tasks = [{"completed": False}]
        planner.save_tasks(tasks)
        # Should not raise KeyError
        planner.list_tasks()

if __name__ == '__main__':
    unittest.main()
