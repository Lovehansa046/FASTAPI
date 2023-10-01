from sqlalchemy import func

from models.BookCategories_models import BookCategory
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.books_models import Book


class BookCategoryController:
    def get_categories_by_book_id(self, db: Session, book_id: int):
        categories = db.query(BookCategory).filter(BookCategory.bookid == book_id).all()
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        return categories

class BookController:
    def search_books_by_title(self, db: Session, query: str):
        books = db.query(Book).filter(Book.title.ilike(f'%{query}%')).all()
        return books

    def get_books(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Book).offset(skip).limit(limit).all()