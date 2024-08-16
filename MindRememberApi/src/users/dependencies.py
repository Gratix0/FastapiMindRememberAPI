from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.models import User
from src.users.schemas import UserCreate

async def check_unique_login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка на наличие пользователя с таким же логином
    result = await db.execute(select(User).where(User.login == user.login))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином уже зарегистрирован в базе данных."
        )
