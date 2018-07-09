import tornado
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnection:
    '''
    This class is creating database connection to SQLalchemy engine
    '''
    # create_engine object
    engine = create_engine('postgresql://root:root@localhost/tododb')
    Session = sessionmaker(bind=engine)
    # Session object
    session = Session()
