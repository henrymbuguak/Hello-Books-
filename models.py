from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
import datetime


class RolesUsers(Base):
    __tablename__ = 'role_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='role_users', backref=backref('users', lazy='dynamic'))


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    created_on = Column(DateTime(), default=datetime.datetime.now())
    updated_on = Column(DateTime(), default=datetime.datetime.now())


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_on = Column(DateTime(), default=datetime.datetime.now())
    updated_on = Column(DateTime(), default=datetime.datetime.now())


class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_on = Column(DateTime(), default=datetime.datetime.now())
    updated_on = Column(DateTime(), default=datetime.datetime.now())


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    author = Column('author', Integer(), ForeignKey('author.id'))
    genre = Column('genre', Integer(), ForeignKey('genre.id'))
    language = Column('language', Integer(), ForeignKey('language.id'))
    summary = Column(String(255))
    created_on = Column(DateTime(), default=datetime.datetime.now())
    updated_on = Column(DateTime(), default=datetime.datetime.now())