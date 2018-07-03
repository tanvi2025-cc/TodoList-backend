# Importing libraries
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import sqlalchemy
from models import Tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import status
from datetime import datetime

# Creating session
engine = create_engine(
    'sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
'''
Subclass of Request Handler
Handling User request for regster
'''
class TasksHandler(tornado.web.RequestHandler):
    # Create a task
    def post(self):
        taskname = self.get_argument('tasks_name')
        deadline = self.get_argument('tasks_deadline')
        print(taskname)
        print(deadline)
        # self.write(dict(taskname=task_name),dict(deadline=tasks_deadline))
        task = Tasks(tasks_name=taskname,
                     tasks_deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        print(task)
        session.add(task)
        session.commit()
        response = {
            'taskname': taskname,
            'deadline': deadline
        }
        self.write(response)

# Retrieve all tasks

    def get(self):
        tasks = session.query(Tasks).all()
        response = {
            'tasks': 'Got it'
        }
        print(tasks)
        self.write(response)

# Delete all tasks

    def delete(self):
        tasks = session.query(Tasks).all()
        tasks.delete()
        self.write(response)

