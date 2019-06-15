
from sqlalchemy import Table, Column, Binary, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from mushroom.config import Config as conf

Base = declarative_base()

_SCHEMA = conf.SCHEMA
_SCHEMA_PREFIX = _SCHEMA + '.' if _SCHEMA else ''

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': _SCHEMA}
    id = Column(String(36), primary_key=True) #use uuid
    username = Column(String(64), unique=True)
    password = Column(String(128)) # needs to be hashed
    nickname = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    date_created = Column(DateTime, default=datetime.now())
    last_modified = Column(DateTime, default=datetime.now())
    image_file = Column(String(20), nullable=False, default='default.jpg')

    posts = relationship('Post', backref='post_author', lazy='dynamic')
    comments = relationship('Comment', backref='comment_author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>'%(self.username)


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'schema': _SCHEMA}
    id = Column(String(36), primary_key=True)
    title = Column(String(256)) 
    body = Column(String())
    like_count = Column(Integer)
    date_created = Column(DateTime)
    last_modified = Column(DateTime)

    comments = relationship('Comment')

    author = relationship('User')
    author_id = Column(String, ForeignKey(_SCHEMA_PREFIX + 'user.id'))

    def __repr__(self):
        return '<Post %r>'%(self.title)


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'schema': _SCHEMA}
    id = Column(String(36), primary_key=True)
    body = Column(String())
    like_count = Column(Integer)
    date_created = Column(DateTime)
    last_modified = Column(DateTime)

    author = relationship('User')
    author_id = Column(String(36), ForeignKey(_SCHEMA_PREFIX + 'user.id'))
    post = relationship('Post')
    post_id = Column(String(36), ForeignKey(_SCHEMA_PREFIX + 'post.id'))

    def __repr__(self):
        return '<Comment %r>'%(self.post.title)

