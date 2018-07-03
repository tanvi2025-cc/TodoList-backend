#Importing sqlalchemy libraries
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref,relationship
from datetime import datetime
from sqlalchemy import DateTime


#Connecting db
engine=create_engine('sqlite:////Volumes/Others/repos/todolist/users.db', echo=True)
# engine=create_engine('sqlite:///:memory:', echo=True)
Session=sessionmaker(bind=engine)
session=Session()
#Declarative base
Base = declarative_base()

#User model
class User(Base):
    __tablename__='users'
    user_id=Column(Integer(),primary_key=True)
    user_name=Column(String(15),nullable=False,unique=True)
    email_address=Column(String(50),nullable=False)
    phone=Column(String(20),nullable=False)
    password=Column(String(25),nullable=False)
    
    def __repr__(self):
        return "Users(username,{self.user_name}),"\
                  "(emailaddress,{self.email_address}),"\
                  "(phone_number,{self.phone})".format(self=self)
#Tasks Model 
class Tasks(Base):
    __tablename__='tasks'
    tasks_id=Column(Integer(),primary_key=True)
    tasks_name=Column(String(),nullable=False)
    tasks_deadline=Column(DateTime(),default=datetime.now)
    
    #Representation method
    def __repr__(self):
        return "Tasks(taskname,{self.tasks_name}),"\
            "(deadline,{self.tasks_deadline})".format(self=self)


Base.metadata.create_all(engine)
