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
from users import UserHandler, LoginHandler
from tasks import TasksHandler
import base64
import uuid
from authentication import AuthHandler
# Creating session
engine = create_engine(
    'sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

COOKIE_SECRET=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
settings={
    'cookie_secret':COOKIE_SECRET,
    'login_url':'/login'
}
if __name__ == "__main__":
    app = tornado.web.Application(
        handlers=[(r'/user', UserHandler),
                  (r'/user/([-0-9-a-z])', UserHandler),
                  (r'/tasks', TasksHandler),
                  (r'/tasks/([-0-9-a-z])', TasksHandler),
                  (r'/login', LoginHandler),
                  (r'/auth',AuthHandler)],**settings
    )
    portNumber = str(8888)
    app.listen(portNumber)
    tornado.ioloop.IOLoop.instance().start()


# authentication
# test cases
