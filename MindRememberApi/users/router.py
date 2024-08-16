from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from .schemas import UserCreate
from .service import create_user


router = APIRouter()

@router.post("/users/")
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(user, db)