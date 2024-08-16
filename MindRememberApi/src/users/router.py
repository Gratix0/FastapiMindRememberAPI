from datetime import timedelta

from fastapi import APIRouter, Response
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from .dependencies import check_unique_login
from .models import User
from .schemas import Folder, Theme, ThemeBase, Record, RecordBase, \
    KnowledgeQueue, KnowledgeQueueBase
from .schemas import UserCreate, Token, UserInDB, FolderCreate
from .service import create_user, create_access_token, authenticate_user, get_current_user, add_folder, \
    get_user_folders, add_theme, get_themes_by_folder, add_record, get_records_by_theme, add_knowledge_queue, \
    get_knowledge_queues_by_user
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/reg", summary="Register a new user", description="Creates a new user account with the provided data.")
async def add_user(user: UserCreate, db: Session = Depends(get_db), _ = Depends(check_unique_login)):
    """
    Registers a new user.

    - **user**: Data for creating a new user account.
    - **db**: Database session, extracted from the dependency.
    - **_**: Dependency to check if the username is unique.

    **Returns**:
    - The created user object.
    """
    return await create_user(user, db)

@router.post("/login", response_model=Token, summary="Login", description="Logs in a user and returns an access token.")
async def login_for_access_token(user: UserInDB, response: Response, db=Depends(get_db)):
    """
    Authenticates a user and generates an access token.

    - **user**: User credentials (username and password hash).
    - **response**: The response object to set a cookie.
    - **db**: Database session.

    **Returns**:
    - `Token`: An object containing the access token and token type.

    **Raises**:
    - HTTPException: If the username or password is incorrect.
    """
    user = await authenticate_user(db=db, username=user.username, password=user.hashed_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )

    # Set token in cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True)  # Secure=True if using HTTPS

    return Token(access_token=access_token, token_type="bearer")

@router.post("/add_one_folder", response_model=Folder, summary="Add One Folder", description="Creates a new folder with the provided data.")
async def add_one_folder(
        folder_data: FolderCreate,
        current_user: UserInDB = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Creates a new folder for the current user.

    - **folder_data**: Data for creating the new folder.
    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `Folder`: The created folder with a unique identifier and data.
    """
    return await add_folder(folder_data, current_user.id, db)

@router.get("/folders", response_model=list[Folder], summary="Get User Folders", description="Returns a list of all folders belonging to the current user.")
async def read_user_folders(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Fetches the list of folders for the user.

    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `List[Folder]`: A list of folders belonging to the current user.
    """
    folders = await get_user_folders(current_user.id, db)
    return folders

# Endpoints for Theme
@router.post("/folders/{folder_id}/add_theme", response_model=Theme, summary="Add Theme", description="Creates a new theme within the specified folder.")
async def create_theme(
    folder_id: int,
    theme_data: ThemeBase,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new theme in the specified folder.

    - **theme_data**: Data for creating the new theme.
    - **folder_id**: Unique identifier of the folder in which the theme is created.
    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `Theme`: The created theme with a unique identifier and data.
    """
    return await add_theme(theme_data, folder_id, db)

@router.get("/folders/{folder_id}/themes", response_model=list[Theme], summary="Get Themes", description="Returns a list of all themes in the specified folder.")
async def read_themes(folder_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetches the list of themes within the specified folder.

    - **folder_id**: Unique identifier of the folder for which themes are retrieved.
    - **db**: Database session.

    **Returns**:
    - `List[Theme]`: A list of themes in the specified folder.
    """
    return await get_themes_by_folder(folder_id, db)

@router.post("/themes/{theme_id}/add_record", response_model=Record, summary="Add Record", description="Creates a new record within the specified theme.")
async def create_record(
    theme_id: int,
    record_data: RecordBase,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new record in the specified theme.

    - **record_data**: Data for creating the new record.
    - **theme_id**: Unique identifier of the theme in which the record is created.
    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `Record`: The created record with a unique identifier and data.
    """
    return await add_record(record_data, theme_id, db)

@router.get("/themes/{theme_id}/records", response_model=list[Record], summary="Get Records", description="Returns a list of all records within the specified theme.")
async def read_records(theme_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetches the list of records in the specified theme.

    - **theme_id**: Unique identifier of the theme for which records are retrieved.
    - **db**: Database session.

    **Returns**:
    - `List[Record]`: A list of records in the specified theme.
    """
    return await get_records_by_theme(theme_id, db)

@router.post("/knowledge_queue", response_model=KnowledgeQueue, summary="Add Knowledge Queue Item", description="Creates a new knowledge queue for the current user.")
async def create_knowledge_queue(
    queue_data: KnowledgeQueueBase,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new knowledge queue for the user.

    - **queue_data**: Data for creating the new knowledge queue.
    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `KnowledgeQueue`: The created knowledge queue with a unique identifier and data.
    """
    return await add_knowledge_queue(queue_data, current_user.id, db)

@router.get("/knowledge_queue", response_model=list[KnowledgeQueue], summary="Get Knowledge Queue", description="Returns a list of all knowledge queues belonging to the current user.")
async def read_knowledge_queue(current_user: UserInDB = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Fetches the list of knowledge queues for the current user.

    - **current_user**: The current user extracted from the dependency.
    - **db**: Database session.

    **Returns**:
    - `List[KnowledgeQueue]`: A list of knowledge queues for the current user.
    """
    return await get_knowledge_queues_by_user(current_user.id, db)

