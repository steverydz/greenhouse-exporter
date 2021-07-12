from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import label


Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    status = Column(String)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    hiring_lead = Column(Integer, ForeignKey("employees.id"))


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    type = Column(
        Enum(
            "candidate_applied",
            "cv_reviewed",
            "scorecard_added",
            "stage_moved",
            "interview_scheduled",
            "participated_interview",
            "hired",
            "rejected",
            "invitations_sent",
            name="types",
        )
    )
