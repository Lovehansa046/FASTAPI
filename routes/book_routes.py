from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from controllers.book_controller import BookCategoryController
from config.database import get_db  # Функция для получения подключения к базе данных
from jinja2 import Template
from fastapi.responses import HTMLResponse
from controllers.book_controller import BookController
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse



router = APIRouter()
book_category_controller = BookCategoryController()
book_controller = BookController()


@router.get("/books/word/{query}", response_class=JSONResponse)
def search_books_by_title(query: str, db: Session = Depends(get_db)):
    books = book_controller.search_books_by_title(db, query)

    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with '{query}' in the title.")

    # Предположим, что books - это список словарей с информацией о книгах
    return books


@router.get("/books/", response_class=JSONResponse)
def read_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = book_controller.get_books(db, skip=skip, limit=limit)
    # Предполагается, что books - это список словарей, представляющих данные о книгах
    return books