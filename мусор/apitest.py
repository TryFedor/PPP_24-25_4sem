from datetime import datetime
from pydantic import BaseModel, PositiveInt
from typing import List, Literal
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess
from fastapi import FastAPI, Depends
import asyncio
from uvicorn import Server, Config

engine = create_engine('sqlite:///example.db')

# Создание базового класса для моделей
Base = declarative_base()

# Определение модели для таблицы
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Создание таблицы в базе данных
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Добавление нового пользователя
new_user = User(name='AKEZ', age=30)
session.add(new_user)
session.commit()

# Получение всех пользователей
users = session.query(User).all()
for user in users:
    print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')


# Вставка нового пользователя
new_user = User(name='Jane Doe', age=25)
session.add(new_user)
session.commit()

# Обновление существующего пользователя
user_to_update = session.query(User).filter_by(name='John Doe').first()
user_to_update.age = 31
session.commit()

# Удаление пользователя
user_to_delete = session.query(User).filter_by(name='Jane Doe').first()
session.delete(user_to_delete)
session.commit()


# Вставка нового пользователя
new_user = User(name='Jane Doee', age=311)
session.add(new_user)
session.commit()

# Получение пользователей с возрастом больше 30
users_over_30 = session.query(User).filter(User.age > 30).all()
for user in users_over_30:
    print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')

# Получение пользователей, отсортированных по имени
sorted_users = session.query(User).order_by(User.name).all()
for user in sorted_users:
    print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users/")
def create_user(name: str, age: int, db: Session = Depends(get_db)):
    db_user = User(name=name, age=age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, age: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = name
    db_user.age = age
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted"}

##############


config = Config(app=app, host="127.0.0.1", port=8000)

# Создайте сервер
server = Server(config)
##
#await server.serve()

command = ["uvicorn", "main:app", "--reload"]
# command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
