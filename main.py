# Im porting libraries
import uuid
from datetime import datetime
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Users.handlers import UserHandler
from Tasks.handlers import TasksHandler
from authentication import LoginHandler

#Creating session
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    app = tornado.web.Application(
        handlers=[(r'/user', UserHandler),
                  (r'/user/([-0-9-a-z])', UserHandler),
                  (r'/tasks', TasksHandler),
                  (r'/tasks/([-0-9-a-z])', TasksHandler),
                  (r'/login', LoginHandler),
                 ]
    )
    portNumber = str(8888)
    app.listen(portNumber)
    tornado.ioloop.IOLoop.instance().start()



