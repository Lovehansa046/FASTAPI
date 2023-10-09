from datetime import datetime
from typing import Optional, Union, List

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

    id = Column(Integer, primary_key=True, index=True, unique=True)
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
    isbn: str
    pageCount: int
    publishedDate: str
    thumbnailUrl: str
    shortDescription: str
    longDescription: str
    status: str

    class Config:
        orm_mode = True

class BookWithCategory(BaseModel):
    id: int
    title: str
    isbn: Optional[Union[str, None]]
    pageCount: int
    publishedDate: Optional[Union[str, datetime, None]]
    thumbnailUrl: Optional[str]
    shortDescription: Optional[Union[str, None]]
    longDescription: Optional[Union[str, None]]
    status: str
    category_name: str

    class Config:
        orm_mode = True



class UpdateAuthorRequest(BaseModel):
    author_name: str

class UpdateCategoryRequest(BaseModel):
    category_name: str


class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    pageCount: Optional[int] = None
    publishedDate: Optional[datetime] = None
    thumbnailUrl: Optional[str] = None
    shortDescription: Optional[str] = None
    longDescription: Optional[str] = None
    status: Optional[str] = None
    authors: Optional[List[str]] = None
    categories: Optional[List[str]] = None



class Authors(BaseModel):
    author_name: str

class Category(BaseModel):
    category_name: str

class CreateBook(BaseModel):
    title: str
    isbn: Optional[Union[str, None]]
    pageCount: int
    publishedDate: Optional[Union[str, datetime, None]]
    thumbnailUrl: Optional[str]
    shortDescription: Optional[Union[str, None]]
    longDescription: Optional[Union[str, None]]
