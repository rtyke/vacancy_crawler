from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///vacancies_sj1401.db', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()



class Vacancy(Base):
    __tablename__ = 'vacancies'
    pk = Column(Integer, primary_key=True)
    # hash = None  # how to create?
    id_on_site = Column('id_on_site', Integer, unique=True)
    title = Column('title', String, nullable=False)
    published_date = Column('published_date', Integer)
    description = Column('description', String)
    firm = Column('firm', String)
    address = Column('address', String)
    town = Column('town', String, nullable=False)
    metro = Column('metro', String)
    type_of_work = Column('type_of_work', String)
    experience = Column('experience', String)
    specializations = Column('specializations', String)
    is_archive = Column('is_archive', Boolean)
    added_to_db_at = Column('added_to_db_at', Integer)
    url = Column('url', String, unique=True)
    source = Column('source', String, default='SuperJob')

    def __init__(self, id_on_site, title, published_date, description, firm,
                 address, town, metro, type_of_work, experience, specializations,
                 is_archive, added_to_db_at, url):
        self.id_on_site = id_on_site
        self.title = title
        self.published_date = published_date
        self.description = description
        self.firm = firm
        self.address = address
        self.town = town
        self.metro = metro
        self.type_of_work = type_of_work
        self.experience = experience
        self.specializations = specializations
        self.is_archive = is_archive
        self.added_to_db_at = added_to_db_at
        self.url = url

    def __repr__(self):
        return f'<Vacancy {self.url}>'


class Salary(Base):
    __tablename__ = 'salary'
    pk = Column(Integer, primary_key=True)
    agreement = Column('agreement', Boolean)
    payment_from = Column('payment_from', Integer)
    payment_to = Column('payment_to', Integer)
    currency = Column('currency', String)
    vacancy_pk = Column(Integer, ForeignKey('vacancies.pk'))
    vacancy = relationship(Vacancy, backref=backref('salary', uselist=False))

    def __init__(self, agreement, payment_from, payment_to, currency, vacancy):
        self.agreement = agreement
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = currency
        self.vacancy = vacancy


def init_db():
    Base.metadata.create_all(bind=engine)


def get_newest_timestamp():
    published_dates = Vacancy.query.values(Vacancy.published_date)
    return max([x[0] for x in published_dates])
