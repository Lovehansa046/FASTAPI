from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.BookCategories_models import BookCategory
from models.categories_models import Categories
from models.books_models import Book
from config.database import get_db

class CategoriesController:
    def get_books_by_category(self, db: Session, category_name: str, skip: int = 0, limit: int = 10):
        category = db.query(Categories).filter(Categories.name == category_name).first()

        if category is None:
            raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")

        books_with_category = db.query(Book).join(BookCategory, Book.id == BookCategory.bookid).filter(BookCategory.categoryid == category.id).offset(skip).limit(limit).all()

        if not books_with_category:
            raise HTTPException(status_code=404, detail=f"No books found in category '{category_name}'")

        return books_with_category

    def get_categories_with_book_counts(self, db: Session) -> List[dict]:
        categories_with_counts = (
            db.query(Categories.name, func.count(BookCategory.bookid).label('book_count'))
            .join(BookCategory, Categories.id == BookCategory.categoryid)
            .group_by(Categories.name)
            .all()
        )

        result = [{"category_name": name, "book_count": count} for name, count in categories_with_counts]
        return result