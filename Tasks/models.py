from datetime import datetime
import tornado.web
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from DatabaseConnect.DbConnection import DbConnection
# Declarative base
Base = declarative_base()


class Tasks(Base):
    '''
    This class is creating tasks table in the database
    '''
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    tasks_name = Column(String(), nullable=False)
    tasks_deadline = Column(DateTime(), default=datetime.now, nullable=False)

    def __str_(self):
        # String representation of object
        return "Tasks(taskname,{self.tasks_name}),"\
            "(deadline,{self.tasks_deadline})".format(self=self)

    def as_dict(self):
        # Dict representation of objects
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base.metadata.create_all(DbConnection.engine)
