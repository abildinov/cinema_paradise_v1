from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
import secrets
import string

from ..database import get_db
from ..models import User as UserModel, UserRole
from ..auth import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from ..schemas import UserCreate, UserResponse

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

def generate_booking_reference() -> str:
    """Генерация уникального номера бронирования"""
    length = 8
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@router.post("/register", response_model=UserResponse, summary="Регистрация пользователя")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя в системе.
    
    - **username**: Уникальное имя пользователя
    - **email**: Email адрес (уникальный)
    - **password**: Пароль пользователя
    - **first_name**: Имя
    - **last_name**: Фамилия
    - **phone**: Номер телефона (опционально)
    """
    # Проверка на существующего пользователя
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user_data.username) | 
        (UserModel.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username или email уже существует"
        )
    
    # Создание нового пользователя
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=UserRole.CUSTOMER
    )
    
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username или email уже существует (ошибка базы данных)"
        )
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token, summary="Вход в систему")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя и получение JWT токена.
    
    - **username**: Имя пользователя
    - **password**: Пароль
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Обновляем время последнего входа
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse, summary="Профиль пользователя")
async def get_current_user_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Получение профиля текущего авторизованного пользователя.
    """
    return current_user

@router.get("/users", summary="Список пользователей (только для админов)")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение списка пользователей (доступно только администраторам).
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users 