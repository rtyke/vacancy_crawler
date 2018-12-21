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
    id = Column('id', Integer)
    title = Column('title', String)
    unixtime = Column('unixtime', Integer)
    description = Column('date', String)
    address = Column('address', String)
    metro = Column('metro', String)
    type_of_work = Column('type_of_work', String)
    experience = Column('experience', String)
    salary = Column('salary', Integer)
    specializations = Column('specializations', String)
    is_archive = Column('is_archive', Boolean)

    def __init__(self, id, title, unixtime, description, address, metro,
                 type_of_work, experience, salary, specializations, is_archive):
        self.id = id
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

