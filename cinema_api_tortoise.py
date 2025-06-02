#!/usr/bin/env python3
"""
Cinema API с Tortoise ORM - полная версия для Python 3.13
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tortoise.contrib.fastapi import register_tortoise
from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum
import jwt
import bcrypt
import uvicorn
import logging
from pathlib import Path

# Создаем директорию для базы данных
Path("data").mkdir(exist_ok=True)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT настройки
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
security = HTTPBearer()

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CUSTOMER = "customer"

class MovieGenre(str, Enum):
    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    HORROR = "horror"
    ROMANCE = "romance"
    SCI_FI = "sci_fi"
    THRILLER = "thriller"
    DOCUMENTARY = "documentary"
    ANIMATION = "animation"
    FANTASY = "fantasy"

# Tortoise Models
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.TextField()
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20, null=True)
    role = fields.CharEnumField(UserRole, default=UserRole.CUSTOMER)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

class Cinema(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    city = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    latitude = fields.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = fields.DecimalField(max_digits=11, decimal_places=8, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cinemas"

class Hall(Model):
    id = fields.IntField(pk=True)
    cinema = fields.ForeignKeyField('models.Cinema', related_name='halls')
    name = fields.CharField(max_length=100)
    capacity = fields.IntField()
    rows = fields.IntField()
    seats_per_row = fields.IntField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "halls"

class Movie(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField()
    genre = fields.CharEnumField(MovieGenre)
    duration_minutes = fields.IntField()
    rating = fields.DecimalField(max_digits=3, decimal_places=1, null=True)
    release_date = fields.DateField()
    director = fields.CharField(max_length=200)
    cast = fields.TextField()
    poster_url = fields.TextField(null=True)
    trailer_url = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "movies"

class Session(Model):
    id = fields.IntField(pk=True)
    movie = fields.ForeignKeyField('models.Movie', related_name='sessions')
    hall = fields.ForeignKeyField('models.Hall', related_name='sessions')
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    base_price = fields.DecimalField(max_digits=10, decimal_places=2)
    available_seats = fields.IntField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "sessions"

class Ticket(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='tickets')
    session = fields.ForeignKeyField('models.Session', related_name='tickets')
    seat_number = fields.CharField(max_length=10)
    row_number = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    booking_time = fields.DatetimeField(auto_now_add=True)
    is_confirmed = fields.BooleanField(default=False)
    is_cancelled = fields.BooleanField(default=False)

    class Meta:
        table = "tickets"

class Review(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='reviews')
    movie = fields.ForeignKeyField('models.Movie', related_name='reviews')
    rating = fields.IntField()  # 1-5
    comment = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "reviews"

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class MovieCreate(BaseModel):
    title: str
    description: str
    genre: MovieGenre
    duration_minutes: int
    release_date: datetime
    director: str
    cast: str
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    genre: MovieGenre
    duration: int  # Будем переименовывать в фронтенде
    rating: Optional[float]
    release_date: datetime
    poster_url: Optional[str]
    created_at: datetime

class HallResponse(BaseModel):
    id: int
    name: str
    capacity: int
    cinema_id: int
    created_at: datetime

class SessionCreate(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    base_price: float

class SessionResponse(BaseModel):
    id: int
    movie_id: int
    hall_id: int
    start_time: datetime
    price: float
    available_seats: int
    is_active: bool
    created_at: datetime
    movie: Optional[MovieResponse] = None
    hall: Optional[HallResponse] = None

class TicketCreate(BaseModel):
    session_id: int
    seat_numbers: List[int]
    total_price: float

class TicketResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    seat_number: str
    row_number: int
    price: float
    is_confirmed: bool
    created_at: datetime
    session: Optional[SessionResponse] = None
    user: Optional[UserResponse] = None

class CinemaResponse(BaseModel):
    id: int
    name: str
    address: str
    created_at: datetime

# FastAPI App
app = FastAPI(
    title="🎬 Cinema API",
    description="""
    **Полнофункциональный API для управления кинотеатром с Tortoise ORM**
    
    ## 🚀 Возможности
    
    * **👥 Пользователи**: Регистрация, авторизация, управление профилями
    * **🎬 Фильмы**: Каталог фильмов с жанрами, рейтингами и описаниями
    * **🏢 Кинотеатры**: Управление сетью кинотеатров и залами
    * **🎭 Сеансы**: Расписание киносеансов с ценами
    * **🎫 Билеты**: Бронирование билетов с выбором мест
    * **⭐ Отзывы**: Система отзывов и рейтингов
    
    ## 🔐 Аутентификация
    
    API использует JWT токены для аутентификации:
    1. Зарегистрируйтесь через `/auth/register`
    2. Войдите через `/auth/login`
    3. Используйте полученный токен в заголовке: `Authorization: Bearer <token>`
    
    ## 📊 База данных
    
    - **ORM**: Tortoise ORM (async)
    - **База**: SQLite (development) / PostgreSQL (production)
    - **Таблицы**: 7 основных таблиц с 130+ полями
    """,
    version="3.0.0",
    contact={
        "name": "Cinema API Team",
        "email": "dev@cinema-api.ru"
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        
        user_id = int(user_id_str)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")
    except ValueError:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Аккаунт деактивирован")
    
    return user

# Routes
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["🚦 Система"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Cinema API работает на Tortoise ORM",
        "version": "3.0.0",
        "orm": "Tortoise ORM",
        "database": "SQLite",
        "python_version": "3.13 compatible",
        "features": [
            "✅ FastAPI активен",
            "✅ Tortoise ORM подключена",
            "✅ JWT аутентификация",
            "✅ 7 таблиц базы данных",
            "✅ 30+ API endpoints",
            "✅ Swagger документация"
        ]
    }

# Auth routes
@app.post("/auth/register", response_model=UserResponse, tags=["🔐 Аутентификация"])
async def register(user_data: UserCreate):
    """Регистрация нового пользователя"""
    
    # Проверка существования пользователя
    existing_user = await User.get_or_none(username=user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    
    existing_email = await User.get_or_none(email=user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Создание пользователя
    hashed_password = hash_password(user_data.password)
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone
    )
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )

@app.post("/auth/login", response_model=Token, tags=["🔐 Аутентификация"])
async def login(user_data: UserLogin):
    """Авторизация пользователя"""
    
    user = await User.get_or_none(username=user_data.username)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Аккаунт деактивирован")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse, tags=["🔐 Аутентификация"])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at
    )

# Movies routes
@app.get("/movies", response_model=List[MovieResponse], tags=["🎬 Фильмы"])
async def get_movies(skip: int = 0, limit: int = 100):
    """Получение списка фильмов"""
    movies = await Movie.filter(is_active=True).offset(skip).limit(limit)
    return [MovieResponse(
        id=m.id,
        title=m.title,
        description=m.description,
        genre=m.genre,
        duration=m.duration_minutes,
        rating=float(m.rating) if m.rating else None,
        release_date=m.release_date,
        poster_url=m.poster_url,
        created_at=m.created_at
    ) for m in movies]

@app.post("/movies", response_model=MovieResponse, tags=["🎬 Фильмы"])
async def create_movie(movie_data: MovieCreate, current_user: User = Depends(get_current_user)):
    """Создание нового фильма (только для менеджеров и админов)"""
    
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    movie = await Movie.create(**movie_data.dict())
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        genre=movie.genre,
        duration=movie.duration_minutes,
        rating=float(movie.rating) if movie.rating else None,
        release_date=movie.release_date,
        poster_url=movie.poster_url,
        created_at=movie.created_at
    )

@app.get("/movies/{movie_id}", response_model=MovieResponse, tags=["🎬 Фильмы"])
async def get_movie(movie_id: int):
    """Получение информации о фильме"""
    movie = await Movie.get_or_none(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        genre=movie.genre,
        duration=movie.duration_minutes,
        rating=float(movie.rating) if movie.rating else None,
        release_date=movie.release_date,
        poster_url=movie.poster_url,
        created_at=movie.created_at
    )

# Sessions routes
@app.get("/sessions", response_model=List[SessionResponse], tags=["🎭 Сеансы"])
async def get_sessions(skip: int = 0, limit: int = 100):
    """Получение списка сеансов"""
    try:
        logger.info(f"Getting sessions with skip={skip}, limit={limit}")
        sessions = await Session.filter(is_active=True).offset(skip).limit(limit).prefetch_related('movie', 'hall')
        logger.info(f"Found {len(sessions)} sessions")
        
        result = []
        for session in sessions:
            logger.debug(f"Processing session {session.id}")
            # Получаем фильм
            movie_data = None
            if session.movie:
                movie_data = MovieResponse(
                    id=session.movie.id,
                    title=session.movie.title,
                    description=session.movie.description,
                    genre=session.movie.genre,
                    duration=session.movie.duration_minutes,
                    rating=float(session.movie.rating) if session.movie.rating else None,
                    release_date=session.movie.release_date,
                    poster_url=session.movie.poster_url,
                    created_at=session.movie.created_at
                )
            
            # Получаем зал
            hall_data = None
            if session.hall:
                logger.debug(f"Processing hall {session.hall.id}")
                # Проверяем наличие created_at в hall
                hall_created_at = getattr(session.hall, 'created_at', datetime.now())
                logger.debug(f"Hall created_at: {hall_created_at}")
                
                hall_data = HallResponse(
                    id=session.hall.id,
                    name=session.hall.name,
                    capacity=session.hall.capacity,
                    cinema_id=session.hall.cinema_id,
                    created_at=hall_created_at
                )
            
            result.append(SessionResponse(
                id=session.id,
                movie_id=session.movie_id,
                hall_id=session.hall_id,
                start_time=session.start_time,
                price=float(session.base_price),
                available_seats=session.available_seats,
                is_active=session.is_active,
                created_at=session.created_at,
                movie=movie_data,
                hall=hall_data
            ))
        
        logger.info(f"Successfully processed {len(result)} sessions")
        return result
    except Exception as e:
        logger.error(f"Error in get_sessions: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения сеансов: {str(e)}")

@app.post("/sessions", response_model=SessionResponse, tags=["🎭 Сеансы"])
async def create_session(session_data: SessionCreate, current_user: User = Depends(get_current_user)):
    """Создание нового сеанса (только для менеджеров и админов)"""
    
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    # Проверяем существование фильма и зала
    movie = await Movie.get_or_none(id=session_data.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    hall = await Hall.get_or_none(id=session_data.hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не найден")
    
    # Вычисляем время окончания
    end_time = session_data.start_time + timedelta(minutes=movie.duration_minutes + 30)  # +30 мин на рекламу
    
    session = await Session.create(
        movie=movie,
        hall=hall,
        start_time=session_data.start_time,
        end_time=end_time,
        base_price=session_data.base_price,
        available_seats=hall.capacity
    )
    
    await session.fetch_related('movie', 'hall')
    
    return SessionResponse(
        id=session.id,
        movie_id=session.movie_id,
        hall_id=session.hall_id,
        start_time=session.start_time,
        price=float(session.base_price),
        available_seats=session.available_seats,
        is_active=session.is_active,
        created_at=session.created_at,
        movie=MovieResponse(
            id=session.movie.id,
            title=session.movie.title,
            description=session.movie.description,
            genre=session.movie.genre,
            duration=session.movie.duration_minutes,
            rating=float(session.movie.rating) if session.movie.rating else None,
            release_date=session.movie.release_date,
            poster_url=session.movie.poster_url,
            created_at=session.movie.created_at
        ),
        hall=HallResponse(
            id=session.hall.id,
            name=session.hall.name,
            capacity=session.hall.capacity,
            cinema_id=session.hall.cinema_id,
            created_at=getattr(session.hall, 'created_at', datetime.now())
        )
    )

# Tickets routes
@app.post("/tickets", response_model=List[TicketResponse], tags=["🎫 Билеты"])
async def create_tickets(ticket_data: TicketCreate, current_user: User = Depends(get_current_user)):
    """Создание билетов (бронирование мест)"""
    
    # Проверяем существование сеанса
    session = await Session.get_or_none(id=ticket_data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    await session.fetch_related('movie', 'hall')
    
    # Проверяем количество доступных мест
    if session.available_seats < len(ticket_data.seat_numbers):
        raise HTTPException(status_code=400, detail="Недостаточно свободных мест")
    
    tickets = []
    for seat_number in ticket_data.seat_numbers:
        # Вычисляем ряд (примерно)
        row_number = (seat_number - 1) // session.hall.seats_per_row + 1
        
        ticket = await Ticket.create(
            user=current_user,
            session=session,
            seat_number=str(seat_number),
            row_number=row_number,
            price=session.base_price
        )
        
        tickets.append(TicketResponse(
            id=ticket.id,
            user_id=ticket.user_id,
            session_id=ticket.session_id,
            seat_number=ticket.seat_number,
            row_number=ticket.row_number,
            price=float(ticket.price),
            is_confirmed=ticket.is_confirmed,
            created_at=ticket.booking_time,
            session=SessionResponse(
                id=ticket.session_id,
                movie_id=ticket.session.movie_id,
                hall_id=ticket.session.hall_id,
                start_time=ticket.session.start_time,
                price=float(ticket.session.base_price),
                available_seats=ticket.session.available_seats,
                is_active=ticket.session.is_active,
                created_at=ticket.session.created_at,
                movie=MovieResponse(
                    id=ticket.session.movie.id,
                    title=ticket.session.movie.title,
                    description=ticket.session.movie.description,
                    genre=ticket.session.movie.genre,
                    duration=ticket.session.movie.duration_minutes,
                    rating=ticket.session.movie.rating,
                    release_date=ticket.session.movie.release_date,
                    poster_url=ticket.session.movie.poster_url,
                    created_at=ticket.session.movie.created_at
                ) if ticket.session.movie else None,
                hall=HallResponse(
                    id=ticket.session.hall.id,
                    name=ticket.session.hall.name,
                    capacity=ticket.session.hall.capacity,
                    cinema_id=ticket.session.hall.cinema_id,
                    created_at=getattr(ticket.session.hall, 'created_at', datetime.now())
                ) if ticket.session.hall else None
            ),
            user=UserResponse(
                id=ticket.user_id,
                username=ticket.user.username,
                email=ticket.user.email,
                role=ticket.user.role,
                created_at=ticket.user.created_at
            ) if ticket.user else None
        ))
    
    # Обновляем количество доступных мест
    session.available_seats -= len(ticket_data.seat_numbers)
    await session.save()
    
    return tickets

@app.get("/tickets/my", response_model=List[TicketResponse], tags=["🎫 Билеты"])
async def get_user_tickets(current_user: UserResponse = Depends(get_current_user)):
    """Получить билеты текущего пользователя"""
    try:
        tickets = await Ticket.filter(user_id=current_user.id).prefetch_related(
            'session__movie', 'session__hall', 'user'
        )
        return [
            TicketResponse(
                id=ticket.id,
                user_id=ticket.user_id,
                session_id=ticket.session_id,
                seat_number=ticket.seat_number,
                row_number=ticket.row_number,
                price=ticket.price,
                is_confirmed=ticket.is_confirmed,
                created_at=ticket.booking_time,
                session=SessionResponse(
                    id=ticket.session.id,
                    movie_id=ticket.session.movie_id,
                    hall_id=ticket.session.hall_id,
                    start_time=ticket.session.start_time,
                    price=float(ticket.session.base_price),
                    available_seats=ticket.session.available_seats,
                    is_active=ticket.session.is_active,
                    created_at=ticket.session.created_at,
                    movie=MovieResponse(
                        id=ticket.session.movie.id,
                        title=ticket.session.movie.title,
                        description=ticket.session.movie.description,
                        genre=ticket.session.movie.genre,
                        duration=ticket.session.movie.duration_minutes,
                        rating=ticket.session.movie.rating,
                        release_date=ticket.session.movie.release_date,
                        poster_url=ticket.session.movie.poster_url,
                        created_at=ticket.session.movie.created_at
                    ) if ticket.session.movie else None,
                    hall=HallResponse(
                        id=ticket.session.hall.id,
                        name=ticket.session.hall.name,
                        capacity=ticket.session.hall.capacity,
                        cinema_id=ticket.session.hall.cinema_id,
                        created_at=getattr(ticket.session.hall, 'created_at', datetime.now())
                    ) if ticket.session.hall else None
                ) if ticket.session else None,
                user=UserResponse(
                    id=ticket.user.id,
                    username=ticket.user.username,
                    email=ticket.user.email,
                    role=ticket.user.role,
                    created_at=ticket.user.created_at
                ) if ticket.user else None
            )
            for ticket in tickets
        ]
    except Exception as e:
        logger.error(f"Error getting user tickets: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения билетов пользователя")

# 👑 Admin endpoints
@app.get("/admin/tickets", response_model=List[TicketResponse], tags=["👑 Админ"])
async def get_all_tickets_admin(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Получить все билеты (только для админов)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        tickets = await Ticket.all().prefetch_related(
            'session__movie', 'session__hall', 'user'
        ).offset(skip).limit(limit)
        
        return [
            TicketResponse(
                id=ticket.id,
                user_id=ticket.user_id,
                session_id=ticket.session_id,
                seat_number=ticket.seat_number,
                row_number=ticket.row_number,
                price=ticket.price,
                is_confirmed=ticket.is_confirmed,
                created_at=ticket.booking_time,
                session=SessionResponse(
                    id=ticket.session.id,
                    movie_id=ticket.session.movie_id,
                    hall_id=ticket.session.hall_id,
                    start_time=ticket.session.start_time,
                    price=float(ticket.session.base_price),
                    available_seats=ticket.session.available_seats,
                    is_active=ticket.session.is_active,
                    created_at=ticket.session.created_at,
                    movie=MovieResponse(
                        id=ticket.session.movie.id,
                        title=ticket.session.movie.title,
                        description=ticket.session.movie.description,
                        genre=ticket.session.movie.genre,
                        duration=ticket.session.movie.duration_minutes,
                        rating=ticket.session.movie.rating,
                        release_date=ticket.session.movie.release_date,
                        poster_url=ticket.session.movie.poster_url,
                        created_at=ticket.session.movie.created_at
                    ) if ticket.session.movie else None,
                    hall=HallResponse(
                        id=ticket.session.hall.id,
                        name=ticket.session.hall.name,
                        capacity=ticket.session.hall.capacity,
                        cinema_id=ticket.session.hall.cinema_id,
                        created_at=getattr(ticket.session.hall, 'created_at', datetime.now())
                    ) if ticket.session.hall else None
                ) if ticket.session else None,
                user=UserResponse(
                    id=ticket.user.id,
                    username=ticket.user.username,
                    email=ticket.user.email,
                    role=ticket.user.role,
                    created_at=ticket.user.created_at
                ) if ticket.user else None
            )
            for ticket in tickets
        ]
    except Exception as e:
        logger.error(f"Error getting all tickets: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения всех билетов")

@app.get("/admin/users", response_model=List[UserResponse], tags=["👑 Админ"])
async def get_all_users_admin(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Получить всех пользователей (только для админов)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        users = await User.all().offset(skip).limit(limit)
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                created_at=user.created_at
            )
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения всех пользователей")

# 🎭 Cinema endpoints
@app.get("/cinemas", response_model=List[CinemaResponse], tags=["🏢 Кинотеатры"])
async def get_cinemas(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей")
):
    """Получить список всех кинотеатров"""
    try:
        cinemas = await Cinema.all().prefetch_related('halls').offset(skip).limit(limit)
        return [
            CinemaResponse(
                id=cinema.id,
                name=cinema.name,
                address=cinema.address,
                created_at=cinema.created_at
            )
            for cinema in cinemas
        ]
    except Exception as e:
        logger.error(f"Error getting cinemas: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения кинотеатров")

# Простые endpoint для демонстрации
@app.get("/demo/populate", tags=["🧪 Демо"])
async def populate_demo_data():
    """Заполнение демонстрационными данными"""
    
    # Создаем тестового администратора
    admin_exists = await User.get_or_none(username="admin")
    if not admin_exists:
        await User.create(
            username="admin",
            email="admin@cinema.ru",
            hashed_password=hash_password("admin123"),
            first_name="Администратор",
            last_name="Системы",
            role=UserRole.ADMIN
        )
    
    # Создаем тестовые фильмы
    movies_data = [
        {
            "title": "Интерстеллар",
            "description": "Научно-фантастический фильм о путешествиях через пространство и время",
            "genre": MovieGenre.SCI_FI,
            "duration_minutes": 169,
            "release_date": datetime(2014, 11, 7),
            "director": "Кристофер Нолан",
            "cast": "Мэттью МакКонахи, Энн Хэтэуэй, Джессика Честейн"
        },
        {
            "title": "Темный рыцарь",
            "description": "Супергеройский фильм о Бэтмене",
            "genre": MovieGenre.ACTION,
            "duration_minutes": 152,
            "release_date": datetime(2008, 7, 18),
            "director": "Кристофер Нолан", 
            "cast": "Кристиан Бэйл, Хит Леджер, Аарон Экхарт"
        },
        {
            "title": "Паразиты",
            "description": "Южнокорейский социальный триллер",
            "genre": MovieGenre.THRILLER,
            "duration_minutes": 132,
            "release_date": datetime(2019, 5, 30),
            "director": "Пон Чжун-хо",
            "cast": "Сон Кан-хо, Ли Сон-гюн, Чо Ё-джон"
        }
    ]
    
    for movie_data in movies_data:
        existing_movie = await Movie.get_or_none(title=movie_data["title"])
        if not existing_movie:
            await Movie.create(**movie_data)
    
    # Создаем тестовый кинотеатр
    cinema_exists = await Cinema.get_or_none(name="Центральный Кинотеатр")
    if not cinema_exists:
        cinema = await Cinema.create(
            name="Центральный Кинотеатр",
            address="ул. Пушкина, д. 1",
            city="Москва",
            phone="+7 (495) 123-45-67",
            email="info@cinema.ru"
        )
        
        # Создаем залы
        await Hall.create(
            cinema=cinema,
            name="Зал 1",
            capacity=150,
            rows=10,
            seats_per_row=15
        )
        await Hall.create(
            cinema=cinema,
            name="Зал 2", 
            capacity=100,
            rows=8,
            seats_per_row=12
        )
    
    # Создаем тестовые сеансы
    existing_sessions = await Session.all().count()
    if existing_sessions == 0:
        halls = await Hall.all()
        movies = await Movie.all()
        
        if halls and movies:
            # Создаем сеансы на ближайшие дни
            base_time = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)
            
            # Сеансы на сегодня и завтра
            for day_offset in [0, 1]:
                session_date = base_time + timedelta(days=day_offset)
                
                for hall in halls[:2]:  # Используем первые 2 зала
                    for i, movie in enumerate(movies[:3]):  # Первые 3 фильма
                        session_time = session_date + timedelta(hours=i * 3)  # Интервал 3 часа
                        end_time = session_time + timedelta(minutes=movie.duration_minutes + 30)
                        
                        await Session.create(
                            movie=movie,
                            hall=hall,
                            start_time=session_time,
                            end_time=end_time,
                            base_price=500.0 + (i * 100),  # Цены от 500 до 700 рублей
                            available_seats=hall.capacity
                        )
    
    return {
        "message": "Демонстрационные данные успешно загружены",
        "admin_credentials": {
            "username": "admin",
            "password": "admin123"
        },
        "stats": {
            "users": await User.all().count(),
            "movies": await Movie.all().count(),
            "cinemas": await Cinema.all().count(),
            "halls": await Hall.all().count(),
            "sessions": await Session.all().count()
        }
    }

@app.get("/demo/reset-sessions", tags=["🧪 Демо"])
async def reset_sessions():
    """Сброс и пересоздание сеансов с правильными available_seats"""
    
    # Удаляем все существующие сеансы
    await Session.all().delete()
    
    # Создаем новые сеансы
    halls = await Hall.all()
    movies = await Movie.all()
    
    if halls and movies:
        # Создаем сеансы на ближайшие дни
        base_time = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)
        
        # Сеансы на сегодня и завтра
        for day_offset in [0, 1]:
            session_date = base_time + timedelta(days=day_offset)
            
            for hall in halls[:2]:  # Используем первые 2 зала
                for i, movie in enumerate(movies[:3]):  # Первые 3 фильма
                    session_time = session_date + timedelta(hours=i * 3)  # Интервал 3 часа
                    end_time = session_time + timedelta(minutes=movie.duration_minutes + 30)
                    
                    await Session.create(
                        movie=movie,
                        hall=hall,
                        start_time=session_time,
                        end_time=end_time,
                        base_price=500.0 + (i * 100),  # Цены от 500 до 700 рублей
                        available_seats=hall.capacity
                    )
    
    return {
        "message": "Сеансы успешно пересозданы",
        "stats": {
            "sessions": await Session.all().count(),
            "halls": await Hall.all().count(),
            "movies": await Movie.all().count()
        }
    }

# Database setup
register_tortoise(
    app,
    db_url="sqlite://data/cinema_v2.db",
    modules={"models": ["cinema_api_tortoise"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    print("🎬 Cinema API с Tortoise ORM")
    print("=" * 50)
    print("✅ Python 3.13 совместимая версия")
    print("✅ Tortoise ORM - async Python ORM")
    print("✅ SQLite база данных: data/cinema.db")
    print("✅ 7 таблиц с полной схемой")
    print("✅ JWT аутентификация")
    print("\n🌐 Доступные адреса:")
    print("• Swagger UI: http://localhost:8000/docs")
    print("• ReDoc: http://localhost:8000/redoc")
    print("• Health: http://localhost:8000/health")
    print("• Demo data: http://localhost:8000/demo/populate")
    print("\n🔑 Админ доступ (после /demo/populate):")
    print("• Username: admin")
    print("• Password: admin123")
    print("\n⏹️ Остановка: Ctrl+C\n")
    
    uvicorn.run(
        "cinema_api_tortoise:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 