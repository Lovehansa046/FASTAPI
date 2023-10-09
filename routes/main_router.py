from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.main_models import Book, UpdateAuthorRequest, UpdateCategoryRequest, \
    UpdateBookRequest, CreateBook
from fastapi.responses import JSONResponse
from controllers.main_controllers import BookController, Author_Book_Controller, Category_controller

book_controller = BookController()
author_book_controller = Author_Book_Controller()
category_controller = Category_controller()

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

@router.put("/categories/{category_id}", response_model=UpdateCategoryRequest)
async def update_category_route(category_id: int, request: UpdateCategoryRequest, db: Session = Depends(get_db)):
    category = category_controller.update_category(db, category_id, request)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/books/{book_id}", response_model=UpdateBookRequest)
async def update_book_route(
    book_id: int,
    request: UpdateBookRequest,
    db: Session = Depends(get_db)
):
    book = book_controller.update_book(db, book_id, request)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/author/{author_id}", response_model=dict)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    try:
        author_book_controller.delete_author_and_associated_books(db, author_id)
        return {"message": "Author and associated data have been deleted"}
    except HTTPException as e:
        raise e

@router.delete("/category/{category_id}", response_model=dict)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    try:
        category_controller.delete_category_and_associated_books(db, category_id)
        return {"message": "Category and associated data have been deleted"}
    except HTTPException as e:
        raise e


@router.delete("/book/{book_id}", response_model=dict)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    try:
        book_controller.delete_book_and_associated_data(db, book_id)
        return {"message": "Book and associated data have been deleted"}
    except HTTPException as e:
        raise e

@router.post("/authors/author", response_model=None)
def add_author(
    author_name: str,
    db: Session = Depends(get_db),
):
    try:
        author = author_book_controller.create_author(db, author_name)
        return {"message": "Author added successfully", "author": author}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categories/category", response_model=None)
def add_category(
    category_name: str,
    db: Session = Depends(get_db),
):
    try:
        category = category_controller.create_category(db, category_name)
        return {"message": "Category created successfully", "category_id": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/books/book")
async def create_book(book_data: CreateBook, author_names: List[str], category_names: List[str], db: Session = Depends(get_db)):
    try:
        result = book_controller.create_book_with_authors_and_categories(db, book_data, author_names, category_names)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))