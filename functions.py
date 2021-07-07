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
        "SELECT id, name, opened_at FROM jobs t WHERE status='open'"
    )

    for job in greenhouse_cursor.fetchall():
        j = Job(id=job[0], name=job[1], status="open", opened_at=job[2])
        canonical_session.add(j)

    canonical_session.commit()


def add_new_candidates(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, first_name, last_name, created_at FROM candidates WHERE created_at between '2021-07-01' and '2021-07-02'"
    )

    all_candidates = greenhouse_cursor.fetchall()
    for candidate in all_candidates:
        c = Candidate(id=candidate[0], first_name=candidate[1], last_name=candidate[2])
        canonical_session.add(c)

        greenhouse_cursor.execute(f"SELECT a.applied_at, jp.job_id FROM applications a join job_posts jp on a.job_post_id = jp.id WHERE a.candidate_id={c.id}")
        for application in greenhouse_cursor.fetchall():
            e = Event(
                date=application[0],
                candidate_id=c.id,
                job_id=application[1],
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
