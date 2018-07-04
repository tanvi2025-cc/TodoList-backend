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


class TasksHandler(tornado.web.RequestHandler):
    # Create a task
    '''
    Subclass of Request Handler
    Handling User request for register
    '''
    @tornado.web.authenticated
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
            'taskname': task.tasks_name,
            'deadline': str(task.tasks_deadline)
        }
        self.write(response)

# Retrieve all tasks

# Filter tasks by id
    @tornado.web.authenticated
    def get(self, tasks_id=None):
        print('>>>>', tasks_id)
        if tasks_id:
            task = session.query(Tasks).filter(
                Tasks.tasks_id == tasks_id).first()
            print(task)
            self.finish(str(task.as_dict()))
        self.finish("Error")

    # def get(self):
    #     #task_date = self.get_arguments('tasks_deadline')
    #    # tasks = session.query(Tasks).all().filter(Tasks.tasks_deadline==task_date)
    #     task = session.query(Tasks).all()
    #     response = {
    #         'tasks': 'Got it'
    #     }
    #     print(task)
    #     self.finish(response)

# Delete all tasks
    #def delete(self):
        #tasks = session.query(Tasks).all()
        #session.delete(tasks)
        #session.commit()
        #print(tasks)
        #self.write(response)



# Delete tasks by id
    @tornado.web.authenticated
    def delete(self, tasks_id):
        print('>>>>', tasks_id)
        if tasks_id:
            task = session.query(Tasks).filter(
                Tasks.tasks_id == tasks_id).first()
            print(task)
            session.delete(task)
            session.commit()
            print(task)
            self.finish(task.as_dict())
        self.finish("Error")
