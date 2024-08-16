import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, MetaData
# from sqlalchemy import Table
# from sqlalchemy.orm import relationship, sessionmaker
#
# metadata = MetaData()

#Императивный подход
#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

# # Определение таблицы Users
# users = Table('users', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('login', String, nullable=False, unique=True),
#     Column('password', String, nullable=False)
# )
#
# # Определение таблицы Folders
# folders = Table('folders', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('text_folder', String, nullable=False),
#     Column('number_of_topics', Integer, default=0),
#     Column('last_open_date_time', DateTime, default=datetime.datetime.utcnow),
#     Column('user_id', Integer, ForeignKey('users.id'))
# )
#
# # Определение таблицы Themes
# themes = Table('themes', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name_theme', String, nullable=False),
#     Column('last_open_date_time', DateTime, default=datetime.datetime.utcnow),
#     Column('number_of_records', Integer, default=0),
#     Column('folder_id', Integer, ForeignKey('folders.id'))
# )
#
# # Определение таблицы Records
# records = Table('records', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name_record', String, nullable=False),
#     Column('text_records', String),
#     Column('last_open_date_time', DateTime, default=datetime.datetime.utcnow),
#     Column('count_text', Integer, default=0),
#     Column('theme_id', Integer, ForeignKey('themes.id'))
# )
#
# # Определение таблицы KnowledgeQueues
# knowledge_queues = Table('knowledge_queues', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('content_knowledge_queue', String, nullable=False),
#     Column('completed_task_status', Boolean, default=False),
#     Column('number_of_cycles', Integer, default=0),
#     Column('create_date_time', DateTime, default=datetime.datetime.utcnow),
#     Column('next_alert_card', DateTime, default=datetime.datetime.utcnow),
#     Column('user_id', Integer, ForeignKey('users.id'))
# )
#-----------------------------------------------------------



#Декларативный подход
#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Folder(Base):
    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True)
    text_folder = Column(String, nullable=False)
    number_of_topics = Column(Integer, default=0)
    last_open_date_time = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey('users.id'))

class Theme(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    name_theme = Column(String, nullable=False)
    last_open_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    number_of_records = Column(Integer, default=0)
    folder_id = Column(Integer, ForeignKey('folders.id'))

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    name_record = Column(String, nullable=False)
    text_records = Column(String)
    last_open_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    count_text = Column(Integer, default=0)
    theme_id = Column(Integer, ForeignKey('themes.id'))

class KnowledgeQueue(Base):
    __tablename__ = 'knowledge_queues'

    id = Column(Integer, primary_key=True)
    content_knowledge_queue = Column(String, nullable=False)
    completed_task_status = Column(Boolean, default=False)
    number_of_cycles = Column(Integer, default=0)
    create_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    next_alert_card = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
#---------------------------------------