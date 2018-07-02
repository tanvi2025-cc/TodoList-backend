#Importing sqlalchemy libraries
import sqlalchemy
print(sqlalchemy.__version__)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

#Connecting db
engine=create_engine('sqlite:///:memory:', echo=True)

#Declarative base
Base = declarative_base()

#User model
class UserModel(Base):
    _tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
        elf.name, self.fullname, self.password)