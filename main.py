from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Импортируем только основные роутеры без сложных зависимостей
try:
    from app.database import engine
    from app import models
    from app.routers import auth, movies, sessions, tickets, cinemas, reviews
    
    # Создание таблиц в базе данных
    models.Base.metadata.create_all(bind=engine)
    FULL_VERSION = True
except ImportError as e:
    print(f"⚠️ Некоторые модули недоступны: {e}")
    print("Запускаем в упрощенном режиме...")
    FULL_VERSION = False

app = FastAPI(
    title="Cinema API",
    description="""
    API для управления кинотеатром с полной функциональностью:
    
    ## 🎬 Возможности
    
    * **Аутентификация**: Регистрация и авторизация пользователей с JWT токенами
    * **Фильмы**: Полное управление каталогом фильмов
    * **Кинотеатры и залы**: Управление сетью кинотеатров и их залами
    * **Сеансы**: Планирование и управление киносеансами
    * **Билеты**: Система бронирования билетов с контролем мест
    * **Отзывы**: Система отзывов и рейтингов фильмов
    * **Геолокация**: Поиск кинотеатров рядом
    
    ## 🔐 Аутентификация
    
    Для доступа к защищенным эндпоинтам используйте Bearer токен:
    1. Зарегистрируйтесь через `/auth/register`
    2. Войдите через `/auth/login` и получите токен
    3. Используйте токен в заголовке: `Authorization: Bearer <your_token>`
    """,
    version="2.0.0",
    contact={
        "name": "Cinema API Support",
        "email": "support@cinema.example.com",
    }
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FULL_VERSION:
    # Подключение роутеров полной версии
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["🔐 Аутентификация"])
    app.include_router(movies.router, prefix="/api/v1/movies", tags=["🎬 Фильмы"])
    app.include_router(cinemas.router, prefix="/api/v1/cinemas", tags=["🏢 Кинотеатры"])
    app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["🎭 Сеансы"])
    app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["🎫 Билеты"])
    app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["⭐ Отзывы"])
else:
    # Упрощенные endpoints для демонстрации
    @app.get("/api/v1/movies", tags=["🎬 Фильмы"])
    async def get_movies():
        """Демо-список фильмов"""
        return {
            "movies": [
                {
                    "id": 1,
                    "title": "Интерстеллар",
                    "genre": "sci_fi",
                    "duration_minutes": 169,
                    "rating": 8.6,
                    "description": "Научно-фантастический фильм о путешествиях через пространство и время"
                },
                {
                    "id": 2,
                    "title": "Темный рыцарь",
                    "genre": "action",
                    "duration_minutes": 152,
                    "rating": 9.0,
                    "description": "Супергеройский фильм о Бэтмене"
                },
                {
                    "id": 3,
                    "title": "Паразиты",
                    "genre": "thriller",
                    "duration_minutes": 132,
                    "rating": 8.5,
                    "description": "Южнокорейский социальный триллер"
                }
            ],
            "total": 3,
            "mode": "demo"
        }
    
    @app.get("/api/v1/sessions", tags=["🎭 Сеансы"])
    async def get_sessions():
        """Демо-список сеансов"""
        return {
            "sessions": [
                {
                    "id": 1,
                    "movie_id": 1,
                    "movie_title": "Интерстеллар",
                    "start_time": "2024-12-21T20:00:00",
                    "hall": "Зал 1",
                    "base_price": 500.0,
                    "available_seats": 120
                },
                {
                    "id": 2,
                    "movie_id": 2,
                    "movie_title": "Темный рыцарь",
                    "start_time": "2024-12-21T22:30:00",
                    "hall": "Зал 2",
                    "base_price": 600.0,
                    "available_seats": 85
                }
            ],
            "total": 2,
            "mode": "demo"
        }

@app.get("/", include_in_schema=False)
async def root():
    """Перенаправление на документацию Swagger"""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["🚦 Система"])
async def health_check():
    """Проверка работоспособности сервиса"""
    return {
        "status": "healthy",
        "message": "Cinema API работает корректно",
        "version": "2.0.0",
        "environment": "development",
        "full_version": FULL_VERSION,
        "features": [
            "✅ FastAPI работает",
            "✅ Swagger UI доступен",
            "✅ REST API функционирует",
            "✅ CORS настроен",
            f"{'✅' if FULL_VERSION else '⚠️'} База данных {'подключена' if FULL_VERSION else 'в демо-режиме'}",
            f"{'✅' if FULL_VERSION else '⚠️'} Аутентификация {'активна' if FULL_VERSION else 'недоступна'}"
        ]
    }

@app.get("/api/info", tags=["🚦 Система"])
async def api_info():
    """Информация об API"""
    return {
        "name": "Cinema API",
        "version": "2.0.0",
        "description": "Полнофункциональный API для управления кинотеатром",
        "mode": "full" if FULL_VERSION else "demo",
        "endpoints_count": len(app.routes),
        "database": "SQLite" if FULL_VERSION else "In-Memory Demo",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    print("🎬 Cinema API - Запуск")
    print("=" * 40)
    print(f"Режим: {'Полная версия' if FULL_VERSION else 'Демо-версия'}")
    print("🌐 Сервер будет доступен по адресам:")
    print("• Swagger UI: http://localhost:8000/docs")
    print("• ReDoc: http://localhost:8000/redoc")
    print("• API Info: http://localhost:8000/api/info")
    print("• Health: http://localhost:8000/health")
    print("\n⏹️ Для остановки нажмите Ctrl+C\n")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    ) 