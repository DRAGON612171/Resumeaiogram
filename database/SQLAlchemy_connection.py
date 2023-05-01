import sqlalchemy
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('postgresql://user:password@localhost/mydatabase')
Base = declarative_base()


Session = sessionmaker(db)
session = Session()


class ResumeBot(Base):
    __tablename__ = 'resume_bot'
    id = Column(Integer, primary_key=True)
    name_surname = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    education = Column(ARRAY(String), nullable=True)
    lang = Column(ARRAY(String), nullable=True)
    lang_level = Column(ARRAY(String), nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    description = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    soft_skills = Column(ARRAY(String), nullable=True)
    tech_skills = Column(ARRAY(String), nullable=True)
    projects = Column(ARRAY(String), nullable=True)
    how_long = Column(ARRAY(String), nullable=True)
    job_description = Column(ARRAY(String), nullable=True)
    past_work = Column(ARRAY(String), nullable=True)
    password = Column(String, nullable=True)




if __name__ == '__main__':
    print('start')
    Base.metadata.create_all(db)
    select = sqlalchemy.select(ResumeBot)
    print(select)
    resumes = session.query(ResumeBot).all()
    print(type(resumes))
    for resume in resumes:
        print(resume.id, resume.name_surname, resume.phone_number, resume.email, resume.education, resume.lang, resume.lang_level, resume.country, resume.city, resume.description, resume.work_experience, resume.profession, resume.soft_skills, resume.tech_skills, resume.projects, resume.how_long, resume.job_description, resume.past_work, resume.password)

    print('finish')