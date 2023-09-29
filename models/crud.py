# crud.py

from sqlalchemy.orm import Session
from models.books_models import Book

def delete_book_and_relations(db: Session, book_id: int):
    # Найдите книгу в базе данных по её идентификатору
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        return False  # Книга не найдена

    # Удалите книгу и её связи (например, авторов и категории)
    db.delete(book)
    db.commit()
    return True  # Книга успешно удалена


