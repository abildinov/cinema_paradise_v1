@echo off
echo 🎬 Cinema Paradise - Запуск системы
echo ====================================
echo.

echo 🔧 Остановка существующих процессов...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3002') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo ✅ Процессы остановлены
echo.

echo 🚀 Запуск API сервера (стабильный режим)...
start "API Server" cmd /c "python stable_api.py"

echo ⏳ Ожидание запуска API сервера...
timeout /t 5 /nobreak >nul

echo 📱 Запуск мобильного приложения...
start "Mobile App" cmd /c "cd mobile_app && python -m http.server 3002"

echo.
echo 🎉 Cinema Paradise запущена!
echo =============================
echo.
echo 📍 Адреса доступа:
echo   🔗 API Server:     http://localhost:8000
echo   📱 Mobile App:     http://localhost:3002
echo   📱 Mobile Network: http://192.168.0.10:3002
echo.
echo 📱 ДЛЯ МОБИЛЬНОГО УСТРОЙСТВА:
echo   1️⃣ Откройте: http://192.168.0.10:3002
echo   2️⃣ Нажмите: "Добавить на главный экран"
echo   3️⃣ Пользуйтесь как нативным приложением!
echo.
echo 💡 Для веб-версии: http://localhost:3000
echo    (запускается отдельно через frontend\start_frontend.bat)
echo.
echo Нажмите любую клавишу для завершения...
pause >nul 