from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

Base = declarative_base()


class Credential(Base):
    __tablename__ = 'Credentials'
    id = Column(Integer, primary_key=True)
    website = Column(String(30))
    login = Column(String(30))
    passwords = relationship('Password', back_populates='credential', uselist=False, cascade='all, delete-orphan')


class Password(Base):
    __tablename__ = 'Passwords'
    id = Column(Integer, primary_key=True)
    password = Column(String)
    credential_id = Column(Integer, ForeignKey('Credentials.id'))
    credential = relationship('Credential', back_populates='passwords')


def create_database():
    engine = create_engine('sqlite:///database.db', echo=False, future=True)
    Base.metadata.create_all(engine)
    sql_session = sessionmaker(bind=engine)
    session = sql_session()

    return session
