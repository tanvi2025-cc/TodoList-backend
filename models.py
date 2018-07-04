# Importing sqlalchemy libraries
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from sqlalchemy import DateTime
from json import dumps
from sqlalchemy.orm import class_mapper


# Connecting db
engine = create_engine(
    'sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
# engine=create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
# Declarative base
Base = declarative_base()

# User model


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)

    def __str__(self):
        return "<User(user_name='%s', email_address='%s', phone='%s',password='%s')>" % (self.user_name, self.email_address, self.phone,self.password)
    def __repr__(self):
       return "<User(user_name'%s', email_address='%s', phone='%s',password='%s')>" % (self.user_name, self.email_address, self.phone,self.password) 
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

    


# Tasks Model
class Tasks(Base):
    __tablename__ = 'tasks'
    tasks_id = Column(Integer(), primary_key=True)
    tasks_name = Column(String(), nullable=False)
    tasks_deadline = Column(DateTime(), default=datetime.now)

    # Representation method
    def __str_(self):
        return "Tasks(taskname,{self.tasks_name}),"\
            "(deadline,{self.tasks_deadline})".format(self=self)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
 
Base.metadata.create_all(engine)
