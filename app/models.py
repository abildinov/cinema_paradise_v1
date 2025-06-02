from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, Enum, DECIMAL, Time
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

class UserRole(enum.Enum):
    """Роли пользователей"""
    ADMIN = "admin"
    MANAGER = "manager"
    CUSTOMER = "customer"

class MovieGenre(enum.Enum):
    """Жанры фильмов"""
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
    date_of_birth = Column(DateTime)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(500))
    address = Column(Text)
    city = Column(String(100))
    postal_code = Column(String(20))
    loyalty_points = Column(Integer, default=0)
    total_spent = Column(DECIMAL(10, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Связи
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

class Movie(Base):
    """Модель фильма"""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    original_title = Column(String(255))
    description = Column(Text)
    synopsis = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(Enum(MovieGenre), nullable=False)
    director = Column(String(255))
    producer = Column(String(255))
    writer = Column(String(255))
    cast = Column(Text)  # JSON string with cast list
    release_year = Column(Integer)
    release_date = Column(DateTime)
    country = Column(String(100))
    language = Column(String(50))
    age_rating = Column(String(10))  # G, PG, PG-13, R, NC-17
    rating = Column(Float, default=0.0)
    imdb_rating = Column(Float)
    budget = Column(DECIMAL(15, 2))
    box_office = Column(DECIMAL(15, 2))
    poster_url = Column(String(500))
    trailer_url = Column(String(500))
    backdrop_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    awards = Column(Text)  # JSON string with awards
    tags = Column(Text)  # JSON string with tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    sessions = relationship("Session", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")

class Cinema(Base):
    """Модель кинотеатра"""
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    opening_time = Column(Time)
    closing_time = Column(Time)
    facilities = Column(Text)  # JSON string with facilities
    parking_available = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    halls = relationship("Hall", back_populates="cinema", cascade="all, delete-orphan")

class Hall(Base):
    """Модель зала"""
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=False)
    name = Column(String(100), nullable=False)
    hall_number = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False)
    rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)
    screen_type = Column(String(50))  # IMAX, 3D, Standard, 4DX
    sound_system = Column(String(50))  # Dolby Atmos, DTS:X, Standard
    accessibility = Column(Boolean, default=False)
    vip_seats = Column(Integer, default=0)
    premium_seats = Column(Integer, default=0)
    standard_seats = Column(Integer, default=0)
    seat_map = Column(Text)  # JSON string with seat layout
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    cinema = relationship("Cinema", back_populates="halls")
    sessions = relationship("Session", back_populates="hall", cascade="all, delete-orphan")

class Session(Base):
    """Модель сеанса"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    base_price = Column(DECIMAL(8, 2), nullable=False)
    vip_price = Column(DECIMAL(8, 2))
    premium_price = Column(DECIMAL(8, 2))
    available_seats = Column(Integer, nullable=False)
    sold_tickets = Column(Integer, default=0)
    reserved_tickets = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_sold_out = Column(Boolean, default=False)
    language = Column(String(50))
    subtitles = Column(String(50))
    format_3d = Column(Boolean, default=False)
    format_imax = Column(Boolean, default=False)
    early_bird_discount = Column(Float, default=0.0)
    late_show_surcharge = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    seat_type = Column(String(20), default="standard")  # standard, premium, vip
    price = Column(DECIMAL(8, 2), nullable=False)
    discount_applied = Column(DECIMAL(8, 2), default=0.0)
    final_price = Column(DECIMAL(8, 2), nullable=False)
    booking_reference = Column(String(20), unique=True, nullable=False, index=True)
    status = Column(String(20), default="reserved")  # reserved, paid, cancelled, used
    payment_method = Column(String(50))
    payment_transaction_id = Column(String(255))
    qr_code = Column(String(500))
    is_paid = Column(Boolean, default=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
    payment_time = Column(DateTime)
    cancellation_time = Column(DateTime)
    used_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с сеансом и пользователем
    session = relationship("Session", back_populates="tickets")
    user = relationship("User", back_populates="tickets")

class Review(Base):
    """Модель отзыва о фильме"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-10
    title = Column(String(255))
    content = Column(Text)
    is_spoiler = Column(Boolean, default=False)
    is_verified_purchase = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    unhelpful_votes = Column(Integer, default=0)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews") 