import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.dialects.postgresql import UUID

# Declarative base
Base = declarative_base()
# Creating session
engine = create_engine('postgresql://root:root@localhost/tododb')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    def __str__(self):
        return "<User(user_name='%s', email_address='%s')>" % (self.user_name, self.email_address)

    def __repr__(self):
        return "<User(user_name'%s', email_address='%s')>" % (self.user_name, self.email_address)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base.metadata.create_all(engine)
