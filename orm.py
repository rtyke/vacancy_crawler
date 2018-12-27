import json

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///vacancies_db.db')
Session = sessionmaker(bind=engine)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id_pk = Column(Integer, primary_key=True)
    hash = None  # how to create?
    vid = Column('id', Integer)
    title = Column('title', String)
    unixtime = Column('unixtime', Integer)
    description = Column('description', String)
    address = Column('address', String)
    metro = Column('metro', String)
    type_of_work = Column('type_of_work', String)
    experience = Column('experience', String)
    salary = Column('salary', Integer)
    specializations = Column('specializations', String)
    is_archive = Column('is_archive', Boolean)
    update_time = Column('update_time', Integer)

    def __init__(self, vid, title, unixtime, description, address, metro,
                 type_of_work, experience, salary, specializations, is_archive,
                 update_time):
        self.vid = vid
        self.title = title
        self.unixtime = unixtime
        self.description = description
        self.address = address
        self.metro = metro
        self.type_of_work = type_of_work
        self.experience = experience
        self.salary = salary
        self.specializations = specializations
        self.is_archive = is_archive
        self.update_time = update_time
