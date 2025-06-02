@echo off
echo ========================================
echo 🎬 Cinema API - Запуск сервера
echo ========================================

echo.
echo 🔌 Активация виртуального окружения...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Виртуальное окружение не найдено.
    echo 📥 Запустите setup.bat для первоначальной настройки.
    pause
    exit /b 1
)

echo.
echo 🌐 Сервер будет доступен по адресам:
echo • Swagger UI: http://localhost:8000/docs
echo • ReDoc: http://localhost:8000/redoc  
echo • API: http://localhost:8000/api/v1/
echo.
echo ⏹️  Для остановки нажмите Ctrl+C
echo.

echo 🚀 Запуск Cinema API сервера...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause 