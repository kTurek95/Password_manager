"""
SQLAlchemy Models Module

This module defines the structure of the tables used in the application's database
using SQLAlchemy ORM. It includes classes representing each table, with fields
defined as class attributes and relationships between tables where applicable.

Classes:
    Credential - Represents the Credentials table with fields for Login and Website.
    Password - Represents the Password table with fields for Password.
    LoginCrednetials - Represents the LoginCredentials table with fields for Login and Passowrd.

"""

from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

Base = declarative_base()

# pylint: disable=too-few-public-methods
class Credential(Base):
    """
        Represents the 'Credentials' table within the database,
        holding login information for various websites.

        Attributes:
            __tablename__ (str):
            The name of the table in the database to which this class is mapped.
            id (Column): The primary key column of the table,
            stores unique identifiers for each record as integers.
            website (Column): A string column meant to store the name of the website
            to which the credentials belong.
            login (Column): A string column to store the login name or user ID
            associated with the credentials.
            passwords (relationship):
            A one-to-one relationship to the 'Password' model, representing the password
            associated with these credentials. It is set not to use a list (uselist=False),
            meaning it supports a single value association. Cascading options are set to
            automatically handle orphaned password records by deleting them.
        """
    __tablename__ = 'Credentials'
    id = Column(Integer, primary_key=True)
    username_id = Column(Integer, ForeignKey('LoginCredentials.id'))
    website = Column(String(30))
    login = Column(String(30))
    passwords = relationship('Password',
                             back_populates='credential',
                             uselist=False,
                             cascade='all, delete-orphan')
    login_credentials = relationship('LoginCredentials',
                                     back_populates='credential')


class Password(Base):
    """
        Represents the 'Passwords' table within the database,
        which stores password information.

        Attributes:
            __tablename__ (str):
            The name of the table in the database to which this class is mapped.
            id (Column): The primary key column of the table,
            stores unique identifiers for each record as integers.
            password (Column): A string column that stores the actual password text.
            credential_id (Column): An integer column set as a foreign key
            that links a password to its corresponding
                                    credential by the 'credential_id' of the 'Credentials' table.
            credential (relationship):
            A relationship to the 'Credential' model that defines a back-population. This
            allows access to the associated credential from the 'Password' side and enables
            bidirectional behavior.

        Note:
            Each 'Password' record is associated with a 'Credential' record
            through the 'credential_id' field,
            and this association is made explicit by the relationship attribute in both models.
        """
    __tablename__ = 'Passwords'
    id = Column(Integer, primary_key=True)
    password = Column(String)
    credential_id = Column(Integer, ForeignKey('Credentials.id'))
    credential = relationship('Credential', back_populates='passwords')


class LoginCredentials(Base):
    """
    Database table model for LoginCredentials.

    This class represents user records in the database, containing user authentication details.
    It includes fields for the username, password, password confirmation, and email address.
    This class is also linked to the Credential table through a relationship, allowing access
    to associated authentication data.

    Attributes:
        id (Integer): Unique identifier for the user, primary key.
        username (String): Username of the user.
        password (String): Password of the user.
        confirm_password (String): Password confirmation for the user.
        email (String): Email address of the user.
        credential (relationship): Relationship with the Credential table.
    """
    __tablename__ = 'LoginCredentials'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    confirm_password = Column(String)
    email = Column(String)
    credential = relationship('Credential',
                              back_populates='login_credentials')


def create_database():
    """
       Creates a new SQLite database named 'database.db'
       and initializes tables based on the Base metadata.

       This function sets up a new SQLite database
       using SQLAlchemy's create_engine function with specified configurations.
       It then uses the metadata from the Base class to create all the defined tables within
       the newly created database.
       Finally, it prepares a sessionmaker instance which can be used to create
       sessions for interacting with the database.

       Returns:
           session (Session):
           A SQLAlchemy Session object that can be used to interact with the database.

       Example:
           To create a new database and start a session, simply call:

           ->     session = create_database()

           You can then use this session object to add, delete or query the database.
    """
    engine = create_engine('sqlite:///database.db',
                           echo=False,
                           future=True)
    Base.metadata.create_all(engine)
    sql_session = sessionmaker(bind=engine)
    session = sql_session()

    return session
