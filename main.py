import uuid
from datetime import datetime
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from Users.handlers import UserHandler
from Tasks.handlers import TasksHandler, ListTaskHandler
from authentication import LoginHandler

if __name__ == "__main__":
    # Application objects
    app = tornado.web.Application(
        # Routes mapped to handlers
        handlers=[(r'/user', UserHandler),
                  (r'/user/([-0-9]+)', UserHandler),
                  (r'/tasks', TasksHandler),
                  (r'/tasks/([-0-9]+)', TasksHandler),
                  (r'/login', LoginHandler),
                  (r'/tasks/list', ListTaskHandler)
                  ]
    )

    PORT_NUMBER '8000'
    app.listen(PORT_NUMBER)
    tornado.ioloop.IOLoop.instance().start()
