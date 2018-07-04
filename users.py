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
    # Create users
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
            'username': user.user_name,
            'emailId': user.email_address,
            'contact': user.phone,
            'password': user.password
        }

        print(user)
        # json.dumps(user)

        self.write(response)

    # Filter users by id

    def get(self, user_id):
        print('>>>>', user_id)
        if user_id:
            user = session.query(User).filter(User.user_id == user_id).first()
            print(user.as_dict())
            # print(json.dumps(user))
            self.write(user.as_dict())
        # self.finish("Error")

    # Delete user by id
    def delete(self, user_id):
        print('>>>>', user_id)
        if user_id:
            user = session.query(User).filter(User.user_id == user_id).first()
            # user=query.one()
            print(user)
            session.delete(user)
            session.commit()
            print(user)
            self.finish(dict(hello="world"))


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        user_name=self.get_argument('user_name')
        user=session.query(User).filter(User.user_name==user_name).first()
        user=user.as_dict()
        print(user['user_name'])
        cookieName=user['user_name']
        if not self.get_secure_cookie(cookieName):
            self.set_secure_cookie("user",cookieName)
            print(cookieName)
            #self.write("Cookie name has been set")
            #self.redirect("/tasks",user_name=cookieName)
        else:
            self.write("Cookie",cookieName)
            #self.write("Success")


         
