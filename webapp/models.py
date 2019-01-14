from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///777.db', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


vac_spec = Table(
    'vacancy_specialization', Base.metadata,
    Column('vacancy_id', Integer, ForeignKey('vacancies.id_vacancy')),
    Column('specialization_id', Integer, ForeignKey('specializations.id_specialization'))
)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id_vacancy = Column(Integer, primary_key=True)
    # hash = None  # how to create?
    id_on_site = Column(Integer, unique=True)
    title = Column(String, nullable=False)
    published_date = Column(Integer)
    description = Column(String)
    firm = Column(String)
    address = Column(String)
    town = Column(String, nullable=False)
    metro = Column(String)
    type_of_work = Column(String)
    experience = Column(String)
    specializations = relationship('Specialization', secondary=vac_spec)
    is_archive = Column(Boolean)
    added_to_db_at = Column(Integer)
    url = Column(String, unique=True)
    source = Column(String, default='SuperJob')


    def __init__(self, id_on_site, title, published_date, description, firm,
                 address, town, metro, type_of_work, experience, is_archive,
                 added_to_db_at, url):
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
        self.is_archive = is_archive
        self.added_to_db_at = added_to_db_at
        self.url = url

    def __repr__(self):
        return f'<Vacancy {self.url}>'


class Salary(Base):
    __tablename__ = 'salaries'
    id_salary = Column(Integer, primary_key=True)
    agreement = Column(Boolean)
    payment_from = Column(Integer)
    payment_to = Column(Integer)
    currency = Column(String)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id_vacancy'))
    vacancy = relationship(Vacancy, backref=backref('salary', uselist=False))

    def __init__(self, agreement, payment_from, payment_to, currency, vacancy):
        self.agreement = agreement
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = currency
        self.vacancy = vacancy

    def __repr__(self):
        return f'<Salary {self.payment_from}>'


class Specialization(Base):
    __tablename__ = 'specializations'
    id_specialization = Column(Integer, primary_key=True)
    id_hh = Column(Integer, unique=True)
    id_sj = Column(Integer, unique=True)
    name = Column(String)

    def __init__(self, id_hh, id_sj, name):
        self.id_hh = id_hh
        self.id_sj = id_sj
        self.name = name

    def __repr__(self):
        return f'<Specialization> {self.name}'


def init_db():
    Base.metadata.create_all(bind=engine)


def add_specializations():
    it = Specialization(1, 33, 'Информационные технологии, интернет, телеком')
    medicine = Specialization(13, 136, 'Медицина, фармацевтика')
    banks = Specialization(5, 381, 'Банки, инвестиции, лизинг')
    insurance = Specialization(19, 284, 'Страхование')
    law = Specialization(23, 100, 'Юристы')
    advert = Specialization(3, 234, 'Маркетинг, реклама, PR')
    accoutnant = Specialization(11, 2, 'Бухгалтерия')
    hr = Specialization(6, 76, 'Управление персоналом, тренинги')
    db_session.add(it)
    db_session.add(medicine)
    db_session.add(banks)
    db_session.add(insurance)
    db_session.add(law)
    db_session.add(advert)
    db_session.add(accoutnant)
    db_session.add(hr)
    db_session.commit()


def get_newest_timestamp():
    published_dates = Vacancy.query.values(Vacancy.published_date)
    return max([x[0] for x in published_dates])
