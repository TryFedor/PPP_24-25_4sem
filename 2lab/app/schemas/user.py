from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str  # Пароль для регистрации

class UserResponse(BaseModel):
    id: int
    email: str
    token: str  # JWT-токен в ответе

    class Config:
        orm_mode = True


class UserMeResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
