from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BookAuthor(Base):
    __tablename__ = "BookAuthors"

    id = Column(Integer, primary_key=True, index=True)
    bookid = Column(Integer, ForeignKey('books.id'))
    authorid = Column(Integer, ForeignKey('authors.id'))

    # Определяем связи с книгами и авторами (если необходимо)
    book = relationship("Book", back_populates="book_authors")
    author = relationship("Author", back_populates="book_authors")