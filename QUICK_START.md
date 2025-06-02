# 🚀 Быстрый запуск Cinema API

## ⚠️ Решение проблем совместимости

Если у вас возникают ошибки с Python 3.13 и pydantic, используйте автоматическую настройку.

## 🖥️ Windows (Рекомендуемый способ)

### 1. Автоматическая настройка
```cmd
# Запустите из корневой папки проекта
setup.bat
```

### 2. Запуск сервера
```cmd
start.bat
```

## 🐧 Linux/macOS

### 1. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
```

### 2. Установка зависимостей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Запуск сервера
```bash
python run.py
# или
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Доступ к API

После успешного запуска откройте в браузере:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/api/v1/

## 🔧 Ручная установка (если автоматическая не работает)

### Если у вас Python 3.13:
```bash
# Установка совместимых версий
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.5.0
pip install sqlalchemy==2.0.23
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install bcrypt==4.1.2
pip install python-multipart==0.0.6
pip install email-validator==2.1.0
pip install alembic==1.12.1
pip install requests==2.31.0
```

### Если у вас Python 3.8-3.12:
```bash
pip install -r requirements.txt
```

## 🎯 Тестирование API

1. Откройте http://localhost:8000/docs
2. Нажмите "Try it out" на любом endpoint
3. Для защищенных endpoints:
   - Сначала зарегистрируйтесь: `POST /api/v1/auth/register`
   - Затем войдите: `POST /api/v1/auth/login`
   - Скопируйте полученный токен
   - Нажмите "Authorize" и вставьте: `Bearer YOUR_TOKEN`

## ❓ Частые проблемы

### "uvicorn not found"
- Используйте `python -m uvicorn` вместо просто `uvicorn`
- Убедитесь, что активировано виртуальное окружение

### "ForwardRef._evaluate() error"
- Обновите до pydantic 2.x: `pip install pydantic==2.5.0`
- Или используйте Python 3.11 вместо 3.13

### "Module not found"
- Убедитесь, что находитесь в корневой папке проекта
- Активируйте виртуальное окружение

## 🆘 Если ничего не помогает

Используйте Docker:
```bash
docker-compose up -d --build
```

API будет доступен на том же адресе: http://localhost:8000/docs 