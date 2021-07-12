from models import Candidate, Employee, Event, Job


def import_employees(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute("SELECT id, full_name, email, status FROM users")

    for user in greenhouse_cursor.fetchall():
        canonical_session.add(
            Employee(
                id=user[0],
                full_name=user[1],
                email=user[2],
                status=user[3]
            )
        )

    canonical_session.commit()


def get_jobs(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, name, opened_at FROM jobs"
    )

    for job in greenhouse_cursor.fetchall():
        j = Job(id=job[0], name=job[1], status="open", opened_at=job[2])
        canonical_session.add(j)

    canonical_session.commit()


def add_new_candidates(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, first_name, last_name, created_at FROM candidates"
    )

    all_candidates = greenhouse_cursor.fetchall()
    for candidate in all_candidates:
        c = Candidate(id=candidate[0], first_name=candidate[1], last_name=candidate[2])
        canonical_session.add(c)

    canonical_session.commit()


def import_candidate_applications(greenhouse_cursor, canonical_session):
        greenhouse_cursor.execute(f"SELECT a.applied_at, a.candidate_id ,jp.job_id FROM applications a join job_posts jp on a.job_post_id = jp.id")
        for application in greenhouse_cursor.fetchall():
            e = Event(
                date=application[0],
                candidate_id=application[1],
                job_id=application[2],
                type="candidate_applied",
            )
            canonical_session.add(e)
        canonical_session.commit()


def import_candidate_rejections(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT c.id, u.id, jp.job_id, a.rejected_at FROM applications a JOIN users u on a.rejected_by_id = u.id JOIN candidates c on a.candidate_id = c.id JOIN job_posts jp on a.job_post_id = jp.id;"
    )

    for rejection in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=rejection[0],
                employee_id=rejection[1],
                job_id=rejection[2],
                date=rejection[3],
                type="rejected",
            )
        )

    canonical_session.commit()


def import_candidate_hired(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "select o.resolved_at, c.id, jp.job_id from offers o join applications a on o.application_id = a.id join candidates c on a.candidate_id = c.id JOIN job_posts jp on a.job_post_id = jp.id where o.status = 'accepted';"
    )

    for hire in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=hire[1],
                job_id=hire[2],
                date=hire[0],
                type="hired",
            )
        )

    canonical_session.commit()


def import_cv_reviewed(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT jp.job_id, a.candidate_id, aps.exited_on FROM application_stages aps JOIN applications a ON a.id = aps.application_id JOIN job_posts jp ON a.job_post_id = jp.id WHERE aps.stage_name='Application Review' AND aps.exited_on is not null"
    )

    for cv_reviewed in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=cv_reviewed[1],
                job_id=cv_reviewed[0],
                date=cv_reviewed[2],
                type="cv_reviewed",
            )
        )

    canonical_session.commit()