import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Base
from functions import (
    add_new_candidates,
    get_jobs
) 


# Connect to greenhouse database
greenhouse_connection = psycopg2.connect(os.getenv("GREENHOUSE_DATABASE_URL"))
greenhouse_cursor = greenhouse_connection.cursor()

# Connect to our database
engine = create_engine(os.getenv("CANONICAL_DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Run functions to fill the database
get_jobs(greenhouse_cursor, session)
add_new_candidates(greenhouse_cursor, session)

# Close connection
greenhouse_connection.close()