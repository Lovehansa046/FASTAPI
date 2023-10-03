# models.py

from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# Многие ко многим связь таблиц для авторов и книг
author_book_association = Table('bookauthors', Base.metadata,
                                Column('author_id', Integer, ForeignKey('authors.author_id')),
                                Column('book_id', Integer, ForeignKey('books.id'))
                                )

# Многие ко многим связь таблиц для книг и категорий
book_category_association = Table('bookcategories', Base.metadata,
                                  Column('book_id', Integer, ForeignKey('books.id')),
                                  Column('category_id', Integer, ForeignKey('categories.category_id'))
                                  )

class UpdateCategoryRequest(BaseModel):
    name: str

class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255))

    books = relationship('Book', secondary=book_category_association, back_populates='categories')

class ReadableCategories(BaseModel):
    name: str

class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255))

    books = relationship("Book", secondary=author_book_association, back_populates="authors")

class ReadableAuthor(BaseModel):
    name: str

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    isbn = Column(String(255))
    pageCount = Column(Integer)
    publishedDate = Column(DateTime)
    thumbnailUrl = Column(String(255))
    shortDescription = Column(Text)
    longDescription = Column(Text)
    status = Column(String(255))

    categories = relationship('Categories', secondary=book_category_association, back_populates='books')
    authors = relationship('Author', secondary=author_book_association, back_populates='books')

class ReadableBook(BaseModel):
    title: str
    isbn: str
    pageCount: int
    publishedDate: str
    thumbnailUrl: str
    shortDescription: str
    longDescription: str
    status: str

class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    isbn: str
    pageCount: int
    publishedDate: str
    thumbnailUrl: str
    shortDescription: str
    longDescription: str
    status: str

    class Config:
        orm_mode = True
