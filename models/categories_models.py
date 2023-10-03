from typing import Optional

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from models.books_models import Book



from models.BookCategories_models import book_category_association

Base = declarative_base()

class UpdateCategoryRequest(BaseModel):
    name: str

class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255))

    books = relationship('Book', secondary=book_category_association, back_populates='categories')

class ReadableCategories(BaseModel):
    name: str