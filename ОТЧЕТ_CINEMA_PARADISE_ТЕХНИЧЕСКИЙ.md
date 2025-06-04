# ОТЧЕТ
## по лабораторной работе
### "Разработка REST API для системы управления кинотеатром"

---

**Выполнил:** [Ваше имя]  
**Группа:** [Ваша группа]  
**Дисциплина:** Методы объектно-ориентированного программирования  
**Дата:** Июнь 2025

---

## Ход Работы

Темой разрабатываемого сервиса стал **«Кинотеатр Cinema Paradise»**.

### Структура проекта

```
cinema_api/
├── app/
│   ├── __init__.py                  # Инициализация приложения
│   ├── main.py                      # Главный файл FastAPI приложения
│   ├── database.py                  # Конфигурация базы данных
│   ├── models.py                    # SQLAlchemy модели и связи
│   │   ├── User.py                  # Модель пользователя
│   │   ├── Movie.py                 # Модель фильма
│   │   ├── Cinema.py                # Модель кинотеатра
│   │   ├── Hall.py                  # Модель зала
│   │   ├── Session.py               # Модель сеанса
│   │   ├── Ticket.py                # Модель билета
│   │   └── Review.py                # Модель отзыва
│   ├── schemas/                     # Pydantic схемы валидации
│   │   ├── user_schemas.py          # Схемы пользователей
│   │   ├── movie_schemas.py         # Схемы фильмов
│   │   ├── session_schemas.py       # Схемы сеансов
│   │   ├── ticket_schemas.py        # Схемы билетов
│   │   └── auth_schemas.py          # Схемы авторизации
│   ├── routers/                     # API маршруты
│   │   ├── auth.py                  # Маршруты авторизации
│   │   ├── movies.py                # Маршруты фильмов
│   │   ├── sessions.py              # Маршруты сеансов
│   │   ├── tickets.py               # Маршруты билетов
│   │   ├── reviews.py               # Маршруты отзывов
│   │   └── admin.py                 # Административные маршруты
│   ├── middleware/
│   │   ├── auth.py                  # Middleware аутентификации
│   │   ├── cors.py                  # CORS настройки
│   │   └── validation.py            # Валидация данных
│   ├── utils/
│   │   ├── jwt_utils.py             # Утилиты для работы с JWT
│   │   ├── password.py              # Хеширование паролей
│   │   └── validators.py            # Дополнительные валидаторы
│   └── config/
│       ├── settings.py              # Настройки приложения
│       └── database.py              # Конфигурация БД
├── frontend/                        # Веб-интерфейс
│   ├── index.html                   # Главная страница
│   ├── css/                         # Стили
│   ├── js/                          # JavaScript
│   └── assets/                      # Статические файлы
├── mobile_app/                      # PWA мобильное приложение
│   ├── index.html                   # Точка входа PWA
│   ├── manifest.json                # PWA манифест
│   └── service-worker.js            # Service Worker
├── tests/                           # Автотесты
│   ├── test_auth.py                 # Тесты авторизации
│   ├── test_movies.py               # Тесты фильмов
│   ├── test_tickets.py              # Тесты билетов
│   └── test_endpoints.py            # Интеграционные тесты
├── docs/
│   └── openapi.yaml                 # OpenAPI спецификация
├── requirements.txt                 # Python зависимости
├── .env                            # Переменные окружения
├── README.md                        # Документация проекта
└── run.py                          # Точка входа приложения
```

### 2. Основные компоненты:

#### Конфигурация (app/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Настройки базы данных
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cinema.db")

# Создание движка БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание таблиц
def create_tables():
    Base.metadata.create_all(bind=engine)
```

#### Модели (app/models.py)

```python
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, Enum, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

class UserRole(enum.Enum):
    """Роли пользователей"""
    ADMIN = "admin"
    MANAGER = "manager"
    CUSTOMER = "customer"

class User(Base):
    """Модель пользователя/клиента"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    loyalty_points = Column(Integer, default=0)
    total_spent = Column(DECIMAL(10, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        from .utils.password import verify_password
        return verify_password(password, self.hashed_password)

class Movie(Base):
    """Модель фильма"""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=False)
    director = Column(String(255))
    rating = Column(Float, default=0.0)
    poster_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    sessions = relationship("Session", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")

class Session(Base):
    """Модель сеанса"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    base_price = Column(DECIMAL(8, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    movie = relationship("Movie", back_populates="sessions")
    hall = relationship("Hall", back_populates="sessions")
    tickets = relationship("Ticket", back_populates="session", cascade="all, delete-orphan")

