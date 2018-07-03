# Importing libraries
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

# Creating session
engine = create_engine(
    'sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class UserHandler(tornado.web.RequestHandler):
    #Create users 
    def post(self):
        username = self.get_argument('user_name')
        emailId = self.get_argument('email_address')
        contact = self.get_argument('phone')
        password = self.get_argument('password')
        user = User(user_name=username, email_address=emailId,
                    phone=contact, password=password)
        session.add(user)
        session.commit()
        response = {
            'username': username,
            'emailId': emailId,
            'contact': contact,
            'password': password
        }

        print(user)
        self.write(response)
# Get all user objects

    def get(self):
        self.write("Hello world")
        user = session.query(User).all()
        print(user)