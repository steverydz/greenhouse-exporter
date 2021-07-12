import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Base
from functions import (
    add_new_candidates,
    get_jobs,
    import_candidate_applications,
    import_candidate_rejections,
    import_candidate_hired,
    import_employees,
    import_cv_reviewed,
    interview_scheduled,
    participated_interview,
    scorecard_added,
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
import_employees(greenhouse_cursor, session)
get_jobs(greenhouse_cursor, session)
add_new_candidates(greenhouse_cursor, session)
import_candidate_applications(greenhouse_cursor, session)
import_candidate_rejections(greenhouse_cursor, session)
import_candidate_hired(greenhouse_cursor, session)
import_cv_reviewed(greenhouse_cursor, session)
interview_scheduled(greenhouse_cursor, session)
participated_interview(greenhouse_cursor, session)
scorecard_added(greenhouse_cursor, session)

# Close connection
greenhouse_connection.close()