class Ticket(Base):
    """Модель билета"""
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_row = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    booking_reference = Column(String(20), unique=True, nullable=False)
    is_paid = Column(Boolean, default=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    session = relationship("Session", back_populates="tickets")
    user = relationship("User", back_populates="tickets")
```

#### Маршруты (app/main.py)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db, create_tables
from .utils.jwt_utils import create_access_token, verify_token
from .utils.password import get_password_hash, verify_password
import os

# Создание приложения FastAPI
app = FastAPI(
    title="Cinema Paradise API",
    description="API для системы управления кинотеатром",
    version="2.0.0"
)

# OAuth2 схема для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Создание таблиц при запуске
create_tables()

# Регистрация пользователя
@app.post("/auth/register", response_model=schemas.UserResponse)
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    try:
        # Проверка существования пользователя
        existing_user = db.query(models.User).filter(
            (models.User.email == user_data.email) | 
            (models.User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email или username уже существует"
            )

        # Создание нового пользователя
        hashed_password = get_password_hash(user_data.password)
        user = models.User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания пользователя: {str(e)}"
        )

# Вход в систему
@app.post("/auth/login", response_model=schemas.Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        # Поиск пользователя
        user = db.query(models.User).filter(
            models.User.username == form_data.username
        ).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверные учетные данные"
            )
        
        # Создание JWT токена
        access_token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка авторизации: {str(e)}"
        )

# Получение текущего пользователя
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        username = verify_token(token)
        user = db.query(models.User).filter(
            models.User.username == username
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )

# Получение списка фильмов
@app.get("/movies", response_model=list[schemas.MovieResponse])
async def get_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        movies = db.query(models.Movie).filter(
            models.Movie.is_active == True
        ).offset(skip).limit(limit).all()
        
        return movies
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения фильмов: {str(e)}"
        )

# Бронирование билета
@app.post("/tickets", response_model=schemas.TicketResponse)
async def create_ticket(
    ticket_data: schemas.TicketCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Проверка доступности сеанса
        session = db.query(models.Session).filter(
            models.Session.id == ticket_data.session_id,
            models.Session.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сеанс не найден"
            )
        
        # Проверка доступности места
        existing_ticket = db.query(models.Ticket).filter(
            models.Ticket.session_id == ticket_data.session_id,
            models.Ticket.seat_row == ticket_data.seat_row,
            models.Ticket.seat_number == ticket_data.seat_number
        ).first()
        
        if existing_ticket:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Место уже занято"
            )
        
        # Создание билета
        import secrets
        booking_reference = secrets.token_hex(8).upper()
        
        ticket = models.Ticket(
            session_id=ticket_data.session_id,
            user_id=current_user.id,
            seat_row=ticket_data.seat_row,
            seat_number=ticket_data.seat_number,
            price=session.base_price,
            booking_reference=booking_reference
        )
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        
        return ticket
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка бронирования: {str(e)}"
        )
```

#### Middleware аутентификации (app/utils/jwt_utils.py)

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import os

# Настройки JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание JWT токена"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str):
    """Проверка JWT токена"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен"
            )
        
        return username
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
```

#### Валидация (app/schemas/user_schemas.py)

```python
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from ..models import UserRole

class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username должен быть не менее 3 символов')
        if not v.isalnum():
            raise ValueError('Username может содержать только буквы и цифры')
        return v

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        return v

class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    role: UserRole
    is_active: bool
    loyalty_points: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """Схема JWT токена"""
    access_token: str
    token_type: str
    user: UserResponse
```

### 3. Основные функции:

#### - Аутентификация и авторизация:
- **JWT-based аутентификация**
- **Роли пользователей (customer, manager, admin)**
- **Middleware для проверки прав доступа**
- **Защищенные маршруты**

#### - Управление данными:
- **CRUD операции для всех сущностей**
- **Валидация входных данных через Pydantic**
- **Обработка ошибок**
- **Пагинация и фильтрация**

#### - Бизнес-логика:
- **Бронирование билетов**
- **Управление сеансами**
- **Система отзывов**
- **Программа лояльности**

### 4. Безопасность:

- **Хеширование паролей (bcrypt)**
- **JWT токены с истечением**
- **Валидация данных (Pydantic)**
- **Защита от SQL-инъекций (SQLAlchemy ORM)**
- **CORS настройки**
- **Rate limiting**

### 5. Обработка ошибок:

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP ошибок"""
    logging.error(f"HTTP Error: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Общий обработчик ошибок"""
    logging.error(f"Internal Error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Внутренняя ошибка сервера",
            "detail": str(exc) if os.getenv("DEBUG") == "True" else None
        }
    )
```

### 6. Запуск сервера:

```python
# run.py
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### 7. Тестирование

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    """Тест регистрации пользователя"""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login_user():
    """Тест входа пользователя"""
    # Сначала создаем пользователя
    client.post("/auth/register", json={
        "username": "logintest",
        "email": "login@example.com", 
        "password": "password123",
        "first_name": "Login",
        "last_name": "Test"
    })
    
    # Затем пытаемся войти
    response = client.post("/auth/login", data={
        "username": "logintest",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_route():
    """Тест защищенного маршрута"""
    # Получаем токен
    login_response = client.post("/auth/login", data={
        "username": "logintest",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Используем токен для доступа к защищенному маршруту
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "logintest"
```

---

**Использованные технологии:**
- **Backend:** Python 3.9+, FastAPI, SQLAlchemy, Pydantic
- **База данных:** SQLite с возможностью PostgreSQL
- **Аутентификация:** JWT токены, bcrypt
- **Тестирование:** pytest, httpx
- **Документация:** OpenAPI/Swagger автогенерация
- **Развертывание:** Uvicorn ASGI сервер

**Архитектурные особенности:**
- **Модульная структура** с разделением на слои
- **Dependency Injection** через FastAPI
- **Асинхронная обработка** запросов
- **Автоматическая валидация** данных
- **Миграции БД** через Alembic
- **Контейнеризация** Docker готова 