from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

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

# Схемы для фильмов
class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название фильма")
    description: Optional[str] = Field(None, description="Описание фильма")
    duration_minutes: int = Field(..., gt=0, description="Продолжительность в минутах")
    genre: MovieGenre
    director: Optional[str] = Field(None, max_length=255, description="Режиссер")
    release_year: Optional[int] = Field(None, ge=1900, le=2030, description="Год выпуска")
    rating: Optional[float] = Field(0.0, ge=0.0, le=10.0, description="Рейтинг фильма")
    poster_url: Optional[str] = Field(None, description="URL постера")
    trailer_url: Optional[str] = Field(None, description="URL трейлера")
    is_active: bool = Field(True, description="Активен ли фильм")

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    genre: Optional[MovieGenre] = None
    director: Optional[str] = Field(None, max_length=255)
    release_year: Optional[int] = Field(None, ge=1900, le=2030)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    is_active: Optional[bool] = None

class MovieResponse(MovieBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime

# Схемы для сеансов
class SessionBase(BaseModel):
    movie_id: int = Field(..., description="ID фильма")
    hall_id: int = Field(..., description="ID зала")
    start_time: datetime = Field(..., description="Время начала сеанса")
    end_time: datetime = Field(..., description="Время окончания сеанса")
    base_price: float = Field(..., gt=0, description="Базовая цена билета")
    language: Optional[str] = Field(None, description="Язык фильма")
    subtitles: Optional[str] = Field(None, description="Субтитры")
    format_3d: bool = Field(False, description="3D формат")
    format_imax: bool = Field(False, description="IMAX формат")
    is_active: bool = Field(True, description="Активен ли сеанс")

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    movie_id: Optional[int] = None
    hall_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    base_price: Optional[float] = Field(None, gt=0)
    language: Optional[str] = None
    subtitles: Optional[str] = None
    format_3d: Optional[bool] = None
    format_imax: Optional[bool] = None
    is_active: Optional[bool] = None

class Session(SessionBase):
    id: int
    available_seats: int
    sold_tickets: int
    reserved_tickets: int
    is_sold_out: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Схемы для билетов
class TicketBase(BaseModel):
    session_id: int = Field(..., description="ID сеанса")
    seat_row: int = Field(..., gt=0, description="Ряд")
    seat_number: int = Field(..., gt=0, description="Номер места")
    seat_type: str = Field("standard", description="Тип места")
    price: float = Field(..., gt=0, description="Цена билета")

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    seat_row: Optional[int] = Field(None, gt=0)
    seat_number: Optional[int] = Field(None, gt=0)
    seat_type: Optional[str] = None
    status: Optional[str] = None
    is_paid: Optional[bool] = None

class Ticket(TicketBase):
    id: int
    user_id: int
    booking_reference: str
    status: str
    payment_method: Optional[str]
    final_price: float
    is_paid: bool
    booking_time: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# Схемы для пользователей
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    role: UserRole
    is_active: bool
    loyalty_points: int
    total_spent: float
    created_at: datetime

# Схемы для ответов
class MovieList(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    per_page: int

class SessionList(BaseModel):
    sessions: List[Session]
    total: int
    page: int
    per_page: int

class TicketList(BaseModel):
    tickets: List[Ticket]
    total: int
    page: int
    per_page: int 