from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL подключения к базе данных
# Для демонстрации используем SQLite, в продакшене - PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cinema_api.db")

# Создание движка SQLAlchemy
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Логирование SQL запросов для отладки
        connect_args={"check_same_thread": False}  # Для SQLite
    )
else:
    # Настройки для PostgreSQL в продакшене
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Логирование SQL запросов для отладки
    )

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 