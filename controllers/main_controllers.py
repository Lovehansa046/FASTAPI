from sqlalchemy.orm import Session
from models.main_models import Book, Author, Categories, BookOut



def get_books_by_category_and_author(db: Session, category_name: str, author_name: str, skip: int = 0, limit: int = 10):
    # Используйте фильтры для выборки книг по имени категории и имени автора
    books = db.query(Book).join(Book.categories).join(Book.authors).filter(
        Categories.category_name == category_name,
        Author.author_name == author_name
    ).offset(skip).limit(limit).all()

    # Преобразуйте объекты книг в схемы BookOut
    books_out = []
    for book in books:
        book_out = BookOut(
            id=book.id,
            title=book.title,
            author_id=book.authors[0].author_id,  # Предполагается, что книга имеет только одного автора
            isbn=book.isbn,
            pageCount=book.pageCount,
            publishedDate=book.publishedDate.strftime('%Y-%m-%d'),  # Преобразуйте дату в строку в нужном формате
            thumbnailUrl=book.thumbnailUrl,
            shortDescription=book.shortDescription,
            longDescription=book.longDescription,
            status=book.status
        )
        books_out.append(book_out)

    return books_out


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books