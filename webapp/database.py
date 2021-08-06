import os

import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from webapp.models import Base


def greenhouse_connection():
    return psycopg2.connect(os.getenv("GREENHOUSE_DATABASE_URL"))


engine = create_engine(os.getenv("CANONICAL_DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
