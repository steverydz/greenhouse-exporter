from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import label

Base = declarative_base()
engine = create_engine(
    "postgresql://postgres:pw@localhost:5432/postgres", echo=True
)


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
    name = Column(String)
    fullname = Column(String)
    greenhouse_link = Column(String)


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    # open_date = Column(String)
    # close_date = Column(String)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    # date = Column()
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))


class Types(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    label = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.commit()
