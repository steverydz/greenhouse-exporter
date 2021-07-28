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
