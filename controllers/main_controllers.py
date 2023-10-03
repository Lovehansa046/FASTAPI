from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import SessionLocal, get_db
from models.main_models import Book, Author, Categories, BookWithCategory




class BookController:

    def count_books_by_category(self, db: Session):
        # Создаем запрос для подсчета книг в каждой категории
        category_counts = db.query(Categories.category_name, func.count(Book.id).label('book_count')) \
            .outerjoin(Categories.books) \
            .group_by(Categories.category_name) \
            .all()

        # Преобразуем результаты запроса в словарь, где ключами будут названия категорий, а значениями - количество книг
        book_counts_by_category = {category_name: book_count for category_name, book_count in category_counts}

        return book_counts_by_category
    def get_books(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Book).offset(skip).limit(limit).all()

    def search_books_by_title(self, db: Session, query: str):
        books = db.query(Book).filter(Book.title.ilike(f'%{query}%')).all()
        return books

    def get_books_by_category(self, db: Session, category_name: str, skip: int = 0, limit: int = 10):
        # Поиск категории по имени
        category = db.query(Categories).filter(Categories.category_name == category_name).first()

        if category is None:
            raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")

        # Поиск книг в указанной категории
        books_with_category = db.query(Book).join(Book.categories).filter(
            Categories.category_id == category.category_id).offset(skip).limit(limit).all()

        if not books_with_category:
            raise HTTPException(status_code=404, detail=f"No books found in category '{category_name}'")

        # Создаем список экземпляров BookWithCategory с информацией о категории для каждой книги
        books_with_category_result = []
        for book in books_with_category:
            book_with_category = BookWithCategory(
                id=book.id,
                title=book.title,
                isbn=book.isbn,
                pageCount=book.pageCount,
                publishedDate=book.publishedDate,  # Преобразуем в строку
                thumbnailUrl=book.thumbnailUrl,
                shortDescription=book.shortDescription,
                longDescription=book.longDescription,
                status=book.status,
                category_name=category.category_name  # Используем имя категории
            )
            books_with_category_result.append(book_with_category)

        return books_with_category_result

class Author_Book_Controller:
    def get_author_and_books(self, db: Session, author_name: str):
        author = db.query(Author).filter(Author.author_name == author_name).first()
        if author:
            books = db.query(Book).join(Author.books).filter(Author.author_id == author.author_id).all()
            return author, books
        return None, []


