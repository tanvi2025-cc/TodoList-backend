import re
import hashlib
import uuid
from datetime import datetime
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import User
from DatabaseConnect.DbConnection import DbConnection


class UserHandler(DbConnection, tornado.web.RequestHandler):
    '''
    Request Handler for users table
    Methods used=('GET ,'POST','DELETE')
    '''

    def validate_email(self, email):
        # Validating the format of email
        if not email:
            self.set_status(400)
            self.finish(dict(error=True, message="Email is missing"))
        if re.match("[^@]+@[^@]+\.[^@]+", email) != None:
            return email
        else:
            self.set_status(400)
            self.finish(dict(error=True, message="Not a valid email"))

    def validate_username(self, username):
        if not username:
            self.set_status(400)
            self.finish(dict(error=True, message="Username is missing"))
        # Validation of username
        if len(username) >= 3:
            return username
        else:
            self.set_status(400)
            self.finish(dict(error=True, message="Not a valid username"))

    def validate_hash_password(self, password):
        if not password:
            self.set_status(400)
            self.finish(dict(error=True, message='Password is missing'))
        if len(password) >= 8:
            # Hashed password
            hashed_password = hashlib.sha256(
                password.encode('utf-8')).hexdigest()
            return hashed_password
        else:
            self.set_status(400)
            self.finish(dict(error=True, message="Not a valid password"))

    def post(self):
        '''
        POST request method to register new user
        '''
        username = self.validate_username(
            self.get_body_argument('user_name', None))
        emailId = self.validate_email(
            self.get_body_argument('email_address', None))
        password = self.validate_hash_password(
            self.get_body_argument('password'))

        user = User(user_name=username, email_address=emailId,
                    password=password)
        self.session.add(user)
        self.session.commit()
        response = dict({'username': user.user_name,
                         'email': user.email_address, 'password': user.password})
        self.write(response)

    def get(self, user_id):
        '''
        GET request method to fetch the user objects by id
        '''

        if user_id:
            user = self.session.query(User).filter(User.id == user_id).first()

            if not user:
                self.set_status(400)
                self.finish(dict(message="User not found"))
            self.finish(user.as_dict())
        else:
            self.set_status(400)
            self.finish(dict(error=True, message="Not a valid user id"))

    def delete(self, user_id):
        '''
        DELETE request method to delete the particular user as per user id.
        '''
        if user_id:
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                self.set_status(404)
                self.finish(dict(error=True, message="User id not found"))

            self.session.delete(user)
            self.session.commit()
            self.finish(dict(error=False, message="Deleted"))
        else:
            self.set_status(400)
            self.finish(dict(error=True, message="Not a valid user id"))
