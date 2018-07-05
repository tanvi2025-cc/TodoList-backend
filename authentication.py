# Importing modules
import jwt
import json
import functools
import bz2
import tornado.web
import tornado.ioloop
import tornado.escape
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Users.models import User
from Users.handlers import UserHandler


JWT_SECRET = 'ABC'

# create engine
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()


class LoginHandler(tornado.web.RequestHandler):

    def prepare(self, userId=None):
        date = datetime.utcnow() + timedelta(hours=1)
        self.encoded = jwt.encode(
            {
                'userId': userId,
                'expiresAt': date.timestamp()
            },
            JWT_SECRET,
            'HS256'
        )

    def post(self):
        user_name = self.get_body_argument('user_name')
        password = self.get_body_argument('password')
        password=UserHandler.hash_password(self,password)
        user = session.query(User).filter(
            User.user_name == user_name,User.password == password).first()
        user=user.as_dict()
        print(user)
        if user:
            self.prepare(user['id'])
            response={'token': str(self.encoded)}
            self.finish(response)
        else:
            self.finish('Error')


def validate(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        encoded=self.request.headers.get('Authorization')
        data=jwt.decode(encoded, JWT_SECRET, 'HS256')
        print(data)

        if data['expiresAt'] > datetime.now().timestamp():
            print(datetime.now().timestamp())
            raise tornado.web.HTTPError(401)

        return method(self, *args, **kwargs)

    return wrapper
