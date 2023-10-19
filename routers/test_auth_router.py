from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import User, get_db
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate


router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@router.get("/users/me")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@router.get("/users/all")
async def protected_route(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    # Создайте объект запроса
    stmt = select(User)

    # Выполните запрос и получите результат
    result = await db.execute(stmt)

    # Получите список пользователей из результата
    users = result.scalars().all()

    user_list = [{"Username": user.username, "Email": user.email} for user in users]

    response_data = {
        "message": f"Hello, {user.username}",
        "users": user_list
    }

    return response_data

@router.get("/anonyms")
def unprotected_route():
    return f"Hello, anonym"

