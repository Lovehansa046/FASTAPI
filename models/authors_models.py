from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

from models.bookauthors_models import author_book_association

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255))

    books = relationship("Books", secondary=author_book_association, back_populates="authors")


class ReadableAuthor(BaseModel):
    name: str