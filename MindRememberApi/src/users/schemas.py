from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ===========================
# User схемы
# ===========================

class UserCreate(BaseModel):
    login: str  # Логин пользователя
    password: str  # Пароль пользователя

class User(BaseModel):
    username: str  # Имя пользователя

class UserInDB(User):
    hashed_password: str  # Хэшированный пароль пользователя для хранения в БД

# ===========================
# Токены и аутентификация
# ===========================

class Token(BaseModel):
    access_token: str  # Поле для токена доступа
    token_type: str  # Тип токена (например, Bearer)

class TokenData(BaseModel):
    username: Optional[str] = None  # Имя пользователя из токена (может отсутствовать)

# ===========================
# Folder схемы
# ===========================

# Базовая схема для Folder с общими полями
class FolderBase(BaseModel):
    text_folder: str  # Название папки
    number_of_topics: Optional[int] = Field(default=0)  # Количество тем в папке
    last_open_date_time: Optional[datetime] = Field(default_factory=None)  # Время последнего открытия

# Схема для создания нового Folder
class FolderCreate(FolderBase):
    pass

# Схема для получения данных из Folder
class Folder(FolderBase):
    id: int  # Уникальный идентификатор папки
    user_id: Optional[int] = None  # Идентификатор пользователя, которому принадлежит папка

    class Config:
        orm_mode = True  # Позволяет использовать Pydantic с ORM моделями

# ===========================
# Theme схемы
# ===========================

# Базовая схема для Theme с общими полями
class ThemeBase(BaseModel):
    name_theme: str  # Название темы
    number_of_records: Optional[int] = Field(default=0)  # Количество записей в теме
    last_open_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow)  # Время последнего открытия

# Схема для создания нового Theme
class ThemeCreate(ThemeBase):
    pass

# Схема для получения данных из Theme
class Theme(ThemeBase):
    id: int  # Уникальный идентификатор темы
    folder_id: Optional[int] = None  # Идентификатор папки, к которой принадлежит тема

    class Config:
        orm_mode = True

# ===========================
# Record схемы
# ===========================

# Базовая схема для Record с общими полями
class RecordBase(BaseModel):
    name_record: str  # Название записи
    text_records: Optional[str] = None  # Содержимое записи
    count_text: Optional[int] = Field(default=0)  # Количество текста в записи
    last_open_date_time: Optional[datetime] = Field(default_factory=datetime.utcnow)  # Время последнего открытия

# Схема для создания новой записи
class RecordCreate(RecordBase):
    pass

# Схема для получения данных из Record
class Record(RecordBase):
    id: int  # Уникальный идентификатор записи
    theme_id: Optional[int] = None  # Идентификатор темы, к которой принадлежит запись

    class Config:
        orm_mode = True

# ===========================
# KnowledgeQueue схемы
# ===========================

# Базовая схема для KnowledgeQueue с общими полями
class KnowledgeQueueBase(BaseModel):
    content_knowledge_queue: str  # Содержимое очереди знаний
    completed_task_status: Optional[bool] = Field(default=False)  # Статус завершения задачи
    number_of_cycles: Optional[int] = Field(default=0)  # Количество циклов
    create_date_time: Optional[datetime] = Field(default_factory=None)  # Время создания
    next_alert_card: Optional[datetime] = Field(default_factory=None)  # Следующее время оповещения

# Схема для создания новой очереди знаний
class KnowledgeQueueCreate(KnowledgeQueueBase):
    pass

# Схема для получения данных из KnowledgeQueue
class KnowledgeQueue(KnowledgeQueueBase):
    id: int  # Уникальный идентификатор очереди знаний
    user_id: Optional[int] = None  # Идентификатор пользователя, которому принадлежит очередь

    class Config:
        orm_mode = True
