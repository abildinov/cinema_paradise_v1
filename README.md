# 🎬 Cinema Paradise - Система управления кинотеатром

**Полнофункциональная система управления кинотеатром с REST API и веб-интерфейсом**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-0.25.0-orange)
![React](https://img.shields.io/badge/React-18-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

## 📋 **Описание проекта**

Cinema Paradise - это современная система управления кинотеатром, разработанная для лабораторных работ. Система включает серверную часть на FastAPI с полным REST API и современный веб-интерфейс на React.

### ✨ **Основные возможности**

#### 🎭 **Для посетителей:**
- 📋 Просмотр списка фильмов и сеансов
- 🎟️ Бронирование билетов на сеансы
- 👤 Личный кабинет с историей бронирований
- 🔐 Регистрация и аутентификация

#### 👨‍💼 **Для менеджеров:**
- 📊 Управление фильмами и сеансами
- 🎯 Мониторинг бронирований
- 📈 Базовая статистика

#### 🔧 **Для администраторов:**
- 👥 Управление пользователями
- 🏢 Управление кинотеатрами и залами
- 📊 Полная статистика системы
- ⚙️ Административная панель

## 🏗️ **Архитектура**

### **Backend (FastAPI + Tortoise ORM)**
- **Python 3.13** совместимость
- **7 таблиц БД:** Users, Movies, Cinemas, Halls, Sessions, Tickets, Reviews
- **36+ REST API эндпоинтов**
- **JWT аутентификация** с ролевой системой
- **3 роли:** Customer, Manager, Admin
- **SQLite база данных**

### **Frontend (React SPA)**
- **Современный UI** с темной темой
- **Адаптивный дизайн** (desktop/mobile)
- **Компонентная архитектура**
- **JWT токен аутентификация**

## 🚀 **Быстрый старт**

### **Предварительные требования**
- Python 3.11+ (рекомендуется 3.13)
- pip
- git

### **1. Клонирование репозитория**
```bash
git clone https://github.com/your-username/cinema-paradise.git
cd cinema-paradise
```

### **2. Установка зависимостей**
```bash
pip install -r requirements.txt
```

### **3. Запуск API сервера**
```bash
python cinema_api_tortoise.py
```

API будет доступен по адресу: `http://localhost:8000`

### **4. Запуск веб-интерфейса**
```bash
cd frontend
python -m http.server 3000
```

Веб-интерфейс будет доступен по адресу: `http://localhost:3000`

### **5. Загрузка демо-данных**
Перейдите по адресу: `http://localhost:8000/demo/populate`

## 🔗 **Важные URL**

| Сервис | URL | Описание |
|--------|-----|----------|
| **API Swagger** | `http://localhost:8000/docs` | Интерактивная документация API |
| **ReDoc** | `http://localhost:8000/redoc` | Альтернативная документация API |
| **Веб-приложение** | `http://localhost:3000` | Пользовательский интерфейс |
| **Демо-данные** | `http://localhost:8000/demo/populate` | Загрузка тестовых данных |
| **Health Check** | `http://localhost:8000/health` | Проверка состояния API |

## 👥 **Тестовые аккаунты**

После загрузки демо-данных (`/demo/populate`) доступны следующие аккаунты:

| Роль | Username | Password | Возможности |
|------|----------|----------|-------------|
| **Администратор** | `admin` | `admin123` | Полный доступ ко всем функциям |
| **Тестовый пользователь** | `testuser` | `testpass123` | Бронирование билетов |

## 📊 **Структура базы данных**

### **Основные таблицы:**
- **`users`** - Пользователи системы
- **`movies`** - Информация о фильмах
- **`cinemas`** - Кинотеатры
- **`halls`** - Залы в кинотеатрах
- **`sessions`** - Сеансы фильмов
- **`tickets`** - Забронированные билеты
- **`reviews`** - Отзывы о фильмах

## 🔧 **REST API**

### **Основные группы эндпоинтов:**

#### **🔐 Аутентификация**
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Информация о текущем пользователе

#### **🎬 Фильмы**
- `GET /movies` - Список всех фильмов
- `POST /movies` - Создание нового фильма (Admin/Manager)
- `GET /movies/{id}` - Детали фильма
- `PUT /movies/{id}` - Обновление фильма (Admin/Manager)

#### **📅 Сеансы**
- `GET /sessions` - Список всех сеансов
- `POST /sessions` - Создание нового сеанса (Admin/Manager)
- `GET /sessions/{id}` - Детали сеанса

#### **🎟️ Билеты**
- `GET /tickets/my` - Мои билеты
- `POST /tickets` - Бронирование билета
- `GET /admin/tickets` - Все билеты (Admin)

#### **👥 Администрирование**
- `GET /admin/users` - Список всех пользователей (Admin)
- `GET /admin/stats` - Статистика системы (Admin)

## 📁 **Структура проекта**

```
cinema-paradise/
├── 📄 cinema_api_tortoise.py      # Главный файл API сервера
├── 📄 requirements.txt            # Python зависимости
├── 📁 data/                       # База данных SQLite
│   └── cinema_v2.db
├── 📁 frontend/                   # Веб-интерфейс React
│   ├── 📄 index.html
│   ├── 📁 js/
│   │   ├── 📄 app.js             # Главное React приложение
│   │   ├── 📁 components/         # React компоненты
│   │   └── 📁 services/           # API сервисы
│   └── 📁 css/
│       └── 📄 styles.css         # Стили приложения
├── 📄 view_db.py                 # Утилита для просмотра БД
└── 📚 docs/                      # Документация
    ├── 📄 API_ENDPOINTS.md
    ├── 📄 ARCHITECTURE.md
    └── 📄 DEPLOYMENT.md
```

## 🛠️ **Технологический стек**

### **Backend**
- **FastAPI** - Современный веб-фреймворк для Python
- **Tortoise ORM** - Async ORM для Python (аналог Django ORM)
- **Pydantic** - Валидация данных и сериализация
- **JWT** - JSON Web Tokens для аутентификации
- **SQLite** - Легковесная база данных
- **Uvicorn** - ASGI сервер

### **Frontend**
- **React 18** - JavaScript библиотека для создания UI
- **Vanilla JavaScript** - Без дополнительных фреймворков
- **TailwindCSS** - Utility-first CSS фреймворк
- **Fetch API** - Для HTTP запросов к API

## 🚢 **Развертывание**

### **Docker (рекомендуемый способ)**
```bash
docker-compose up --build
```

### **VPS развертывание**
См. подробную инструкцию в `DEPLOYMENT.md`

## 🧪 **Тестирование API**

Используйте встроенную Swagger документацию:
```
http://localhost:8000/docs
```

Или протестируйте с помощью curl:
```bash
# Получить список фильмов
curl http://localhost:8000/movies

# Регистрация пользователя
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"user@example.com","password":"password123"}'
```

## 🔧 **Разработка**

### **Добавление новых эндпоинтов**
1. Определите Pydantic модели в `cinema_api_tortoise.py`
2. Создайте маршруты FastAPI
3. Добавьте соответствующие функции в frontend

### **Обновление базы данных**
Tortoise ORM автоматически создает схему при запуске. Для сброса БД удалите файл `data/cinema_v2.db`.

## 🐛 **Известные проблемы**

- Требуется Python 3.11+ из-за несовместимости SQLAlchemy 2.0.x с Python 3.13
- PowerShell может требовать специальный синтаксис для команд с `&&`

## 📚 **Дополнительная документация**

- [📖 API Endpoints](API_ENDPOINTS.md) - Полная документация API
- [🏗️ Architecture](ARCHITECTURE.md) - Архитектура системы
- [🚀 Deployment](DEPLOYMENT.md) - Инструкции по развертыванию
- [📋 Project Summary](PROJECT_SUMMARY.md) - Сводка проекта

## 🎯 **Планы развития**

- [ ] **Мобильное приложение** React Native
- [ ] Интеграция платежных систем
- [ ] Система уведомлений
- [ ] Расширенная аналитика
- [ ] Интеграция с внешними кинотеатрами

## 🤝 **Вклад в проект**

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 **Лицензия**

Этот проект создан для образовательных целей в рамках лабораторных работ.

## 👨‍💻 **Автор**

Разработано для изучения современных веб-технологий и создания распределенных систем.

---

**🎬 Cinema Paradise - Ваш билет в мир современных технологий!** 