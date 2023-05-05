from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

# from Resumeaiogram import config

db = create_engine('postgresql://postgres:Nazar2006@127.0.0.1/test_bot')
# 'postgresql://user:password@localhost/mydatabase'
Base = declarative_base()
# Base.metadata.create_all(db)

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

    def add_lang(self, lang):
        # if not self.lang:
        #     self.lang = lang
        # else:
            self.lang.append(lang)

    def add_lang_level(self, lang_level):
        # if not self.lang_level:
        #     self.lang_level = lang_level
        # else:
            self.lang.append(lang_level)

    def update_info(self, id=None, name_surname=None, email=None, phone_number=None, education=None, lang=None,
                    lang_level=None, country=None, city=None, description=None, profession=None, soft_skills=None,
                    tech_skills=None, projects=None, how_long=None, job_description=None, past_work=None, password=None):
        if id:
            self.id = id
        elif name_surname:
            self.name_surname = name_surname
        if email:
            self.email = email
        elif phone_number:
            self.phone_number = phone_number
        if education:
            self.education = education
        # elif lang:
        #     self.lang = lang
        # if lang_level:
        #     self.lang_level = lang_level
        elif country:
            self.country = country
        if city:
            self.city = city
        elif description:
            self.description = description
        if profession:
            self.profession = profession
        elif soft_skills:
            self.soft_skills = soft_skills
        if tech_skills:
            self.tech_skills = tech_skills
        elif password:
            self.password = password
        if projects:
            self.projects = projects
        elif how_long:
            self.how_long = how_long
        if job_description:
            self.job_description = job_description
        elif past_work:
            self.past_work = past_work


if __name__ == '__main__':
    print('start')
    Base.metadata.create_all(db)
    select = select(ResumeBot)
    print(select)
    resumes = session.query(ResumeBot).all()
    print(type(resumes))
    for resume in resumes:
        print(resume.id, resume.name_surname, resume.phone_number, resume.email, resume.education, resume.lang, resume.lang_level, resume.country, resume.city, resume.description, resume.past_work, resume.profession, resume.soft_skills, resume.tech_skills, resume.projects, resume.how_long, resume.job_description, resume.past_work, resume.password)

    print('finish')