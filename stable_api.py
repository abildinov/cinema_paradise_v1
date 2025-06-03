#!/usr/bin/env python3
"""
🎬 Cinema Paradise API - Стабильная версия
Запуск без auto-reload для мобильной разработки
"""

import uvicorn
import sys
import os

# Добавляем текущую директорию в PATH для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎬 Cinema Paradise API - Стабильный режим")
    print("=" * 50)
    print("✅ Без auto-reload")
    print("✅ Игнорирует изменения в mobile/")
    print("✅ Стабильная работа на localhost:8000")
    print("=" * 50)
    
    # Импортируем приложение
    from cinema_api_tortoise import app
    
    # Запускаем без auto-reload
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Отключаем auto-reload
        log_level="info"
    )

if __name__ == "__main__":
    main() 