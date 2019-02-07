from sqlalchemy import create_engine, Column, Integer, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


engine = create_engine('postgres://localhost/8888', echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


vac_spec = Table(
    'vacancy_fields', Base.metadata,
    Column('vacancy_filed_id', Integer, primary_key=True),
    Column('vacancy_id', Integer, ForeignKey('vacancies.id')),
    Column('specialization_id', Integer, ForeignKey('fields.id'))
)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    # hash = None  # how to create?
    id_on_site = Column(Integer, index=True, unique=True)
    title = Column(Text, nullable=False)
    published_date = Column(DateTime)
    description = Column(Text)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(Text)
    firm = Column(Text)
    address = Column(Text)
    # town = Column(Text, nullable=False)
    town = Column(Text)
    metro = Column(Text)
    type_of_work = Column(Text)
    experience = Column(Text)
    field = relationship('Field', secondary=vac_spec)
    is_archive = Column(Boolean)
    added_to_db_at = Column(DateTime)
    url = Column(Text, unique=True)
    source = Column(Text, default='SuperJob')


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


def init_db():
    Base.metadata.create_all(bind=engine)


def fill_in_fields_handbook():
    it = Field(1, 33, 'Информационные технологии, интернет, телеком')
    medicine = Field(13, 136, 'Медицина, фармацевтика')
    banks = Field(5, 381, 'Банки, инвестиции, лизинг')
    insurance = Field(19, 284, 'Страхование')
    law = Field(23, 100, 'Юристы')
    advert = Field(3, 234, 'Маркетинг, реклама, PR')
    accoutant = Field(2, 11, 'Бухгалтерия')
    hr = Field(6, 76, 'Управление персоналом, тренинги')
    db_session.add(it)
    db_session.add(medicine)
    db_session.add(banks)
    db_session.add(insurance)
    db_session.add(law)
    db_session.add(advert)
    db_session.add(accoutant)
    db_session.add(hr)
    db_session.commit()


def get_newest_timestamp():
    published_dates = Vacancy.query.values(Vacancy.published_date)
    return max([x[0] for x in published_dates])
