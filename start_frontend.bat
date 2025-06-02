@echo off
echo 🌐 Запуск фронтенда Cinema API...
echo.
echo Фронтенд будет доступен по адресу: http://localhost:3000
echo API должен быть запущен на: http://localhost:8000
echo.
echo Для остановки нажмите Ctrl+C
echo.

cd frontend
python -m http.server 3000
pause