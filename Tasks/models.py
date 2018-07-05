# Importing sqlalchemy libraries
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from sqlalchemy.dialects.postgresql import UUID


# Creating session
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
# Tasks Model


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    tasks_name = Column(String(), nullable=False)
    tasks_deadline = Column(DateTime(), default=datetime.now, nullable=False)

    # Representation method
    def __str_(self):
        return "Tasks(taskname,{self.tasks_name}),"\
            "(deadline,{self.tasks_deadline})".format(self=self)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base.metadata.create_all(engine)
