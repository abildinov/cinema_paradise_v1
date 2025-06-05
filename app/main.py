from fastapi import FastAPI, Header, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import create_engine
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session

# Импортируем модели напрямую для избежания циклических зависимостей
try:
    from app import models
    User = models.User
    Movie = models.Movie
    Hall = models.Hall
    Session = models.Session
    Ticket = models.Ticket
    Cinema = models.Cinema
except ImportError as e:
    print(f"Ошибка импорта моделей: {e}")

from app.models import UserRole, MovieGenre

# Создаем приложение FastAPI
app = FastAPI(
    title="🎬 Cinema Paradise API",
    description="API для управления кинотеатром",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Функция для добавления тестовых данных в БД
def init_db():
    db = next(get_db())
    # Проверяем, есть ли данные
    try:
        # Создаем таблицы, если они еще не созданы
        Base.metadata.create_all(bind=engine)
        
        if db.query(User).first() is None:
            # Добавляем пользователей
            admin = User(username="admin", email="admin@cinema.com", hashed_password="admin123", first_name="Admin", last_name="User", role=UserRole.ADMIN)
            manager = User(username="manager", email="manager@cinema.com", hashed_password="manager123", first_name="Manager", last_name="User", role=UserRole.MANAGER)
            user = User(username="user", email="user@cinema.com", hashed_password="user123", first_name="Regular", last_name="User", role=UserRole.CUSTOMER)
            db.add(admin)
            db.add(manager)
            db.add(user)
            db.commit()
            print("Тестовые пользователи добавлены")
        else:
            print("Пользователи уже существуют")
        
        if db.query(Movie).first() is None:
            # Добавляем фильмы
            movie1 = Movie(title="Аватар: Путь воды", duration_minutes=192, rating=8.5, genre=MovieGenre.SCI_FI)
            movie2 = Movie(title="Топ Ган: Мэверик", duration_minutes=130, rating=8.8, genre=MovieGenre.ACTION)
            movie3 = Movie(title="Чёрная пантера: Ваканда навеки", duration_minutes=161, rating=7.2, genre=MovieGenre.ACTION)
            db.add(movie1)
            db.add(movie2)
            db.add(movie3)
            db.commit()
            print("Тестовые фильмы добавлены")
        else:
            print("Фильмы уже существуют")
        
        if db.query(Cinema).first() is None:
            # Добавляем кинотеатр
            cinema = Cinema(name="Cinema Paradise", address="ул. Примерная, 123", city="Москва")
            db.add(cinema)
            db.commit()
            print("Тестовый кинотеатр добавлен")
        else:
            print("Кинотеатр уже существует")
        
        if db.query(Hall).first() is None:
            # Добавляем залы
            cinema = db.query(Cinema).first()
            hall1 = Hall(cinema_id=cinema.id, name="Зал №1", hall_number=1, total_seats=100, rows=10, seats_per_row=10)
            hall2 = Hall(cinema_id=cinema.id, name="Зал №2", hall_number=2, total_seats=80, rows=8, seats_per_row=10)
            db.add(hall1)
            db.add(hall2)
            db.commit()
            print("Тестовые залы добавлены")
        else:
            print("Залы уже существуют")
        
        if db.query(Session).first() is None:
            # Добавляем сеансы
            from datetime import datetime
            session1 = Session(movie_id=1, hall_id=1, start_time=datetime(2024, 1, 15, 14, 0), end_time=datetime(2024, 1, 15, 17, 12), date=datetime(2024, 1, 15), base_price=450, available_seats=100)
            session2 = Session(movie_id=2, hall_id=2, start_time=datetime(2024, 1, 15, 16, 30), end_time=datetime(2024, 1, 15, 18, 40), date=datetime(2024, 1, 15), base_price=400, available_seats=80)
            session3 = Session(movie_id=3, hall_id=1, start_time=datetime(2024, 1, 15, 19, 0), end_time=datetime(2024, 1, 15, 21, 41), date=datetime(2024, 1, 15), base_price=420, available_seats=100)
            db.add(session1)
            db.add(session2)
            db.add(session3)
            db.commit()
            print("Тестовые сеансы добавлены")
        else:
            print("Сеансы уже существуют")
        
        if db.query(Ticket).first() is None:
            # Добавляем тестовые билеты
            from datetime import datetime
            ticket1 = Ticket(user_id=1, session_id=1, seat_row=2, seat_number=5, price=450, final_price=450, status="booked", booking_reference="REF1", is_paid=True, booking_time=datetime(2024, 1, 15, 10, 30))
            ticket2 = Ticket(user_id=3, session_id=2, seat_row=3, seat_number=3, price=400, final_price=400, status="booked", booking_reference="REF2", is_paid=False, booking_time=datetime(2024, 1, 15, 11, 15))
            db.add(ticket1)
            db.add(ticket2)
            db.commit()
            print("Тестовые билеты добавлены")
        else:
            print("Билеты уже существуют")
    except Exception as e:
        print(f"Ошибка при инициализации данных: {e}")
    finally:
        db.close()

# Вызываем инициализацию при запуске
@app.on_event("startup")
async def startup_db_client():
    # Убедимся, что таблицы созданы перед инициализацией данных
    Base.metadata.create_all(bind=engine)
    init_db()
    print("База данных инициализирована")

# Базовые эндпоинты
@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": "🎬 Cinema Paradise API",
        "status": "active",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья системы"""
    return {
        "status": "healthy",
        "service": "Cinema Paradise API",
        "timestamp": "2024-01-15T12:00:00Z"
    }

# Демо эндпоинты для базовой функциональности
@app.get("/movies")
async def get_movies(db: Session = Depends(get_db)):
    """Получить список фильмов"""
    movies = db.query(Movie).all()
    return [{
        "id": movie.id,
        "title": movie.title,
        "duration": movie.duration_minutes,
        "rating": movie.rating,
        "genre": movie.genre.value
    } for movie in movies]

@app.get("/sessions")
async def get_sessions(db: Session = Depends(get_db)):
    """Получить список сеансов"""
    sessions = db.query(Session).all()
    result = []
    for session in sessions:
        movie = db.query(Movie).filter(Movie.id == session.movie_id).first()
        hall = db.query(Hall).filter(Hall.id == session.hall_id).first()
        result.append({
            "id": session.id,
            "movie_id": session.movie_id,
            "movie": {"title": movie.title},
            "start_time": session.start_time.isoformat(),
            "price": float(session.base_price),
            "hall_id": session.hall_id,
            "hall": {"name": hall.name, "capacity": hall.total_seats},
            "available_seats": session.available_seats
        })
    return result

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Авторизация пользователя через форму (form-data)"""
    username = form_data.username
    password = form_data.password
    user = db.query(User).filter(User.username == username).first()
    # В реальном приложении сравнивай хеш пароля!
    if user and user.hashed_password == password:
        token = f"demo_token_{username}"
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "role": user.role.value,
                "email": user.email
            }
        }
    else:
        return JSONResponse(
            status_code=401,
            content={"detail": "Неверные учетные данные"}
        )

