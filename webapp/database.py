from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from flask import current_app


# engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
engine = create_engine('sqlite:///vacancies_sj.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()



def init_db():
    from webapp.models import Vacancy, Salary
    Base.metadata.create_all(bind=engine)