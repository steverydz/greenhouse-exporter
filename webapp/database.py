import os

import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from webapp.models import Base


greenhouse_connection = lambda: psycopg2.connect(
    os.getenv("GREENHOUSE_DATABASE_URL")
)


engine = create_engine(os.getenv("CANONICAL_DATABASE_URL"))
db_session = None


def create_session():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def drop_all():
    Base.metadata.drop_all(engine)
    global db_session
    db_session = create_session()


db_session = create_session()
