#Im porting libraries
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import sqlalchemy
from models import User,Tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import requests
import status

#Creating session 
engine=create_engine('sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session=sessionmaker(bind=engine)
session=Session()

#Controller classes
#Get all user objects
class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        user=session.query(User).all()
        #print(json.load(user))
        response={
            'res':'hello'
        }
        self.write(response)
        self.set_status(status.HTTP_200_OK)
        print(user)

class CreateTasksHandler(tornado.web.RequestHandler):
    #Create a task 
    def post(self):
        taskname=self.get_argument('tasks_name')
        deadline=self.get_argument('tasks_deadline')
        print(taskname)
        print(deadline)
        #self.write(dict(taskname=task_name),dict(deadline=tasks_deadline))
        response={
            'taskname':taskname,
            'deadline':deadline
        }
        self.write(response)
#Retrieve all tasks
class GetTasksHandler(tornado.web.RequestHandler):
    def get(self):
        tasks=session.query(Tasks).all()
        response={
            'tasks':'Got it'
        }
        print(tasks)
        self.write(response)
#Retrieve Tasks by Id
class GetTasksByIdHandler(tornado.web.RequestHandler):
    def get(self,id):
        taskId=int(id)
        if taskId is not in Tasks.tasks_id:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        tasks=session.query(Tasks).get(task_id=taskId)
        response={
            'task':tasks
        }
        self.write(response)

        
#Delete all tasks
class DeleteAllTasksHandler(tornado.web.RequestHandler):
    def delete(self):
        tasks=session.query(Tasks).all()
        tasks.delete()
        response=self.set_status(status.HTTP_200_OK)
        self.write(response)
#Delete tasks by id
class DeleteTasksByIdHandler(tornado.web.RequestHandler):
    def delete(self,id):
        taskId=int(id)
        if taskId is not in Tasks.tasks_id:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        tasks=session.query(Tasks).all().filter(taskId=tasks_id)
        tasks.delete()
        res=self.set_status(status.HTTP_200_OK)
        response={
            'status':res
        }
        self.write(response)
if __name__=="__main__":
    app = tornado.web.Application(
    handlers=[(r'/', GetUserHandler),(r'/tasks',GetTasksHandler)]
    
    #template_path=os.path.join(os.path.dirname(__file__), "templates")
    ) 
    portNumber=str(8888)
    app.listen(portNumber)
    tornado.ioloop.IOLoop.instance().start()
    
