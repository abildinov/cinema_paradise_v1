#!/usr/bin/env python3
"""
Тестовый запуск Cinema API с минимальными зависимостями
"""

try:
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите зависимости: pip install fastapi uvicorn")
    exit(1)

# Создаем простое приложение FastAPI
app = FastAPI(
    title="Cinema API - Test Version",
    description="Тестовая версия Cinema API для проверки работоспособности",
    version="1.0.0"
)

# Добавляем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    """Перенаправление на документацию"""
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    """Проверка работоспособности"""
    return {
        "status": "healthy",
        "message": "Cinema API работает!",
        "version": "1.0.0",
        "test_mode": True
    }

@app.get("/api/v1/movies")
async def get_movies():
    """Тестовый endpoint для получения фильмов"""
    return {
        "movies": [
            {
                "id": 1,
                "title": "Интерстеллар",
                "genre": "sci_fi",
                "duration_minutes": 169,
                "rating": 8.6
            },
            {
                "id": 2,
                "title": "Темный рыцарь",
                "genre": "action",
                "duration_minutes": 152,
                "rating": 9.0
            }
        ],
        "total": 2
    }

@app.get("/api/v1/test")
async def test_endpoint():
    """Тестовый endpoint"""
    return {
        "message": "Cinema API работает корректно!",
        "features": [
            "✅ FastAPI сервер запущен",
            "✅ Swagger UI доступен",
            "✅ REST API функционирует",
            "✅ CORS настроен"
        ]
    }

if __name__ == "__main__":
    print("🎬 Cinema API - Тестовый запуск")
    print("=" * 40)
    print("🌐 Сервер будет доступен по адресам:")
    print("• Swagger UI: http://localhost:8000/docs")
    print("• ReDoc: http://localhost:8000/redoc")
    print("• Test API: http://localhost:8000/api/v1/test")
    print("• Health: http://localhost:8000/health")
    print("\n⏹️  Для остановки нажмите Ctrl+C\n")
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        print("Попробуйте: python -m uvicorn test_run:app --reload") 