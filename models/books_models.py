
from sqlalchemy import Column, Integer, String, DateTime, Table,  Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel


Base = declarative_base()

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
