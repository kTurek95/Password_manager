from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Credential(Base):
    __tablename__ = 'Credentials'
    id = Column(Integer, primary_key=True)
    website = Column(String(30))
    login = Column(String(30))
    passwords = relationship('Password', back_populates='credential', uselist=False, cascade='all, delete-orphan')
