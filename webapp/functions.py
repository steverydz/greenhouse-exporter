from webapp.models import Candidate, Employee, Event, Job


def import_employees(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute("SELECT id, full_name, email, status FROM users")

    for user in greenhouse_cursor.fetchall():
        canonical_session.add(
            Employee(
                id=user[0], full_name=user[1], email=user[2], status=user[3]
            )
        )

    canonical_session.commit()


def get_jobs(greenhouse_cursor, canonical_session, hiring_leads):
    greenhouse_cursor.execute("SELECT id, name, opened_at, status FROM jobs")

    for job in greenhouse_cursor.fetchall():
        canonical_session.add(
            Job(
                id=job[0],
                name=job[1],
                status=job[3],
                opened_at=job[2],
                hiring_lead=hiring_leads.get(job[0]),
            )
        )

    canonical_session.commit()


def add_new_candidates(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, first_name, last_name, created_at FROM candidates"
    )

    all_candidates = greenhouse_cursor.fetchall()
    for candidate in all_candidates:
        c = Candidate(
            id=candidate[0], first_name=candidate[1], last_name=candidate[2]
        )
        canonical_session.add(c)

    canonical_session.commit()


def import_candidate_applications(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        """
          SELECT a.applied_at, a.candidate_id, jp.job_id
            FROM applications a join job_posts jp on a.job_post_id = jp.id
        """
    )
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
        """
            SELECT c.id, u.id, jp.job_id, a.rejected_at
              FROM applications a JOIN users u on a.rejected_by_id = u.id
              JOIN candidates c on a.candidate_id = c.id
              JOIN job_posts jp on a.job_post_id = jp.id;
        """
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
        """
            SELECT o.resolved_at, c.id, jp.job_id
              FROM offers o join applications a ON o.application_id = a.id
              JOIN candidates c ON a.candidate_id = c.id
              JOIN job_posts jp ON a.job_post_id = jp.id
              WHERE o.status = 'accepted';
        """
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


def import_cv_reviewed(greenhouse_cursor, canonical_session, hiring_leads):
    greenhouse_cursor.execute(
        """
            SELECT jp.job_id, a.candidate_id, aps.exited_on
              FROM application_stages aps
              JOIN applications a ON a.id = aps.application_id
              JOIN job_posts jp ON a.job_post_id = jp.id
              WHERE aps.stage_name='Application Review'
                AND aps.exited_on is not null
        """
    )

    for cv_reviewed in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=cv_reviewed[1],
                employee_id=hiring_leads.get(cv_reviewed[0]),
                job_id=cv_reviewed[0],
                date=cv_reviewed[2],
                type="cv_reviewed",
            )
        )

    canonical_session.commit()


def interview_scheduled(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        """
            SELECT jp.job_id, a.candidate_id, si.scheduled_at
              FROM scheduled_interviews si
              JOIN applications a ON a.id = si.application_id
              JOIN job_posts jp ON a.job_post_id = jp.id
        """
    )

    for interview_scheduled in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=interview_scheduled[1],
                job_id=interview_scheduled[0],
                date=interview_scheduled[2],
                type="interview_scheduled",
            )
        )

    canonical_session.commit()


def participated_interview(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        """
            SELECT i.user_id, jp.job_id, si.ends_at, a.candidate_id
              FROM interviewers i
              JOIN scheduled_interviews si on i.interview_id = si.id
              JOIN applications a ON a.id = si.application_id
              JOIN job_posts jp ON a.job_post_id = jp.id;
        """
    )

    for participated_interview in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=participated_interview[3],
                job_id=participated_interview[1],
                date=participated_interview[2],
                employee_id=participated_interview[0],
                type="participated_interview",
            )
        )

    canonical_session.commit()


def scorecard_added(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        """
            SELECT s.interviewer_id, s.submitted_at, jp.job_id, a.candidate_id
              FROM scorecards s
              JOIN applications a ON a.id = s.application_id
              JOIN job_posts jp ON a.job_post_id = jp.id;
        """
    )

    for scorecard in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=scorecard[3],
                job_id=scorecard[2],
                date=scorecard[1],
                employee_id=scorecard[0],
                type="scorecard_added",
            )
        )

    canonical_session.commit()


def stage_moved(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        """
            SELECT jp.job_id, a.candidate_id, ast.entered_on, ast.stage_name
              FROM application_stages ast
              JOIN applications a on ast.application_id = a.id
              JOIN job_posts jp on a.job_post_id = jp.id
              WHERE ast.entered_on is not null
        """
    )

    for stage_move in greenhouse_cursor.fetchall():
        canonical_session.add(
            Event(
                candidate_id=stage_move[1],
                job_id=stage_move[0],
                date=stage_move[2],
                stage=stage_move[3],
                type="stage_moved",
            )
        )

    canonical_session.commit()
