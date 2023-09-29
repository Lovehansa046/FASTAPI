from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector

# Замените на свои данные для подключения к базе данных MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost/books"

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаем сессию SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='books'
)

cursor = connection.cursor()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()