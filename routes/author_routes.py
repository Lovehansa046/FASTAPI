from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from controllers.author_controller import AuthorController
from config.database import get_db
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.books_models import BookOut

router = APIRouter()
author_controller = AuthorController()


@router.get("/booksauthors/{author_name}")
async def get_author_and_books(author_name: str, db: Session = Depends(get_db)):
    author, books = author_controller.get_author_and_books(db, author_name)
    if author is None:
        raise HTTPException(status_code=404, detail=f"Author '{author_name}' not found")

    # Подготовим данные в формате словаря
    response_data = {
        "authors": {
            "author_id": author.author_id,
            "author_name": author.author_name,
            # Другие данные об авторе, которые вы хотите включить
        },
        "books": books  # Список названий книг
    }

    return response_data



