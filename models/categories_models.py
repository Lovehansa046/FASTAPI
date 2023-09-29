from typing import Optional

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


Base = declarative_base()

class UpdateCategoryRequest(BaseModel):
    name: str

class Categories(Base):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class ReadableCategories(BaseModel):
    name: str