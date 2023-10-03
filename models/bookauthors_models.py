from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

author_book_association = Table(
    'author_book_association',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.author_id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)