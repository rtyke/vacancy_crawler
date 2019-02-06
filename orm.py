from sqlalchemy import create_engine, Column, Integer, Boolean, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgres://localhost/vartan', echo=True)
Base = declarative_base()
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()


vac_spec = Table(
    'vacancy_fields', Base.metadata,
    Column('vacancy_filed_id', Integer, primary_key=True),
    Column('vacancy_id', Integer, ForeignKey('vacancies.id')),
    Column('specialization_id', Integer, ForeignKey('fields.id'))
)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    id_on_site = Column(Integer, index=True, unique=True)
    title = Column(Text, nullable=False)
    published_date = Column(DateTime)
    description = Column(Text)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(Text)
    firm = Column(Text)
    address = Column(Text)
    town = Column(Text)
    metro = Column(Text)
    type_of_work = Column(Text)
    experience = Column(Text)
    field = relationship('Field', secondary=vac_spec)
    is_archive = Column(Boolean)
    added_to_db_at = Column(DateTime)
    url = Column(Text, unique=True)
    source = Column(Text, default='HeadHunter')

    def __init__(self, id_on_site, title, published_date, description,
                 salary_from, salary_to, currency, firm, address, town, metro,
                 type_of_work, experience, is_archive, added_to_db_at, url):
        self.id_on_site = id_on_site
        self.title = title
        self.published_date = published_date
        self.description = description
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.firm = firm
        self.address = address
        self.town = town
        self.metro = metro
        self.type_of_work = type_of_work
        self.experience = experience
        self.is_archive = is_archive
        self.added_to_db_at = added_to_db_at
        self.url = url

    def __repr__(self):
        return f'<Vacancy {self.url}>'


class Field(Base):
    __tablename__ = 'fields'
    id = Column(Integer, primary_key=True)
    id_hh = Column(Integer, unique=True)
    id_sj = Column(Integer, unique=True)
    name = Column(Text, unique=True)

    def __init__(self, id_hh, id_sj, name):
        self.id_hh = id_hh
        self.id_sj = id_sj
        self.name = name

    def __repr__(self):
        return f'<Specialization> {self.name}'


Base.metadata.create_all(bind=engine)

