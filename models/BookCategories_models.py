from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class BookCategory(Base):
    __tablename__ = "BookCategories"

    id = Column(Integer, primary_key=True, index=True)
    bookid = Column(Integer, ForeignKey('book.id'))
    categoryid = Column(Integer, ForeignKey('Category.id'))

    # Определяем связи с книгами и категориями
    book = relationship("Book", back_populates="book_categoies")
    category = relationship("Category", back_populates="book_categoies")
