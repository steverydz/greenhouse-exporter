import os
import flask

from canonicalwebteam.flask_base.app import FlaskBase

from webapp.database import db_session, greenhouse_connection
from webapp.models import Job, Employee
from webapp.sso import init_sso, login_required

HARVEST_API_KEY = os.getenv("HARVEST_API_KEY")

app = FlaskBase(
    __name__,
    "greenhouse-exporter",
    template_folder="../templates",
    static_folder="../static",
)

init_sso(app)


@app.route("/")
@login_required
def index():
    return flask.render_template("index.html")


@app.route("/api/jobs")
@login_required
def api_jobs():
    jobs = tuple(
        job[0]
        for job in db_session.query(Job.id)
        .join(Employee)
        .filter(Employee.email == flask.session["openid"]["email"])
        .all()
    )

    if not jobs:
        return flask.jsonify([])

    with greenhouse_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT j.name, count(j.id) from applications a
                JOIN job_posts jp on a.job_post_id = jp.id
                JOIN jobs j on jp.job_id = j.id
                WHERE a.status = 'active' and job_id in %s
                GROUP BY j.name;""",
            (jobs,),
        )

        jobs = []
        for row in cursor.fetchall():
            jobs.append({"job": row[0], "applications": row[1]})

        return flask.jsonify(jobs)


@app.route("/api/interviews")
@login_required
def api_interviews():

    with greenhouse_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT c.first_name, c.last_name, a.stage_name, a.status, si.starts_at
                FROM interviewers i
                    JOIN scheduled_interviews si on i.interview_id = si.id
                    JOIN applications a ON a.id = si.application_id
                    JOIN job_posts jp ON a.job_post_id = jp.id
                    JOIN candidates c on a.candidate_id = c.id
                    JOIN users u on i.user_id = u.id
                WHERE u.email = %s
                ORDER BY si.ends_at DESC
                LIMIT 10""",
            (flask.session["openid"]["email"],),
        )

        interviews = []
        for row in cursor.fetchall():
            interviews.append(
                {
                    "applicant": f"{row[0]} {row[1]}",
                    "date": row[4],
                    "current_stage": row[2],
                    "application_status": row[3],
                }
            )

        return flask.jsonify(interviews)


@app.route("/api/workload")
@login_required
def api_workload():
    """Get interviews scheduled for the jobs that the logged user is a hiring lead."""

    with greenhouse_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT h.job_id, j.created_at, j.name, u.email, si.starts_at, si.ends_at, si.stage_name, si.id, i."user"
                FROM hiring_team h
                    JOIN jobs j on h.job_id = j.id
                    JOIN users u on h.user_id = u.id
                    JOIN applications_jobs aj on j.id = aj.job_id
                    JOIN scheduled_interviews si on aj.application_id = si.application_id
                    JOIN interviewers i on i.interview_id = si.id
                WHERE j.status = 'open' AND u.email=%s AND h.role='Recruiter' AND h.responsible=true AND si.status='scheduled'
                ORDER BY j.created_at DESC            
            """,
            (flask.session["openid"]["email"],),
        )

        workload = []
        for row in cursor.fetchall():
            workload.append(
                {
                    "interviewer": row[8],
                    "stage": row[6],
                    "date": row[4],
                    "estimated_duration": round(
                        (row[5] - row[4]).total_seconds() / 60
                    ),
                }
            )

        return flask.jsonify(workload)


@app.route("/api/interviews/<email>")
# @login_required
def api_interviews_user(email):
    """Get interviews schedules for a specific employee
    2021-09-16: This is not currently used. Kept just for reference
    """

    with greenhouse_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT i.user_id, i.user, i2.name, si.starts_at, si.ends_at, si.status
                FROM interviewers i
                    JOIN scheduled_interviews si on i.interview_id = si.id
                    JOIN users u on i.user_id = u.id
                    JOIN interviews i2 on si.interview_id = i2.id
                WHERE u.email= %s
                ORDER BY si.ends_at DESC;""",
            (email,),
        )

        interviews = []
        for row in cursor.fetchall():
            interviews.append(
                {
                    "employee": row[1],
                    "type": row[2],
                    "date": row[3],
                    "estimated_duration": round(
                        (row[4] - row[3]).total_seconds() / 60
                    ),
                    "status": row[5],
                }
            )

        return flask.jsonify(interviews)
