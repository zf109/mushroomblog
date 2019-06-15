from contextlib import contextmanager
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..config import Config as conf

@contextmanager
def db_session(db_url=None, engine=None, autoflush=True):
    """ Creates a context with an open SQLAlchemy session.
    """
    db_url = db_url or conf.DATABASE_URL

    if not db_url:
        raise ValueError("No db_url given, need to have a connection string")
    engine = engine or create_engine(db_url, convert_unicode=True)

    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=autoflush, bind=engine))()
    yield db_session
    db_session.close()
    connection.close()
