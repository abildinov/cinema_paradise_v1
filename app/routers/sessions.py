from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import Session as SessionModel, Movie as MovieModel, Ticket
from ..schemas import Session as SessionSchema, SessionCreate, SessionUpdate, SessionList

router = APIRouter()

@router.post("/", response_model=SessionSchema, summary="Создать сеанс")
async def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового сеанса в базе данных.
    
    - **movie_id**: ID фильма (обязательно)
    - **start_time**: Время начала сеанса
    - **end_time**: Время окончания сеанса
    - **hall_number**: Номер зала
    - **total_seats**: Общее количество мест
    - **price**: Цена билета
    """
    # Проверяем существование фильма
    movie = db.query(MovieModel).filter(MovieModel.id == session.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    # Проверяем логику времени
    if session.end_time <= session.start_time:
        raise HTTPException(status_code=400, detail="Время окончания должно быть позже времени начала")
    
    db_session = SessionModel(
        **session.dict(),
        available_seats=session.total_seats  # Изначально все места доступны
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=SessionList, summary="Получить список сеансов")
async def get_sessions(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей на странице"),
    movie_id: Optional[int] = Query(None, description="Фильтр по ID фильма"),
    hall_number: Optional[int] = Query(None, description="Фильтр по номеру зала"),
    date_from: Optional[datetime] = Query(None, description="Фильтр сеансов от даты"),
    date_to: Optional[datetime] = Query(None, description="Фильтр сеансов до даты"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    db: Session = Depends(get_db)
):
    """
    Получение списка сеансов с возможностью фильтрации.
    """
    query = db.query(SessionModel)
    
    if movie_id:
        query = query.filter(SessionModel.movie_id == movie_id)
    
    if hall_number:
        query = query.filter(SessionModel.hall_number == hall_number)
    
    if date_from:
        query = query.filter(SessionModel.start_time >= date_from)
    
    if date_to:
        query = query.filter(SessionModel.start_time <= date_to)
    
    if is_active is not None:
        query = query.filter(SessionModel.is_active == is_active)
    
    query = query.order_by(SessionModel.start_time)
    
    total = query.count()
    sessions = query.offset(skip).limit(limit).all()
    
    return SessionList(
        sessions=sessions,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )

@router.get("/{session_id}", response_model=SessionSchema, summary="Получить сеанс по ID")
async def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного сеанса по его ID.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    return session

@router.put("/{session_id}", response_model=SessionSchema, summary="Обновить сеанс")
async def update_session(
    session_id: int,
    session_update: SessionUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновление данных сеанса.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    update_data = session_update.dict(exclude_unset=True)
    
    # Если обновляется movie_id, проверяем существование фильма
    if "movie_id" in update_data:
        movie = db.query(MovieModel).filter(MovieModel.id == update_data["movie_id"]).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Фильм не найден")
    
    # Если обновляется total_seats, пересчитываем available_seats
    if "total_seats" in update_data:
        sold_tickets = len(session.tickets)
        new_total = update_data["total_seats"]
        if new_total < sold_tickets:
            raise HTTPException(status_code=400, detail="Нельзя уменьшить количество мест меньше проданных билетов")
        update_data["available_seats"] = new_total - sold_tickets
    
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        for field, value in update_data.items():
            setattr(session, field, value)
        
        db.commit()
        db.refresh(session)
    
    return session

@router.delete("/{session_id}", summary="Удалить сеанс")
async def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаление сеанса из базы данных.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    # Проверяем, есть ли проданные билеты
    if session.tickets:
        raise HTTPException(status_code=400, detail="Нельзя удалить сеанс с проданными билетами")
    
    db.delete(session)
    db.commit()
    return {"message": "Сеанс успешно удален"}

@router.get("/{session_id}/tickets", summary="Получить билеты сеанса")
async def get_session_tickets(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение всех билетов конкретного сеанса.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    return session.tickets

@router.get("/{session_id}/available-seats", summary="Получить доступные места")
async def get_available_seats(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение списка доступных мест для сеанса.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    occupied_seats = [ticket.seat_number for ticket in session.tickets]
    available_seats = [seat for seat in range(1, session.total_seats + 1) 
                      if seat not in occupied_seats]
    
    return {
        "session_id": session_id,
        "total_seats": session.total_seats,
        "available_seats": available_seats,
        "occupied_seats": occupied_seats,
        "available_count": len(available_seats)
    } 