@echo off
echo ============================================
echo 🎬 Cinema API - Автоматическая настройка
echo ============================================

echo.
echo 🔍 Проверка Python...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python не найден! Установите Python 3.8+ с официального сайта.
    pause
    exit /b 1
)

echo.
echo 📦 Создание виртуального окружения...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo ❌ Ошибка создания виртуального окружения
    pause
    exit /b 1
)

echo.
echo 🔌 Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo 📥 Обновление pip...
python -m pip install --upgrade pip

echo.
echo 📚 Установка зависимостей...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo.
echo ✅ Настройка завершена успешно!
echo.
echo 🚀 Для запуска сервера выполните:
echo    start.bat
echo.
echo 🌐 После запуска откройте в браузере:
echo    http://localhost:8000/docs
echo.

pause 