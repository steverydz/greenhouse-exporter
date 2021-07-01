from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import label


Base = declarative_base()

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))


class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    open_date = Column(DateTime)
    close_date = Column(DateTime)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    type_id = Column(Integer, ForeignKey("types.id"))


class Types(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    label = Column(String)