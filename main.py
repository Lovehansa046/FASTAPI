from jinja2 import Template
from sqlalchemy.orm import Session

from config.database import get_db
from models.BookCategories_models import BookCategory
from models.books_models import Book
from models.categories_models import Categories
from routes.book_routes import router as book_router
from routes.author_routes import router as author_router
from routes.categories_routes import router as category_router

from fastapi.responses import HTMLResponse




from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()




app.include_router(category_router)
app.include_router(book_router)
app.include_router(author_router)