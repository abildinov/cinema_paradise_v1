@echo off
echo 📱 Запуск мобильного приложения Cinema Paradise [БЕЗ КЭША]
echo ===============================================
echo.

echo 🎯 Что такое это приложение:
echo • 📱 Progressive Web App (PWA)
echo • 🔄 Работает офлайн
echo • 📥 Устанавливается как нативное приложение
echo • 🔔 Push-уведомления
echo • 🎬 Полная интеграция с Cinema Paradise API
echo • 🚀 БЕЗ КЭШИРОВАНИЯ - всегда свежая версия!
echo.

REM Проверяем API сервер
echo 🔍 Проверка API сервера...
netstat -an | findstr :8000 >nul
if %errorlevel%==0 (
    echo ✅ API сервер работает на порту 8000
) else (
    echo ❌ API сервер не запущен!
    echo 💡 Запустите сначала: python stable_api.py
    echo.
    pause
    exit /b 1
)

echo.
echo 📱 Запуск мобильного приложения на порту 3002...
echo.
echo 📍 Адреса для доступа:
echo   • 📱 Мобильное приложение: http://localhost:3002
echo   • 📱 Для телефона: http://192.168.0.10:3002
echo   • 🌐 Полная веб-версия: http://localhost:3000
echo   • 🔗 API: http://localhost:8000
echo.
echo 💡 Инструкции по установке:
echo   1️⃣ Откройте приложение в браузере телефона
echo   2️⃣ Нажмите "Добавить на главный экран" или "Установить приложение"
echo   3️⃣ Приложение появится как нативное на рабочем столе
echo.
echo 🚀 НОВИНКА: Сервер без кэширования!
echo ✅ Все изменения видны сразу
echo ✅ Никаких проблем с обновлением
echo.
echo Для остановки нажмите Ctrl+C
echo.

cd mobile_app
python server.py

pause 