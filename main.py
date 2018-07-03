# Im porting libraries
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import sqlalchemy
from models import User, Tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import status
from datetime import datetime
from users import UserHandler
from tasks import TasksHandler,IdHandler
# Creating session
engine = create_engine(
    'sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    app = tornado.web.Application(
        handlers=[(r'/register', UserHandler),
                  (r'/tasks',TasksHandler),
                  (r'/tasksid',IdHandler)]

        #template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    portNumber = str(8888)
    app.listen(portNumber)
    tornado.ioloop.IOLoop.instance().start()



# routes should be RESTful
#authentication
#test cases
#Jsonify in models
