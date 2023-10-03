from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.main_controllers import get_books_by_category_and_author, get_all_books
from models.main_models import BookOut, ReadableBook


router = APIRouter()

@router.get("/books/{category_name}/{author_name}", response_model=List[BookOut])
def get_books_by_category_and_author_route(
    category_name: str, author_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    books = get_books_by_category_and_author(db, category_name, author_name, skip, limit)
    return books

@router.get("/books", response_model=List[ReadableBook])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = get_all_books(db, skip=skip, limit=limit)
    return books