from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import Ticket as TicketModel, Session as SessionModel
from ..schemas import Ticket, TicketCreate, TicketUpdate, TicketList

router = APIRouter()

@router.post("/", response_model=Ticket, summary="Забронировать билет")
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):
    """
    Бронирование билета на сеанс.
    
    - **session_id**: ID сеанса (обязательно)
    - **seat_number**: Номер места
    - **customer_name**: Имя клиента
    - **customer_email**: Email клиента
    - **customer_phone**: Телефон клиента
    - **price**: Цена билета
    """
    # Проверяем существование сеанса
    session = db.query(SessionModel).filter(SessionModel.id == ticket.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    
    if not session.is_active:
        raise HTTPException(status_code=400, detail="Сеанс неактивен")
    
    # Проверяем, что место свободно
    existing_ticket = db.query(TicketModel).filter(
        TicketModel.session_id == ticket.session_id,
        TicketModel.seat_number == ticket.seat_number
    ).first()
    
    if existing_ticket:
        raise HTTPException(status_code=400, detail="Место уже занято")
    
    # Проверяем валидность номера места
    if ticket.seat_number < 1 or ticket.seat_number > session.total_seats:
        raise HTTPException(status_code=400, detail="Неверный номер места")
    
    # Создаем билет
    db_ticket = TicketModel(**ticket.dict())
    db.add(db_ticket)
    
    # Уменьшаем количество доступных мест
    session.available_seats -= 1
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/", response_model=TicketList, summary="Получить список билетов")
async def get_tickets(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей на странице"),
    session_id: Optional[int] = Query(None, description="Фильтр по ID сеанса"),
    customer_name: Optional[str] = Query(None, description="Фильтр по имени клиента"),
    customer_email: Optional[str] = Query(None, description="Фильтр по email клиента"),
    is_paid: Optional[bool] = Query(None, description="Фильтр по статусу оплаты"),
    db: Session = Depends(get_db)
):
    """
    Получение списка билетов с возможностью фильтрации.
    """
    query = db.query(TicketModel)
    
    if session_id:
        query = query.filter(TicketModel.session_id == session_id)
    
    if customer_name:
        query = query.filter(TicketModel.customer_name.ilike(f"%{customer_name}%"))
    
    if customer_email:
        query = query.filter(TicketModel.customer_email.ilike(f"%{customer_email}%"))
    
    if is_paid is not None:
        query = query.filter(TicketModel.is_paid == is_paid)
    
    query = query.order_by(TicketModel.booking_time.desc())
    
    total = query.count()
    tickets = query.offset(skip).limit(limit).all()
    
    return TicketList(
        tickets=tickets,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )

@router.get("/{ticket_id}", response_model=Ticket, summary="Получить билет по ID")
async def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного билета по его ID.
    """
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Билет не найден")
    return ticket

@router.put("/{ticket_id}", response_model=Ticket, summary="Обновить билет")
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновление данных билета.
    """
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Билет не найден")
    
    update_data = ticket_update.dict(exclude_unset=True)
    
    # Если обновляется номер места, проверяем его доступность
    if "seat_number" in update_data:
        new_seat = update_data["seat_number"]
        session = ticket.session
        
        # Проверяем валидность номера места
        if new_seat < 1 or new_seat > session.total_seats:
            raise HTTPException(status_code=400, detail="Неверный номер места")
        
        # Проверяем, что место свободно (кроме текущего билета)
        existing_ticket = db.query(TicketModel).filter(
            TicketModel.session_id == ticket.session_id,
            TicketModel.seat_number == new_seat,
            TicketModel.id != ticket_id
        ).first()
        
        if existing_ticket:
            raise HTTPException(status_code=400, detail="Место уже занято")
    
    if update_data:
        for field, value in update_data.items():
            setattr(ticket, field, value)
        
        db.commit()
        db.refresh(ticket)
    
    return ticket

@router.delete("/{ticket_id}", summary="Отменить бронирование билета")
async def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """
    Отмена бронирования билета.
    """
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Билет не найден")
    
    session = ticket.session
    
    # Увеличиваем количество доступных мест
    session.available_seats += 1
    
    db.delete(ticket)
    db.commit()
    return {"message": "Бронирование билета отменено"}

@router.patch("/{ticket_id}/pay", response_model=Ticket, summary="Оплатить билет")
async def pay_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """
    Отметка билета как оплаченного.
    """
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Билет не найден")
    
    if ticket.is_paid:
        raise HTTPException(status_code=400, detail="Билет уже оплачен")
    
    ticket.is_paid = True
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/customer/{customer_email}", summary="Получить билеты клиента")
async def get_customer_tickets(
    customer_email: str,
    db: Session = Depends(get_db)
):
    """
    Получение всех билетов конкретного клиента по email.
    """
    tickets = db.query(TicketModel).filter(
        TicketModel.customer_email == customer_email
    ).order_by(TicketModel.booking_time.desc()).all()
    
    return tickets

@router.get("/statistics/", summary="Статистика по билетам")
async def get_tickets_statistics(
    date_from: Optional[datetime] = Query(None, description="Дата начала периода"),
    date_to: Optional[datetime] = Query(None, description="Дата окончания периода"),
    db: Session = Depends(get_db)
):
    """
    Получение статистики по билетам за период.
    """
    query = db.query(TicketModel)
    
    if date_from:
        query = query.filter(TicketModel.booking_time >= date_from)
    
    if date_to:
        query = query.filter(TicketModel.booking_time <= date_to)
    
    total_tickets = query.count()
    paid_tickets = query.filter(TicketModel.is_paid == True).count()
    unpaid_tickets = total_tickets - paid_tickets
    
    total_revenue = sum([ticket.price for ticket in query.filter(TicketModel.is_paid == True).all()])
    
    return {
        "total_tickets": total_tickets,
        "paid_tickets": paid_tickets,
        "unpaid_tickets": unpaid_tickets,
        "total_revenue": total_revenue,
        "average_ticket_price": total_revenue / paid_tickets if paid_tickets > 0 else 0
    } 