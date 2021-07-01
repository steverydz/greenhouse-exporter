from models import Candidates, Events, Jobs

def get_jobs(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, name, opened_at FROM jobs t WHERE status='open'"
    )

    for jobs in greenhouse_cursor.fetchall():
        j = Jobs(id=jobs[0], name=jobs[1], status="open", opened_at=jobs[2])
        canonical_session.add(j)

    canonical_session.commit()

def add_new_candidates(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, first_name, last_name, created_at FROM candidates WHERE created_at between '2021-07-01' and '2021-07-02'"
    )

    all_candidates = greenhouse_cursor.fetchall()
    for candidate in all_candidates:
        c = Candidates(id=candidate[0], first_name=candidate[1], last_name=candidate[2])
        canonical_session.add(c)

        greenhouse_cursor.execute(f"SELECT a.applied_at, jp.job_id FROM applications a join job_posts jp on a.job_post_id = jp.id WHERE a.candidate_id={c.id}")
        for application in greenhouse_cursor.fetchall():
            e = Events(
                date=application[0],
                candidate_id=c.id,
                job_id=application[1],
                type="candidate_applied",
            )
            canonical_session.add(e)

    canonical_session.commit()