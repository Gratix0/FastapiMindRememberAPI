# Import necessary libraries and modules
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Cookie, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

# Local imports
from .dependencies import check_unique_login  # Import function to check unique login
from .models import User, Folder, KnowledgeQueue, Record, Theme  # Import models
from .schemas import UserCreate, UserInDB, TokenData, FolderCreate, \
    FolderBase, KnowledgeQueueCreate, RecordCreate, ThemeCreate  # Import schemas
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES  # Configuration
from ..database import get_db  # Import function to get DB session

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Setup OAuth2 scheme


# ===========================
# User Operations
# ===========================

# Create a new user
async def create_user(user: UserCreate, db: AsyncSession):
    new_user = User(**user.dict())  # Create a new user
    new_user.password = get_password_hash(new_user.password)  # Hash the password
    try:
        db.add(new_user)  # Add user to session
        await db.commit()  # Save changes
        await db.refresh(new_user)  # Refresh user data
    except IntegrityError:  # In case of unique constraint violation
        await db.rollback()  # Rollback transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this login already exists."
        )
    return {"status": 201, "data": new_user}  # Return created user

# Verify password
async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# Get user from DB by username
async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.login == username))  # Execute query
    return result.scalars().first()  # Return first found user

# Authenticate user
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)  # Get user
    if not user:
        return False  # If user not found
    if not await verify_password(password, user.password):  # Verify password
        return False
    return user  # Return user on successful authentication


# ===========================
# Tokenization
# ===========================

# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # Copy data for token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Set expiration time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default
    to_encode.update({"exp": expire})  # Update data with expiration time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode token
    return encoded_jwt

# Get current user
async def get_current_user(
        access_token: str = Cookie(None),  # Extract token from cookies
        db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception  # If token is missing
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode token
        username: str = payload.get("sub")  # Get username from payload
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)  # Create TokenData object
    except JWTError:
        raise credentials_exception  # If JWT error occurs

    user = await get_user(db=db, username=token_data.username)  # Get user by username
    if user is None:
        raise credentials_exception  # If user not found

    return user  # Return current user


# ===========================
# Folder Operations
# ===========================

# Add a folder
async def add_folder(folder_data: FolderBase, user_id: int, db: AsyncSession) -> Folder:
    new_folder = Folder(**folder_data.dict(), user_id=user_id)
    new_folder.last_open_date_time = datetime.utcnow()  # Set current creation time

    try:
        db.add(new_folder)  # Add new folder to session
        await db.commit()  # Save changes
        await db.refresh(new_folder)  # Refresh data
    except Exception:
        await db.rollback()  # Rollback transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add folder."
        )

    return new_folder  # Return created folder

# Get user folders
async def get_user_folders(user_id: int, db: AsyncSession):
    result = await db.execute(select(Folder).where(Folder.user_id == user_id))  # Get folders
    folders = result.scalars().all()  # Return all found folders
    return folders


# ===========================
# Theme Services
# ===========================

# Add a theme
async def add_theme(theme_data: ThemeCreate, folder_id: int, db: AsyncSession) -> Theme:
    new_theme = Theme(**theme_data.dict(), folder_id=folder_id)
    new_theme.last_open_date_time = datetime.utcnow()  # Set current creation time

    try:
        db.add(new_theme)  # Add new theme to session
        await db.commit()  # Save changes
        await db.refresh(new_theme)  # Refresh data
    except Exception:
        await db.rollback()  # Rollback transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add theme."
        )

    return new_theme  # Return created theme

# Get themes by folder
async def get_themes_by_folder(folder_id: int, db: AsyncSession):
    result = await db.execute(select(Theme).where(Theme.folder_id == folder_id))  # Get themes
    return result.scalars().all()  # Return all found themes


# ===========================
# Record Services
# ===========================

# Add a record
async def add_record(record_data: RecordCreate, theme_id: int, db: AsyncSession) -> Record:
    new_record = Record(**record_data.dict(), theme_id=theme_id)
    new_record.last_open_date_time = datetime.utcnow()  # Set current creation time

    try:
        db.add(new_record)  # Add new record to session
        await db.commit()  # Save changes
        await db.refresh(new_record)  # Refresh data
    except Exception:
        await db.rollback()  # Rollback transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add record."
        )

    return new_record  # Return created record

# Get records by theme
async def get_records_by_theme(theme_id: int, db: AsyncSession):
    result = await db.execute(select(Record).where(Record.theme_id == theme_id))  # Get records
    return result.scalars().all()  # Return all found records


# ===========================
# KnowledgeQueue Services
# ===========================

# Add a knowledge queue entry
async def add_knowledge_queue(queue_data: KnowledgeQueueCreate, user_id: int, db: AsyncSession) -> KnowledgeQueue:
    new_queue = KnowledgeQueue(**queue_data.dict(), user_id=user_id)
    new_queue.create_date_time = datetime.utcnow()  # Set current creation time
    new_queue.next_alert_card = None  # Implement reminder time
    try:
        db.add(new_queue)  # Add new queue to session
        await db.commit()  # Save changes
        await db.refresh(new_queue)  # Refresh data
    except Exception:
        await db.rollback()  # Rollback transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add knowledge queue."
        )

    return new_queue  # Return created knowledge queue

# Get knowledge queues by user
async def get_knowledge_queues_by_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(KnowledgeQueue).where(KnowledgeQueue.user_id == user_id))  # Get queues
    return result.scalars().all()  # Return all found knowledge queues
