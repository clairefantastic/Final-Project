""" A command line task manager program """

from datetime import datetime
from typing import Optional
import uuid
import pickle
import argparse

class Task:
    """Representation of a task
  
    Attributes:
        - created - date
        - completed - date
        - name - string
        - unique id - string
        - priority - int value of 1, 2, or 3; 1 is default
        - due date - date, this is optional
    """
    def __init__(self, name: str, priority: int=1, due_date: Optional[datetime]=None):
        self.created = datetime.now()
        # Complete time should be None when initialize
        self.completed = None
        self.name = name
        # Random uuid string
        self.unique_id = uuid.uuid4()
        # Priority default to 1
        self.priority = priority
        # Due date is optional
        self.due_date = due_date
    
    # Call the function when task completed
    def completed_task(self):
        self.completed = datetime.now()


class Tasks:
    """A list of `Task` objects."""
   
    def __init__(self):
        """Read pickled tasks file into a list"""
        try:
            with open('.todo.pickle', 'rb') as pickle_file:
                try:
                    self.tasks = pickle.load(pickle_file)
                # Pickle file is empty
                except EOFError:
                    self.tasks = []
        # Find no pickle file
        except FileNotFoundError:
            self.tasks = []

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle', 'wb') as pickle_file:
            pickle.dump(self.tasks, pickle_file)
    
    def print_tasks(self, tasks):
        """ Print tasks for list and query """
        # Print the labels, <n save n spaces for the format
        print(f"{'ID':<8} {'Age':<4} {'Due Date':<10} {'Priority':<10} {'Task'}")
        print(f"{'-'*8:<8} {'---':<4} {'-'*10:<10} {'-'*10:<10} {'-'*8}")

        for task in tasks:
            # Calculate the age
            age = (datetime.now() - task.created).days
            age_string = f"{age}d"
            # Assign the task due date
            if task.due_date:
                due_date_string = task.due_date
            else:
                due_date_string = "-"
            # Print the tasks
            # Leave only the first 8 digit of the id
            print(f"{str(task.unique_id)[:8]:<8} {age_string:<4} {due_date_string:<10} {task.priority:<10} {task.name}")

    def list(self):
        """ List all uncompleted tasks """
        # List comprehension
        uncompleted_tasks = [task for task in self.tasks if task.completed is None]
        # Sort by due date, if having the same due date or no, sort by decreasing priority
        uncompleted_tasks.sort(key=lambda x: (x.due_date is None, x.due_date, x.priority))
        
        self.print_tasks(uncompleted_tasks)

    def report(self):
        """ List all the tasks """
        # Sort by due date, if having the same due date or no, sort by decreasing priority
        self.tasks.sort(key=lambda x: (x.due_date is None, x.due_date, x.priority))
        
        # Print the labels, <n save n spaces for the format
        print(f"{'ID':<8} {'Age':<4} {'Due Date':<10} {'Priority':<10} {'Task':<16} {'Created':<19} {'Completed':<19}")
        print(f"{'-'*8:<8} {'---':<4} {'-'*10:<10} {'-'*10:<10} {'-'*8:<16} {'-'*19:<19} {'-'*19:<19}")

        for task in self.tasks:
            # Calculate the age
            age = (datetime.now() - task.created).days
            age_string = f"{age}d"
            # Assign the task due date
            if task.due_date:
                due_date_string = task.due_date
            else:
                due_date_string = "-"
            created_string = f"{task.created}"
            if task.completed:
                completed_string = f"{task.completed}"
            else:
                completed_string = "-"
            # Print the tasks
            # Leave only the first 8 digit of the id
            print(f"{str(task.unique_id)[:8]:<8} {age_string:<4} {due_date_string:<10} {task.priority:<10} {task.name:<16} {created_string[:19]:<19} {completed_string[:19]:<19}")

    def done(self, unique_id):
        """ Find the task and complete it with giving it a completed time """
        for task in self.tasks:
            if task.unique_id == uuid.UUID(unique_id):
                task.completed_task()
                print(f"Completed task {unique_id}")
                return
        print(f"No task found with ID {unique_id}.")

    def query(self, terms):
        """ Find the tasks that matches the query terms """
        results = []
        # List comprehension
        uncompleted_tasks = [task for task in self.tasks if task.completed is None]
        # Sort by due date, if having the same due date or no, sort by decreasing priority
        uncompleted_tasks.sort(key=lambda x: (x.due_date is None, x.due_date, x.priority))
        
        for task in uncompleted_tasks:
            for term in terms:
                if term.lower() in task.name.lower():
                    results.append(task)
        
        self.print_tasks(results)

    def add(self, name, priority=1, due_date=None):
        """ Add task to tasks list """
        # Check the user input type valid
        if not name or not isinstance(name, str):
            print('There was an error in creating your task. Run "todo -h" for usage instructions.')
            return
            
        # Create the new task instance
        task = Task(name, priority, due_date)
        # Append the task to tasks
        self.tasks.append(task)
        # Print the created task message
        print(f'Created task {task.unique_id}')
        
    def delete(self, unique_id):
        """ Find the id matches and delete it """
        for task in self.tasks:
            if task.unique_id == uuid.UUID(unique_id):
                self.tasks.remove(task)
                print(f"Deleted task {unique_id}")
                return
        print(f"No task found with ID {unique_id}.")

def main():
    parser = argparse.ArgumentParser(description="Update your ToDo List.")
    
    # Add the arguments
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1')
    parser.add_argument('--due', type=str, required=False, help='due date in dd/MM/YYYY format')
    parser.add_argument('--query', type=str, required=False, nargs='+', help='query the task')
    parser.add_argument('--list', action='store_true', required=False, help='list all tasks that have not been completed')
    parser.add_argument('--done', type=str, required=False, help='complete a task with its id')
    parser.add_argument('--delete', type=str, required=False, help='delete a task with its id')
    parser.add_argument('--report', action='store_true', required=False, help='list all tasks that have not been completed')
    
    
    # Parse the arguments
    args = parser.parse_args()
    
    tasks = Tasks()
    
    if args.add:
        tasks.add(args.add, args.priority, args.due)
    elif args.list:
        tasks.list()
    elif args.query:
        tasks.query(args.query)
    elif args.done:
        tasks.done(args.done)
    elif args.delete:
        tasks.delete(args.delete)
    elif args.report:
        tasks.report()
        
    tasks.pickle_tasks()
    exit()

if __name__ == "__main__":
    main()
