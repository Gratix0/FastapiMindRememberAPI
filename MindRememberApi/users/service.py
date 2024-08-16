from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .models import User
from .schemas import UserCreate


async def create_user(user: UserCreate, db: AsyncSession):
    # Проверка на наличие пользователя с таким же логином
    result = await db.execute(select(User).where(User.login == user.login))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует."
        )

    new_user = User(**user.dict())

    try:
        db.add(new_user)
        await db.commit()  # Не забудьте await
        await db.refresh(new_user)  # Не забудьте await
    except IntegrityError:  # В случае нарушения уникальности
        await db.rollback()  # Откат транзакции
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует."
        )

    return new_user