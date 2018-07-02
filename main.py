#Im porting libraries
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import sqlalchemy
from models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import requests

#Creating session 
engine=create_engine('sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session=sessionmaker(bind=engine)
session=Session()

#Controller class
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        user=(session.query(User).all())
        #print(json.load(user))
        response={
            'res':'hello'
        }
        self.write(response)
        print(user)

class TasksHandler(tornado.web.RequestHandler):
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
         
        

if __name__=="__main__":
    app = tornado.web.Application(
    handlers=[(r'/', MainHandler),(r'/tasks',TasksHandler)]
    
    #template_path=os.path.join(os.path.dirname(__file__), "templates")
    ) 
    portNumber=str(8888)
    app.listen(portNumber)
    tornado.ioloop.IOLoop.instance().start()
    
