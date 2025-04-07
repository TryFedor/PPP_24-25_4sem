from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends, APIRouter
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse

router = APIRouter()

Base.metadata.create_all(bind=engine)  # создаем базу данных


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.post('/users/', response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(
    get_db)) -> DbUser:  # когда мы передаем данные post запросом, так же сраху передамем данные о пользователе
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post('/posts/', response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> Post:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.get('/posts/', response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()