@app.post("/auth/register")
async def register(user_data: dict, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    print(f"Данные регистрации: {user_data}")
    username = user_data.get("username")
    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name", "User")
    last_name = user_data.get("last_name", "Lastname")
    
    # Проверяем, существует ли пользователь
    if db.query(User).filter(User.username == username).first():
        return JSONResponse(
            status_code=400,
            content={"detail": "Пользователь уже существует"}
        )
    
    # Создаем нового пользователя
    new_user = User(username=username, email=email, hashed_password=password, first_name=first_name, last_name=last_name, role=UserRole.CUSTOMER)
    db.add(new_user)
    db.commit()
    
    return {
        "message": "Пользователь зарегистрирован",
        "username": username,
        "email": email
    }

@app.get("/auth/me")
async def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Получить данные текущего пользователя"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    # Извлекаем токен из заголовка "Bearer token"
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    except:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    # Извлекаем username из токена
    username = token.replace("demo_token_", "")
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {
            "username": user.username,
            "role": user.role.value,
            "email": user.email
        }
    else:
        raise HTTPException(status_code=401, detail="Недействительный токен")

@app.get("/demo/populate")
async def populate_demo_data(db: Session = Depends(get_db)):
    """Загрузить демо данные"""
    init_db()
    user_count = db.query(User).count()
    return {
        "message": "Демо данные загружены",
        "movies": 3,
        "sessions": 2,
        "users": user_count
    }

# ИСПРАВЛЕННЫЕ ЭНДПОИНТЫ ДЛЯ БИЛЕТОВ
@app.get("/tickets/my")
async def get_my_tickets(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Получить мои билеты"""
    if not authorization:
        return JSONResponse(
            status_code=401,
            content={"detail": "Не авторизован"}
        )
    
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    except:
        return JSONResponse(
            status_code=401,
            content={"detail": "Неверный формат токена"}
        )
    
    username = token.replace("demo_token_", "")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "Недействительный токен"}
        )
    
    tickets = db.query(Ticket).filter(Ticket.user_id == user.id).all()
    result = []
    for ticket in tickets:
        session = db.query(Session).filter(Session.id == ticket.session_id).first()
        movie = db.query(Movie).filter(Movie.id == session.movie_id).first()
        hall = db.query(Hall).filter(Hall.id == session.hall_id).first()
        result.append({
            "id": ticket.id,
            "session_id": ticket.session_id,
            "seat_numbers": [ticket.seat_number],
            "seat_number": ticket.seat_number,
            "row_number": ticket.seat_row,
            "total_price": float(ticket.final_price),
            "price": float(ticket.price),
            "user": username,
            "customer_name": username,
            "customer_email": user.email,
            "booking_time": ticket.booking_time.isoformat(),
            "status": ticket.status,
            "is_paid": ticket.is_paid,
            "is_confirmed": ticket.is_paid,
            "session": {
                "id": session.id,
                "movie": {"title": movie.title, "id": movie.id},
                "hall": {"name": hall.name, "id": hall.id},
                "start_time": session.start_time.isoformat()
            }
        })
    return result

# Функция для извлечения username из токена (заглушка, в реальном приложении нужно проверять токен)
def get_username_from_token(token: str) -> str:
    token_to_user = {
        "demo_token_admin": "admin",
        "demo_token_user": "user"
    }
    return token_to_user.get(token, "unknown_user")

@app.post("/tickets")
async def create_ticket(ticket_data: dict, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Создать новый билет (бронирование) - УЛУЧШЕННАЯ ВЕРСИЯ С ПОДРОБНОСТЯМИ"""
    print("Начало обработки запроса /tickets")
    if not authorization:
        print("Ошибка: Токен не предоставлен")
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    # Извлекаем токен из заголовка
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        print(f"Токен извлечен: {token}")
    except:
        print("Ошибка: Неверный формат токена")
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    # Извлекаем username из токена
    username = token.replace("demo_token_", "")
    print(f"Username извлечен из токена: {username}")
    
    # Проверяем пользователя в базе
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"Ошибка: Пользователь {username} не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    print(f"Пользователь найден: {username}, ID: {user.id}")
    
    # Проверяем наличие данных о бронировании
    session_id = ticket_data.get("session_id")
    seat_numbers = ticket_data.get("seat_numbers", [])
    total_price = ticket_data.get("total_price")
    
    if not session_id or not seat_numbers:
        print("Ошибка: Не указан session_id или seat_numbers")
        raise HTTPException(status_code=400, detail="Не указан session_id или seat_numbers")
    print(f"Данные бронирования: session_id={session_id}, seat_numbers={seat_numbers}, total_price={total_price}")
    
    # Проверяем существование сеанса
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        print(f"Ошибка: Сеанс {session_id} не найден")
        raise HTTPException(status_code=404, detail="Сеанс не найден")
    print(f"Сеанс найден: {session_id}")
    
    # Проверяем зал
    hall = db.query(Hall).filter(Hall.id == session.hall_id).first()
    if not hall:
        print(f"Ошибка: Зал для сеанса {session_id} не найден")
        raise HTTPException(status_code=404, detail="Зал не найден")
    print(f"Зал найден: {hall.name}, всего мест: {hall.total_seats}")
    
    # Проверяем доступность мест
    if session.available_seats < len(seat_numbers):
        print(f"Ошибка: Недостаточно свободных мест. Доступно: {session.available_seats}, запрошено: {len(seat_numbers)}")
        raise HTTPException(status_code=400, detail=f"Недостаточно свободных мест. Доступно: {session.available_seats}")
    print(f"Свободных мест достаточно: {session.available_seats}")
    
    # Проверяем, не заняты ли места
    existing_tickets = db.query(Ticket).filter(Ticket.session_id == session_id, Ticket.seat_number.in_(seat_numbers)).all()
    if existing_tickets:
        occupied_seats = [ticket.seat_number for ticket in existing_tickets]
        print(f"Ошибка: Места уже заняты: {occupied_seats}")
        raise HTTPException(status_code=400, detail=f"Места уже заняты: {occupied_seats}")
    print("Все указанные места свободны")
    
    # Проверяем фильм
    movie = db.query(Movie).filter(Movie.id == session.movie_id).first()
    if movie:
        print(f"Фильм: {movie.title}, Зал: {hall.name}")
    
    # Создаем билеты
    import uuid
    tickets = []
    base_price_per_seat = float(session.base_price) / len(seat_numbers) if total_price is None else float(total_price) / len(seat_numbers)
    
    # Получаем конфигурацию зала для правильного расчета рядов
    seats_per_row = 10  # По умолчанию 10 мест в ряду
    if hasattr(hall, 'seats_per_row') and hall.seats_per_row:
        seats_per_row = hall.seats_per_row
    else:
        # Вычисляем seats_per_row на основе общего количества мест и рядов
        total_seats = hall.total_seats
        estimated_rows = max(1, int((total_seats / 10) + 0.5))  # Примерно 10 мест в ряду
        seats_per_row = max(1, total_seats // estimated_rows)
    
    for seat_number in seat_numbers:
        # Вычисляем ряд на основе номера места
        seat_row = ((seat_number - 1) // seats_per_row) + 1
        seat_in_row = ((seat_number - 1) % seats_per_row) + 1
        
        # Определяем тип места и цену (упрощенная логика)
        seat_type = "standard"
        seat_price = base_price_per_seat
        # Проверяем, является ли место VIP или премиум на основе количества мест (примерная логика)
        if seat_number <= hall.vip_seats:
            seat_type = "vip"
            seat_price = float(session.vip_price) if session.vip_price else base_price_per_seat * 1.5
        elif seat_number <= (hall.vip_seats + hall.premium_seats):
            seat_type = "premium"
            seat_price = float(session.premium_price) if session.premium_price else base_price_per_seat * 1.2
        
        ticket = Ticket(
            user_id=user.id,
            session_id=session_id,
            seat_row=seat_row,  # Правильно вычисленный ряд
            seat_number=seat_number,
            seat_type=seat_type,
            price=seat_price,
            final_price=seat_price,
            booking_reference=str(uuid.uuid4())[:8].upper(),
            status="booked",
            is_paid=False
        )
        db.add(ticket)
        tickets.append(ticket)
        print(f"Билет создан: ряд {seat_row}, место {seat_number} (в ряду: {seat_in_row}), тип {seat_type}, цена {seat_price}")
    
    # Обновляем количество доступных мест в сеансе
    session.available_seats -= len(seat_numbers)
    session.reserved_tickets += len(seat_numbers)
    if session.available_seats == 0:
        session.is_sold_out = True
    
    db.commit()
    print(f"Сеанс обновлен: доступно мест {session.available_seats}, зарезервировано билетов {session.reserved_tickets}")
    
    return {
        "message": f"Билеты успешно забронированы для {username}",
        "ticket_ids": [ticket.id for ticket in tickets],
        "booking_references": [ticket.booking_reference for ticket in tickets]
    }

@app.get("/admin/users")
async def get_admin_users(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Получить список пользователей (только для админа)"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    except:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    username = token.replace("demo_token_", "")
    current_user = db.query(User).filter(User.username == username).first()
    if not current_user or current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    users = db.query(User).all()
    return [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat() if user.created_at else None
    } for user in users]

@app.get("/admin/tickets")
async def get_admin_tickets(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Получить все билеты (для админа)"""
    if not authorization:
        return JSONResponse(
            status_code=401,
            content={"detail": "Не авторизован"}
        )
    
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    except:
        return JSONResponse(
            status_code=401,
            content={"detail": "Неверный формат токена"}
        )
    
    username = token.replace("demo_token_", "")
    current_user = db.query(User).filter(User.username == username).first()
    if not current_user or current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        return JSONResponse(
            status_code=403,
            content={"detail": "Доступ запрещён"}
        )
    
    tickets = db.query(Ticket).all()
    result = []
    print(f"🔍 Админ запросил билеты. Найдено: {len(tickets)} билетов")
    for ticket in tickets:
        session = db.query(Session).filter(Session.id == ticket.session_id).first()
        movie = db.query(Movie).filter(Movie.id == session.movie_id).first()
        hall = db.query(Hall).filter(Hall.id == session.hall_id).first()
        user = db.query(User).filter(User.id == ticket.user_id).first()
        print(f"   - Билет #{ticket.id}: {user.username} → {movie.title}, место {ticket.seat_number}")
        result.append({
            "id": ticket.id,
            "session_id": ticket.session_id,
            "seat_numbers": [ticket.seat_number],
            "seat_number": ticket.seat_number,
            "row_number": ticket.seat_row,
            "total_price": float(ticket.final_price),
            "price": float(ticket.price),
            "user": user.username,
            "customer_name": user.username,
            "customer_email": user.email,
            "booking_time": ticket.booking_time.isoformat(),
            "purchase_date": ticket.booking_time.isoformat(),
            "status": ticket.status,
            "is_paid": ticket.is_paid,
            "is_confirmed": ticket.is_paid,
            "customer_phone": user.phone or "",
            "session": {
                "id": session.id,
                "movie": {"title": movie.title, "id": movie.id},
                "hall": {"name": hall.name, "id": hall.id},
                "start_time": session.start_time.isoformat()
            },
            "movie_title": movie.title,
            "movie": {"title": movie.title, "id": movie.id},
            "hall_name": hall.name,
            "hall": {"name": hall.name, "id": hall.id},
            "start_time": session.start_time.isoformat(),
            "user_info": {
                "username": user.username,
                "email": user.email,
                "role": user.role.value
            }
        })
    return result

@app.get("/sessions/{session_id}/tickets")
async def get_tickets_for_session(session_id: int, db: Session = Depends(get_db)):
    """Получить билеты для конкретного сеанса"""
    tickets = db.query(Ticket).filter(Ticket.session_id == session_id).all()
    return [{
        "id": ticket.id,
        "seat_number": ticket.seat_number,
        "user_id": ticket.user_id,
        "price": float(ticket.price),
        "status": ticket.status,
        "is_paid": ticket.is_paid
    } for ticket in tickets]

@app.post("/admin/update_seat_rows")
async def update_seat_rows(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Обновить seat_row для всех существующих билетов"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    try:
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    except:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    username = token.replace("demo_token_", "")
    user = db.query(User).filter(User.username == username).first()
    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    tickets = db.query(Ticket).all()
    updated_count = 0
    for ticket in tickets:
        session = db.query(Session).filter(Session.id == ticket.session_id).first()
        if session:
            hall = db.query(Hall).filter(Hall.id == session.hall_id).first()
            if hall:
                seats_per_row = hall.seats_per_row if hall.seats_per_row else 10
                new_row = ((ticket.seat_number - 1) // seats_per_row) + 1
                if ticket.seat_row != new_row:
                    ticket.seat_row = new_row
                    updated_count += 1
    db.commit()
    return {
        "message": "Обновление seat_row завершено",
        "updated_tickets": updated_count
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 