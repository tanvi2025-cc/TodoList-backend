import re
import hashlib
import uuid
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import User

# generating session
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()


class UserHandler(tornado.web.RequestHandler):
    '''
    This is a Request Handler for users table
    Methods used=('GET ,'POST')
    '''
    def validate_email(self, email):
        #Validating the format of email
        if re.match("[^@]+@[^@]+\.[^@]+", email) != None:
            return email
        raise tornado.web.HTTPError(401)

    def validate_username(self, username):
        #Validation of username
        if len(username) >= 3:
            return username
        raise tornado.web.HTTPError(401)

    def hash_password(self, password):
        if len(password) >= 8:
            #Hashed password
            hashed_password = hashlib.sha256(
                password.encode('utf-8')).hexdigest()
            return hashed_password
        raise tornado.web.HTTPError(401)

    def post(self):
        '''
        This is 
        '''
        username = self.validate_username(self.get_body_argument('user_name'))
        emailId = self.validate_email(self.get_body_argument('email_address'))
        password = self.hash_password(self.get_body_argument('password'))

        user = User(user_name=username, email_address=emailId,
                    password=password)
        session.add(user)
        session.commit()
        response = dict({'username': user.user_name,
                         'email': user.email_address, 'password': user.password})
        self.write(response)

    # Filter users by id

    def get(self, user_id):

        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            print(user.as_dict())
            self.write(user.as_dict())
        else:
            self.finish()

    # Delete user by id
    def delete(self, user_id):

        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            session.delete(user)
            session.commit()
            self.finish(dict({'status''deleted'})
