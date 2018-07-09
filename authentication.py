import jwt
import json
import functools
from datetime import datetime, timedelta
import tornado.web
import tornado.ioloop
import tornado.escape
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Users.models import User
from Users.handlers import UserHandler
from DatabaseConnect.DbConnection import DbConnection

JWT_SECRET = 'ABC'
ALGORITHM = 'HS256'



class LoginHandler(DbConnection,tornado.web.RequestHandler):
    '''
    Request Handler for user Login request
    Methods=('PREPARE','POST')
    '''

    def prepare(self, userId=None):
        '''
        Prepare method to generate jwt token
        '''
        date = datetime.utcnow() + timedelta(hours=1)
        self.encoded = jwt.encode(
            {
                'userId': userId,
                'expiresAt': date.timestamp()
            },
            JWT_SECRET,
            ALGORITHM

        )

    def post(self):
        '''
        Post method to submit credentials for authentication
        '''
        user_name = self.get_body_argument('user_name')
        password = UserHandler.validate_hash_password(
            self, self.get_body_argument('password'))
        user = self.session.query(User).filter(
            User.user_name == user_name, User.password == password).first()
        user = user.as_dict()

        if user:
            self.prepare(user['id'])
            response = {'token': str(self.encoded)}
            self.finish(response)
        else:
            self.finish('Error')


def validate(method):
    '''
    Decorator to authenticate requests
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        encoded = self.request.headers.get('Authorization')
        data = jwt.decode(encoded, JWT_SECRET, ALGORITHM)

        if data['expiresAt'] > datetime.now().timestamp():

            raise tornado.web.HTTPError(401)

        return method(self, *args, **kwargs)

    return wrapper
