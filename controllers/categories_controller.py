from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

# from models.BookCategories_models import BookCategory
from models.authors_models import Author
# from models.bookauthors_models import BookAuthor
from models.categories_models import Categories
from models.books_models import Book
from config.database import get_db

class CategoriesController:

    def get_books_by_category(self, db: Session, category_name: str, skip: int = 0, limit: int = 10):
        category = db.query(Categories).filter(Categories.category_name == category_name).first()

        if category is None:
            # Если категория не найдена, вы можете вернуть пустой список или бросить исключение HTTPException с кодом 404
            return []

        books_with_category = db.query(Book).join(Book.categories).filter(
            Categories.id == category.category_id).offset(skip).limit(limit).all()

        books_list = []
        for book in books_with_category:
            # Здесь вы можете добавить любую другую информацию о книге, которую вы хотите включить в результат
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
            }
            books_list.append(book_dict)

        return books_list

    def count_books_by_category(self, db: Session):
        # Выполнить запрос для подсчета количества книг в каждой категории
        category_counts = db.query(Categories.category_name, func.count(BookCategory.book_id)).join(BookCategory).group_by(
            Categories.category_name).all()

        # Создать словарь для хранения результатов
        category_counts_dict = {}
        for category_name, book_count in category_counts:
            category_counts_dict[category_name] = book_count

        return category_counts_dict


