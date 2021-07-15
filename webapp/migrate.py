import csv
import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from webapp.models import Base, Employee
from webapp.functions import (
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
    stage_moved,
)


# Connect to greenhouse database
greenhouse_connection = psycopg2.connect(os.getenv("GREENHOUSE_DATABASE_URL"))
greenhouse_cursor = greenhouse_connection.cursor()

# Connect to our database
engine = create_engine(os.getenv("CANONICAL_DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


import_employees(greenhouse_cursor, session)

hiring_leads = {}
with open("hiring_leads.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        if not row["Primary Recruiter"]:
            continue

        try:
            employee = (
                session.query(Employee)
                .filter(Employee.full_name == row["Primary Recruiter"])
                .one_or_none()
            )
            hiring_leads[int(row["Job ID"])] = employee.id
        except:
            continue

get_jobs(greenhouse_cursor, session, hiring_leads)
add_new_candidates(greenhouse_cursor, session)
import_candidate_applications(greenhouse_cursor, session)
import_candidate_rejections(greenhouse_cursor, session)
import_candidate_hired(greenhouse_cursor, session)
import_cv_reviewed(greenhouse_cursor, session)
interview_scheduled(greenhouse_cursor, session)
participated_interview(greenhouse_cursor, session)
scorecard_added(greenhouse_cursor, session)
stage_moved(greenhouse_cursor, session)

# Close connection
greenhouse_connection.close()
