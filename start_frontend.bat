@echo off
echo 🌐 Запуск фронтенда Cinema Paradise...
echo ======================================
echo.
echo ✅ Полная веб-версия Cinema Paradise
echo 📍 Адрес: http://localhost:3000  
echo 🔗 API: http://localhost:8000
echo.
echo 💡 Убедитесь что API сервер запущен!
echo    python stable_api.py
echo.
echo Для остановки нажмите Ctrl+C
echo.

cd frontend
python -m http.server 3000