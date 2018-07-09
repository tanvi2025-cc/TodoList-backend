import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from .models import Tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from authentication import validate
from DatabaseConnect.DbConnection import DbConnection


class TasksHandler(DbConnection, tornado.web.RequestHandler):
    '''
    This class is Request Handler class for tasks table
    Methods Used=('GET','POST','DELETE')
    '''

    def validate_taskname(self, tasks_name):
        # Validate tasks
        if not tasks_name:
            self.set_status(400)
            self.finish(dict(error=True, message="Task name is missing"))
        return tasks_name

    def validate_deadline(self, task_deadline):
        # Validate deadlines
        if not task_deadline:
            self.set_status(400)
            self.finish(dict(error=True, message="Deadline is missing"))
        if datetime.strptime(task_deadline, '%Y-%m-%d') < datetime.now():
            self.set_status(400)
            self.finish(
                dict(error=True, message="Date has been already passed"))
        return task_deadline

    # Authenticate request

    @validate
    def post(self):
        '''
        POST request method to add tasks in the database
        '''

        taskname = self.validate_taskname(
            self.get_body_argument('tasks_name', None))
        deadline = self.validate_deadline(
            self.get_body_argument('tasks_deadline',None))

        task = Tasks(tasks_name=taskname,
                     tasks_deadline=datetime.strptime(deadline, '%Y-%m-%d'))

        self.session.add(task)
        self.session.commit()
        response = dict(
            task_id=task.id,
            taskname=task.tasks_name,
            deadline=str(task.tasks_deadline)
        )
        self.finish(response)

    # Authenticate request

    @validate
    def get(self, tasks_id):
        '''
        GET request method to fetch a task by id.
        '''
        if tasks_id:
            task = self.session.query(Tasks).filter(
                Tasks.id == tasks_id).first()
            if not task:
                self.set_status(404)
                self.finish(dict(error=True, message="Task not found"))

            task.tasks_deadline = task.tasks_deadline.isoformat()
            self.finish(task.as_dict())
        else:
            self.finish(dict(error=True, message="Id is not valid"))

    # Authenticate request
    @validate
    def delete(self, tasks_id):
        '''
        DELETE request method to delete a tasks according to it's mapped id.
        '''

        if tasks_id:
            task = self.session.query(Tasks).filter(
                Tasks.id == tasks_id).first()
            if not task:
                self.set_status(404)
                self.finish(dict(error=True, message="Object not found"))

            self.session.delete(task)
            self.session.commit()
            self.finish(dict(error=False, message='Deleted'))
        else:
            self.set_status(400)
            self.finish(dict(error=True,message="Invalid Id"))


class ListTaskHandler(DbConnection, tornado.web.RequestHandler):
    '''
    Request Handler to retrive and delete tasks list.
    Methods Used=('GET','DELETE')
    '''

    # Authenticate request
    @validate
    def get(self):
        '''
        GET request method to fetch list of the tasks.
        '''
        tasks = self.session.query(Tasks).all()
        self.finish(tasks.as_dict())

    # Authenticate request
    @validate
    def delete(self):
        '''
        DELETE request method to delete the list of the tasks.
        '''
        tasks = self.session.query(Tasks).all()
        self.session.delete(tasks)
        self.session.commit()
        self.finish(dict(error=False,status="Deleted Successfully"))
