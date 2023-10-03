from sqlalchemy.orm import Session
from models.authors_models import Author
from models.books_models import Book
# from models.bookauthors_models import BookAuthor

class AuthorController:
    def get_author_and_books(self, db: Session, author_name: str):
        author = db.query(Author).filter(Author.author_name == author_name).first()
        if author:
            books = db.query(Book.title).join(BookAuthor, Book.id == BookAuthor.book_id).filter(BookAuthor.author_id == author.author_id).all()
            return author, [book.title for book in books]
        return None, []
