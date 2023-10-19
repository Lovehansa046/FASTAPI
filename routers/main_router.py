from typing import List, Union


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from auth.database import get_db, User
from auth.schemas import UpdateUserData
from config_db.database__ITEM import get_sync_db

from models.main_models import UpdateAuthorRequest, UpdateCategoryRequest, \
    UpdateBookRequest, CreateBook, Author, Book
from fastapi.responses import JSONResponse
from controllers.main_controllers import BookController, Author_Book_Controller, Category_controller

from sqlalchemy.future import select

from routers.test_auth_router import current_user

book_controller = BookController()
author_book_controller = Author_Book_Controller()
category_controller = Category_controller()

router = APIRouter()


def get_current_user(user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def get_current_user_role(user: User = Depends(get_current_user)):
    # Предположим, что у вас есть поле "role" в модели User, которое определяет роль пользователя
    if user.role_id != 2:  # Замените "admin" на вашу роль
        raise HTTPException(status_code=403, detail="YOU DON'T ADMIN")
    return user

@router.put("/user/update", response_model=None)
def update_user_data(
        verify_account_name: str,
    updated_data: UpdateUserData,
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что пользователь пытается обновить свой собственный профиль
    if verify_account_name != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can only update your own profile data."
        )

    # Обновляем данные пользователя
    current_user.username = updated_data.username
    current_user.email = updated_data.email

    # Здесь вы можете сохранить обновленные данные в вашем хранилище, например, в базе данных

    # Возвращаем обновленные данные пользователя
    return current_user

@router.get("/books/", response_class=JSONResponse)
async def read_all_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    books = await book_controller.get_books(db, skip=skip, limit=limit)
    # Предполагается, что books - это список словарей, представляющих данные о книгах
    return books


@router.get("/books/word/{query}", response_class=JSONResponse)
async def search_books_by_title(query: str, db: AsyncSession = Depends(get_db)):  # Добавлено ключевое слово async
    books = await book_controller.search_books_by_title(db, query)  # Используется await для выполнения асинхронной операции

    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with '{query}' in the title.")

    return books


@router.get("/author/{author_name}")
async def get_author_and_books_route(author_name: str, db: AsyncSession = Depends(get_db)):
    author, books = await author_book_controller.get_author_and_books(db, author_name)
    if author:
        return {"author": author, "books": books}
    raise HTTPException(status_code=404, detail="Author not found")



@router.get("/books/category/{category_name}")
async def get_books_by_category(category_name: str, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    books = await book_controller.get_books_by_category(db, category_name, skip, limit)
    return books


@router.get("/count-books-by-category")
async def get_count_books_by_category(db: AsyncSession = Depends(get_db)):
    return await book_controller.count_books_by_category(db)


@router.put("/authors/{author_id}", response_model=UpdateAuthorRequest)
async def update_author_route(author_id: int, request: UpdateAuthorRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_role)):
    author = await author_book_controller.update_author(db, author_id, request)
    return author


@router.put("/categories/{category_id}", response_model=UpdateCategoryRequest)
async def update_category_route(category_id: int, request: UpdateCategoryRequest, db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user_role)):
    category = await category_controller.update_category(db, category_id, request)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/books/{book_id}", response_model=UpdateBookRequest)
async def update_book_route(
        book_id: int,
        request: UpdateBookRequest,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),

):
    book = book_controller.update_book(db, book_id, request)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/author/{author_id}", response_model=dict)
def delete_author(
        author_id: int,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),
):
    try:
        author_book_controller.delete_author_and_associated_books(db, author_id)
        return {"message": "Author and associated data have been deleted"}
    except HTTPException as e:
        raise e


@router.delete("/category/{category_id}", response_model=dict)
def delete_category(
        category_id: int,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),

):
    try:
        category_controller.delete_category_and_associated_books(db, category_id)
        return {"message": "Category and associated data have been deleted"}
    except HTTPException as e:
        raise e


@router.delete("/book/{book_id}", response_model=dict)
def delete_book(
        book_id: int,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),

):
    try:
        book_controller.delete_book_and_associated_data(db, book_id)
        return {"message": "Book and associated data have been deleted"}
    except HTTPException as e:
        raise e


@router.post("/authors/author", response_model=None)
def add_author(
        author_name: str,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),

):
    try:
        author = author_book_controller.create_author(db, author_name)
        return {"message": "Author added successfully", "author": author}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categories/category", response_model=None)
def add_category(
        category_name: str,
        db: Session = Depends(get_sync_db),
        user: User = Depends(get_current_user_role),

):
    try:
        category = category_controller.create_category(db, category_name)
        return {"message": "Category created successfully", "category_id": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/books/book")
async def create_book(book_data: CreateBook, author_names: List[str], category_names: List[str],
                      db: Session = Depends(get_sync_db), user: User = Depends(get_current_user_role)):
    try:
        result = book_controller.create_book_with_authors_and_categories(db, book_data, author_names, category_names)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": False,
#     },
# }



# @router.post("/users/")
# def create_new_user(user_data: Create_User, db: Session = Depends(get_db)):
#     # Вызовите функцию create_user для создания нового пользователя
#     new_user = users.create_user(db, user_data)
#
#     # Верните созданного пользователя в качестве результата
#     return new_user
#


