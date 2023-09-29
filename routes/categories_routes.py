from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.categories_controller import CategoriesController
from config.database import get_db

router = APIRouter()
categories_controller = CategoriesController()

@router.get("/books/category/{category_name}")
def get_books_by_category(category_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return categories_controller.get_books_by_category(db, category_name, skip, limit)

@router.get("/categories/books/", response_model=List[dict])
def get_categories_with_book_counts(db: Session = Depends(get_db)):
    return categories_controller.get_categories_with_book_counts(db)