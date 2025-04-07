#from app.db.session import Base
#from app.models.user import User

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DB_URL = 'sqlite:///./fedor.db'

engine = create_engine(SQL_DB_URL, connect_args={'check_same_thread': False})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)  # чтобы вручную комитить изменения в бд

Base = declarative_base() # создаст базовый класс моделей
