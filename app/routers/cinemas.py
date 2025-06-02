from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, time

from ..database import get_db
from ..models import Cinema as CinemaModel, Hall as HallModel, User
from ..auth import get_current_user, get_admin_user

router = APIRouter()

# Схемы для кинотеатров
class CinemaBase(BaseModel):
    name: str = Field(..., description="Название кинотеатра")
    address: str = Field(..., description="Адрес")
    city: str = Field(..., description="Город")
    postal_code: Optional[str] = Field(None, description="Почтовый индекс")
    phone: Optional[str] = Field(None, description="Телефон")
    email: Optional[str] = Field(None, description="Email")
    website: Optional[str] = Field(None, description="Веб-сайт")
    latitude: Optional[float] = Field(None, description="Широта")
    longitude: Optional[float] = Field(None, description="Долгота")
    opening_time: Optional[time] = Field(None, description="Время открытия")
    closing_time: Optional[time] = Field(None, description="Время закрытия")
    facilities: Optional[str] = Field(None, description="Удобства (JSON)")
    parking_available: bool = Field(False, description="Наличие парковки")

class CinemaCreate(CinemaBase):
    pass

class Cinema(CinemaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схемы для залов
class HallBase(BaseModel):
    cinema_id: int = Field(..., description="ID кинотеатра")
    name: str = Field(..., description="Название зала")
    hall_number: int = Field(..., description="Номер зала")
    total_seats: int = Field(..., gt=0, description="Общее количество мест")
    rows: int = Field(..., gt=0, description="Количество рядов")
    seats_per_row: int = Field(..., gt=0, description="Мест в ряду")
    screen_type: Optional[str] = Field(None, description="Тип экрана")
    sound_system: Optional[str] = Field(None, description="Звуковая система")
    accessibility: bool = Field(False, description="Доступность для инвалидов")
    vip_seats: int = Field(0, description="VIP места")
    premium_seats: int = Field(0, description="Премиум места")
    standard_seats: int = Field(0, description="Стандартные места")
    seat_map: Optional[str] = Field(None, description="Карта мест (JSON)")

class HallCreate(HallBase):
    pass

class Hall(HallBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=Cinema, summary="Создать кинотеатр")
async def create_cinema(
    cinema: CinemaCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Создание нового кинотеатра (только для администраторов).
    """
    db_cinema = CinemaModel(**cinema.dict())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema

@router.get("/", response_model=List[Cinema], summary="Получить список кинотеатров")
async def get_cinemas(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей на странице"),
    city: Optional[str] = Query(None, description="Фильтр по городу"),
    db: Session = Depends(get_db)
):
    """
    Получение списка кинотеатров с возможностью фильтрации.
    """
    query = db.query(CinemaModel).filter(CinemaModel.is_active == True)
    
    if city:
        query = query.filter(CinemaModel.city.ilike(f"%{city}%"))
    
    cinemas = query.offset(skip).limit(limit).all()
    return cinemas

@router.get("/{cinema_id}", response_model=Cinema, summary="Получить кинотеатр по ID")
async def get_cinema(
    cinema_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение информации о конкретном кинотеатре.
    """
    cinema = db.query(CinemaModel).filter(CinemaModel.id == cinema_id).first()
    if cinema is None:
        raise HTTPException(status_code=404, detail="Кинотеатр не найден")
    return cinema

@router.get("/{cinema_id}/halls", response_model=List[Hall], summary="Получить залы кинотеатра")
async def get_cinema_halls(
    cinema_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение списка залов конкретного кинотеатра.
    """
    cinema = db.query(CinemaModel).filter(CinemaModel.id == cinema_id).first()
    if cinema is None:
        raise HTTPException(status_code=404, detail="Кинотеатр не найден")
    
    halls = db.query(HallModel).filter(
        HallModel.cinema_id == cinema_id,
        HallModel.is_active == True
    ).all()
    return halls

@router.post("/{cinema_id}/halls", response_model=Hall, summary="Создать зал")
async def create_hall(
    cinema_id: int,
    hall: HallCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Создание нового зала в кинотеатре (только для администраторов).
    """
    # Проверяем существование кинотеатра
    cinema = db.query(CinemaModel).filter(CinemaModel.id == cinema_id).first()
    if cinema is None:
        raise HTTPException(status_code=404, detail="Кинотеатр не найден")
    
    # Проверяем уникальность номера зала в кинотеатре
    existing_hall = db.query(HallModel).filter(
        HallModel.cinema_id == cinema_id,
        HallModel.hall_number == hall.hall_number
    ).first()
    
    if existing_hall:
        raise HTTPException(status_code=400, detail="Зал с таким номером уже существует")
    
    hall_data = hall.dict()
    hall_data["cinema_id"] = cinema_id
    db_hall = HallModel(**hall_data)
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall

@router.get("/halls/{hall_id}", response_model=Hall, summary="Получить зал по ID")
async def get_hall(
    hall_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение информации о конкретном зале.
    """
    hall = db.query(HallModel).filter(HallModel.id == hall_id).first()
    if hall is None:
        raise HTTPException(status_code=404, detail="Зал не найден")
    return hall

@router.get("/search", summary="Поиск кинотеатров")
async def search_cinemas(
    lat: Optional[float] = Query(None, description="Широта для поиска рядом"),
    lng: Optional[float] = Query(None, description="Долгота для поиска рядом"),
    radius: Optional[float] = Query(10.0, description="Радиус поиска в км"),
    db: Session = Depends(get_db)
):
    """
    Поиск кинотеатров по геолокации.
    Примечание: Для полноценной геолокации нужно использовать PostGIS.
    """
    query = db.query(CinemaModel).filter(CinemaModel.is_active == True)
    
    if lat is not None and lng is not None:
        # Простая фильтрация по координатам (для демонстрации)
        # В продакшене следует использовать PostGIS для точных расчетов
        lat_range = radius / 111.0  # Примерное преобразование км в градусы
        lng_range = radius / (111.0 * abs(lat))
        
        query = query.filter(
            CinemaModel.latitude.between(lat - lat_range, lat + lat_range),
            CinemaModel.longitude.between(lng - lng_range, lng + lng_range)
        )
    
    cinemas = query.all()
    return cinemas 