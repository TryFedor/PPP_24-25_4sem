from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post('/sign-up', response_model=UserResponce)