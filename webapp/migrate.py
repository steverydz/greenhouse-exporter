import csv

from webapp.database import greenhouse_connection, db_session, drop_all
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
from webapp.models import Employee


with greenhouse_connection() as connection:
    greenhouse_cursor = connection.cursor()

    drop_all()
    import_employees(greenhouse_cursor, db_session)

    hiring_leads = {}
    with open("hiring_leads.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            if not row["Primary Recruiter"]:
                continue

            try:
                employee = (
                    db_session.query(Employee)
                    .filter(Employee.full_name == row["Primary Recruiter"])
                    .one_or_none()
                )
                hiring_leads[int(row["Job ID"])] = employee.id
            except Exception:
                continue

    get_jobs(greenhouse_cursor, db_session, hiring_leads)
    add_new_candidates(greenhouse_cursor, db_session)
    import_candidate_applications(greenhouse_cursor, db_session)
    import_candidate_rejections(greenhouse_cursor, db_session)
    import_candidate_hired(greenhouse_cursor, db_session)
    import_cv_reviewed(greenhouse_cursor, db_session, hiring_leads)
    interview_scheduled(greenhouse_cursor, db_session)
    participated_interview(greenhouse_cursor, db_session)
    scorecard_added(greenhouse_cursor, db_session)
    stage_moved(greenhouse_cursor, db_session)
