from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db, SessionLocal
from models.main_models import Book, ReadableBook, Categories, UpdateAuthorRequest, Author
from fastapi.responses import JSONResponse
from controllers.main_controllers import BookController, Author_Book_Controller

book_controller = BookController()
author_book_controller = Author_Book_Controller()

router = APIRouter()

@router.get("/books/", response_class=JSONResponse)
def read_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = book_controller.get_books(db, skip=skip, limit=limit)
    # Предполагается, что books - это список словарей, представляющих данные о книгах
    return books

@router.get("/books/word/{query}", response_class=JSONResponse)
def search_books_by_title(query: str, db: Session = Depends(get_db)):
    books = book_controller.search_books_by_title(db, query)

    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with '{query}' in the title.")

    # Предположим, что books - это список словарей с информацией о книгах
    return books

@router.get("/author/{author_name}")
def get_author_and_books_route(author_name: str, db: Session = Depends(get_db)):
    author, books = author_book_controller.get_author_and_books(db, author_name)
    if author:
        return {"author": author, "books": books}
    raise HTTPException(status_code=404, detail="Author not found")

@router.get("/books/category/{category_name}")
def get_books_by_category(category_name: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    books = book_controller.get_books_by_category(db, category_name, skip, limit)
    return books

@router.get("/count-books-by-category")
def get_count_books_by_category(db: Session = Depends(get_db)):
    return book_controller.count_books_by_category(db)


@router.put("/authors/{author_id}", response_model=UpdateAuthorRequest)
async def update_author_route(author_id: int, request: UpdateAuthorRequest, db: Session = Depends(get_db)):
    author = author_book_controller.update_author(db, author_id, request)
    return author