from typing import List

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.main_models import Book, Author, Categories, BookWithCategory, UpdateAuthorRequest, UpdateCategoryRequest, \
    UpdateBookRequest, CreateBook


class BookController:

    def create_book_with_authors_and_categories(self, db: Session, book_data: CreateBook, author_names: List[str],
                                                category_names: List[str]):
        try:
            # Создаем список авторов и категорий
            authors = []
            for author_name in author_names:
                author = Author_Book_Controller.get_author_by_name(db, author_name)
                if author is None:
                    author = Author_Book_Controller.create_author(db, author_name)
                authors.append(author)

            categories = []
            for category_name in category_names:
                category = Category_controller.get_category_by_name(db, category_name)
                if category is None:
                    category = Category_controller.create_category(db, category_name)
                categories.append(category)

            new_book = Book(**book_data.dict())

            # Связываем книгу с авторами и категориями
            new_book.authors.extend(authors)
            new_book.categories.extend(categories)

            db.add(new_book)
            db.commit()
            db.refresh(new_book)

            # Получаем информацию о созданных авторах и категориях
            author_info = [{"id": author.author_id, "name": author.author_name} for author in authors]
            category_info = [{"id": category.category_id, "name": category.category_name} for category in categories]

            return {
                "book": new_book,
                "authors": author_info,
                "categories": category_info
            }
        except Exception as e:
            db.rollback()
            raise e


    def delete_book_and_associated_data(self, db: Session, book_id: int):
        book = db.query(Book).filter(Book.id == book_id).first()

        if book:
            # Удалите связи книги с авторами (пример)
            for author in book.authors:
                book.authors.remove(author)

            # Удалите связи книги с категориями (пример)
            for category in book.categories:
                book.categories.remove(category)

            # Теперь удалите саму книгу
            db.delete(book)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def update_book(self, db: Session, book_id: int, request: UpdateBookRequest):
        book = db.query(Book).filter(Book.id == book_id).first()

        if book:
            updated = False  # Флаг, чтобы определить, были ли какие-либо обновления

            if request.authors:
                for author_name in request.authors:
                    author = db.query(Author).filter(Author.author_name == author_name).first()
                    if not author:
                        author = Author(author_name=author_name)
                        db.add(author)
                    if author not in book.authors:
                        book.authors.append(author)
                    updated = True

            if request.categories:
                for category_name in request.categories:
                    category = db.query(Categories).filter(Categories.category_name == category_name).first()
                    if not category:
                        category = Categories(category_name=category_name)
                        db.add(category)
                    if category not in book.categories:
                        book.categories.append(category)
                    updated = True

            # Обновление остальных полей книги, если они указаны в запросе
            for field in ["title", "isbn", "pageCount", "publishedDate", "thumbnailUrl", "shortDescription",
                          "longDescription", "status"]:
                if hasattr(request, field) and getattr(request, field) is not None:
                    setattr(book, field, getattr(request, field))
                    updated = True

            if updated:
                db.flush()  # Сохранение новых авторов и категорий, если они были созданы
                db.commit()
                return {"message": "Book updated successfully"}  # Вернуть подтверждение об успешном обновлении
        raise HTTPException(status_code=404, detail="Book not found")

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

    def delete_author_and_associated_books(self, db: Session, author_id: int):
        author = db.query(Author).filter(Author.author_id == author_id).first()

        if author:
            # Удалите связи автора с книгами (пример)
            for book in author.books:
                author.books.remove(book)

            # Теперь удалите самого автора
            db.delete(author)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Author not found")
    def get_author_and_books(self, db: Session, author_name: str):
        author = db.query(Author).filter(Author.author_name == author_name).first()
        if author:
            books = db.query(Book).join(Author.books).filter(Author.author_id == author.author_id).all()
            return author, books
        return None, []

    def update_author(self, db: Session, author_id: int, request: UpdateAuthorRequest):
        author = db.query(Author).filter(Author.author_id == author_id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        author.author_name = request.author_name
        db.commit()
        db.refresh(author)

        return author

    @staticmethod
    def get_author_by_name(db: Session, author_name: str):
        return db.query(Author).filter(Author.author_name == author_name).first()

    @staticmethod
    def create_author(db: Session, author_name: str):
        author = Author(author_name=author_name)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    def create_author(self, db: Session, author_name: str):
        author = Author(author_name=author_name)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author


class Category_controller:

    def create_category(self, db: Session, category_name: str):
        category = Categories(category_name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_category_by_name(db: Session, category_name: str):
        return db.query(Categories).filter(Categories.category_name == category_name).first()

    @staticmethod
    def create_category(db: Session, category_name: str):
        category = Categories(category_name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def update_category(self, db: Session, category_id: int, request: UpdateCategoryRequest):
        category = db.query(Categories).filter(Categories.category_id == category_id).first()

        if category:
            category.category_name = request.category_name
            db.commit()
            db.refresh(category)
            return category
        return None

    def delete_category_and_associated_books(self, db: Session, category_id: int):
        category = db.query(Categories).filter(Categories.category_id == category_id).first()

        if category:
            # Удалите связи категории с книгами (пример)
            for book in category.books:
                category.books.remove(book)

            # Теперь удалите саму категорию
            db.delete(category)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Category not found")

