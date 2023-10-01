from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.BookCategories_models import BookCategory
from models.authors_models import Author
from models.bookauthors_models import BookAuthor
from models.categories_models import Categories
from models.books_models import Book
from config.database import get_db

class CategoriesController:
    def get_books_by_category(self, db: Session, category_name: str, skip: int = 0, limit: int = 10):
        category = db.query(Categories).filter(Categories.name == category_name).first()

        if category is None:
            raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")

        books_with_category = db.query(Book).join(BookCategory, Book.id == BookCategory.bookid).filter(
            BookCategory.categoryid == category.id).offset(skip).limit(limit).all()

        if not books_with_category:
            raise HTTPException(status_code=404, detail=f"No books found in category '{category_name}'")

        books_list = []
        for book in books_with_category:
            # Получить информацию об авторе книги
            author = db.query(Author).join(BookAuthor, Author.id == BookAuthor.authorid).filter(
                BookAuthor.bookid == book.id).first()

            # Создать словарь для книги, включая информацию о категории и авторе
            book_dict = {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "pageCount": book.pageCount,
                "publishedDate": book.publishedDate,
                "thumbnailUrl": book.thumbnailUrl,
                "shortDescription": book.shortDescription,
                "longDescription": book.longDescription,
                "status": book.status,
                # Добавить информацию о категории в словарь
                "category": category.name,
                # Добавить информацию об авторе в словарь
                "author": author.name
                if author else None
            }
            books_list.append(book_dict)

        return books_list

    def count_books_by_category(self, db: Session):
        # Выполнить запрос для подсчета количества книг в каждой категории
        category_counts = db.query(Categories.name, func.count(BookCategory.bookid)).join(BookCategory).group_by(
            Categories.name).all()

        # Создать словарь для хранения результатов
        category_counts_dict = {}
        for category_name, book_count in category_counts:
            category_counts_dict[category_name] = book_count

        return category_counts_dict


