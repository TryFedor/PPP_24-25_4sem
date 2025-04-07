from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.cruds.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import create_access_token
from app.cruds.user import get_user_by_email, verify_password, get_user_by_id

from fastapi.security import OAuth2PasswordBearer
from app.services.auth import decode_token  # функция декодирования токена


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up/", response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка наличия email
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Создание пользователя
    new_user = create_user(db, user)
    # Генерация токена
    access_token = create_access_token(
        data={"sub": new_user.email, "user_id": new_user.id}
    )
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        token=access_token
    )


@router.post("/login/", response_model=UserResponse)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        token=access_token
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Декодируем токен
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    # Ищем пользователя в БД
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/me/", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

