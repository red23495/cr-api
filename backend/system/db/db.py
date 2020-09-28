from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from backend.config import config

SQLALCHEMY_DATABASE_URL = config.DB_CONFIG.build_connection_uri()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """ Creates a new db session and returns it. """
    return SessionLocal()


Base = declarative_base()
