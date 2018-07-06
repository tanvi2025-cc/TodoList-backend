# Importing libraries
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from .models import Tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import status
from datetime import datetime
from authentication import validate

#create engine
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()


class TasksHandler(tornado.web.RequestHandler):
    # Create a task
    '''
    Subclass of Request Handler
    Handling User request for register
    '''
    @validate
    def post(self):
        # user_name=tornado.escape.xhtml_escape(self.current_user)
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
        response = dict(
            taskname=task.tasks_name,
            deadline=str(task.tasks_deadline)
        )
        self.write(response)

# Retrieve all tasks

# Filter tasks by id
    @validate
    def get(self, tasks_id=None):
        # user_name=tornado.escape.xhtml_escape(self.current_user)
        print('>>>>', tasks_id)
        if tasks_id:
            task = session.query(Tasks).filter(
                Tasks.id == tasks_id).first()
            print(task)
            self.finish(str(task.as_dict()))
        else:
            self.finish("Error")

# Delete tasks by id
    @validate
    def delete(self, tasks_id):
        print('>>>>', tasks_id)
        if tasks_id:
            task = session.query(Tasks).filter(
                Tasks.id == tasks_id).first()
            print(task)
            session.delete(task)
            session.commit()
            print(task)
            self.finish(task.as_dict())
        self.finish("Error")
# Lists and delete all tasks


class ListTaskHandler(tornado.web.RequestHandler):
    @validate
    def get(self):
        tasks = session.query(Tasks).all()
        self.finish(tasks.as_dict())

    @validate
    def delete(self):
        tasks = session.query(Tasks).all()
        session.delete(tasks)
        session.commit()
        self.finish(dict(tasks='Deleted'))
