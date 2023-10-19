from datetime import datetime
from typing import Optional, Union, List

from sqlalchemy import Column, Boolean, Integer, String, Table, DateTime, ForeignKey, Text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from passlib.hash import bcrypt

from config_db.database__ITEM import SessionLocal

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
    longDescription: Optional[Union[str, None]] # Optional позволяет принять пустое значение,
                                                # а Union принимает множество значений
    status: Optional[str] = None
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
    status: Optional[str] = None


# class User(Base):
#     __tablename__ = "users"
#
#     user_id = Column(Integer, primary_key=True)
#     username = Column(String, nullable=False, unique=True)
#     name = Column(String, nullable=False)
#     surname = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     user_password = Column(String, nullable=False)
#
#     # Определите внешний ключ на столбец role_id, который ссылается на роли по role_id
#     role_id = Column(Integer, ForeignKey("roles.role_id"))
#
#
#
#
# class Role_User(Base):
#     __tablename__ = "roles"
#
#     role_id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#
# class Create_User(BaseModel):
#     username: str
#     name: str
#     surname: str
#     email: str
#     password: str
#     role: int
#
#
# class BaseUser(BaseModel):
#     name: str
#     email: Union[str, None] = None
#     surname: Union[str, None] = None


