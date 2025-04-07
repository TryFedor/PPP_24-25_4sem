from datetime import datetime, timedelta
from fastapi import HTTPException

import jwt  # Теперь импортируем из PyJWT
from app.core.config import settings
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from app.core.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
