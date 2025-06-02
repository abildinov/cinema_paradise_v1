# Cinema API - Полная документация endpoints

## 📋 Обзор API

Cinema API предоставляет 32 REST endpoint'а для полного управления кинотеатром. Все endpoint'ы следуют стандартам OpenAPI 3.0 и автоматически документируются через Swagger UI.

**Base URL**: `http://localhost:8000/api/v1`  
**Swagger UI**: `http://localhost:8000/docs`  
**ReDoc**: `http://localhost:8000/redoc`

## 🔐 Аутентификация (4 endpoint'а)

### 1. POST `/auth/register`
**Описание**: Регистрация нового пользователя  
**Авторизация**: Не требуется  
**Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+7900123456"
}
```
**Response**: `UserResponse`

### 2. POST `/auth/login`
**Описание**: Авторизация и получение JWT токена  
**Авторизация**: Не требуется  
**Body**: OAuth2 form data (username, password)  
**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": { "id": 1, "username": "john_doe", ... }
}
```

### 3. GET `/auth/me`
**Описание**: Получение профиля текущего пользователя  
**Авторизация**: Bearer token  
**Response**: `UserResponse`

### 4. GET `/auth/users`
**Описание**: Список пользователей (только для администраторов)  
**Авторизация**: Bearer token (роль ADMIN)  
**Parameters**: `skip: int = 0`, `limit: int = 100`  
**Response**: `List[UserResponse]`

## 🎬 Фильмы (6 endpoint'ов)

### 5. GET `/movies`
**Описание**: Список фильмов с фильтрацией и пагинацией  
**Авторизация**: Не требуется  
**Parameters**:
- `skip: int = 0` - Пропустить записи
- `limit: int = 100` - Лимит записей
- `genre: str = None` - Фильтр по жанру
- `year: int = None` - Фильтр по году
- `is_active: bool = True` - Только активные фильмы
- `search: str = None` - Поиск по названию

**Response**: `MovieList`

### 6. POST `/movies`
**Описание**: Создание нового фильма  
**Авторизация**: Bearer token (роль ADMIN/MANAGER)  
**Body**: `MovieCreate`
```json
{
  "title": "Интерстеллар",
  "description": "Научно-фантастический фильм о путешествиях через червоточины",
  "duration_minutes": 169,
  "genre": "sci_fi",
  "director": "Кристофер Нолан",
  "release_year": 2014,
  "rating": 8.6,
  "poster_url": "https://example.com/poster.jpg"
}
```

### 7. GET `/movies/{movie_id}`
**Описание**: Получение фильма по ID  
**Авторизация**: Не требуется  
**Path Parameters**: `movie_id: int`  
**Response**: `Movie`

### 8. PUT `/movies/{movie_id}`
**Описание**: Обновление фильма  
**Авторизация**: Bearer token (роль ADMIN/MANAGER)  
**Path Parameters**: `movie_id: int`  
**Body**: `MovieUpdate`

### 9. DELETE `/movies/{movie_id}`
**Описание**: Удаление фильма  
**Авторизация**: Bearer token (роль ADMIN)  
**Path Parameters**: `movie_id: int`

### 10. GET `/movies/{movie_id}/sessions`
**Описание**: Сеансы конкретного фильма  
**Авторизация**: Не требуется  
**Path Parameters**: `movie_id: int`  
**Response**: `List[Session]`

## 🏢 Кинотеатры (6 endpoint'ов)

### 11. GET `/cinemas`
**Описание**: Список кинотеатров  
**Авторизация**: Не требуется  
**Parameters**:
- `skip: int = 0`
- `limit: int = 100`
- `city: str = None` - Фильтр по городу
- `is_active: bool = True`

### 12. POST `/cinemas`
**Описание**: Создание кинотеатра  
**Авторизация**: Bearer token (роль ADMIN)  
**Body**: `CinemaCreate`

### 13. GET `/cinemas/{cinema_id}`
**Описание**: Получение кинотеатра по ID  
**Авторизация**: Не требуется  
**Path Parameters**: `cinema_id: int`

### 14. GET `/cinemas/{cinema_id}/halls`
**Описание**: Залы кинотеатра  
**Авторизация**: Не требуется  
**Path Parameters**: `cinema_id: int`

### 15. POST `/cinemas/{cinema_id}/halls`
**Описание**: Создание зала в кинотеатре  
**Авторизация**: Bearer token (роль ADMIN/MANAGER)  
**Path Parameters**: `cinema_id: int`  
**Body**: `HallCreate`

### 16. GET `/cinemas/search`
**Описание**: Поиск кинотеатров по геолокации  
**Авторизация**: Не требуется  
**Parameters**:
- `latitude: float`
- `longitude: float` 
- `radius: float = 10.0` - Радиус поиска в км

## 🎭 Сеансы (6 endpoint'ов)

### 17. GET `/sessions`
**Описание**: Список сеансов с фильтрацией  
**Авторизация**: Не требуется  
**Parameters**:
- `skip: int = 0`
- `limit: int = 100`
- `movie_id: int = None`
- `hall_id: int = None`
- `date: date = None` - Дата сеанса
- `is_active: bool = True`

### 18. POST `/sessions`
**Описание**: Создание сеанса  
**Авторизация**: Bearer token (роль ADMIN/MANAGER)  
**Body**: `SessionCreate`
```json
{
  "movie_id": 1,
  "hall_id": 1,
  "start_time": "2024-12-21T20:00:00",
  "end_time": "2024-12-21T22:49:00",
  "base_price": 500.0,
  "language": "ru",
  "subtitles": "en",
  "format_3d": false,
  "format_imax": true
}
```

### 19. GET `/sessions/{session_id}`
**Описание**: Получение сеанса по ID  
**Авторизация**: Не требуется  
**Path Parameters**: `session_id: int`

### 20. PUT `/sessions/{session_id}`
**Описание**: Обновление сеанса  
**Авторизация**: Bearer token (роль ADMIN/MANAGER)  
**Path Parameters**: `session_id: int`  
**Body**: `SessionUpdate`

### 21. DELETE `/sessions/{session_id}`
**Описание**: Удаление сеанса  
**Авторизация**: Bearer token (роль ADMIN)  
**Path Parameters**: `session_id: int`

### 22. GET `/sessions/{session_id}/available-seats`
**Описание**: Доступные места на сеанс  
**Авторизация**: Не требуется  
**Path Parameters**: `session_id: int`  
**Response**: Схема зала с доступными местами

## 🎫 Билеты (7 endpoint'ов)

### 23. POST `/tickets`
**Описание**: Бронирование билета  
**Авторизация**: Bearer token  
**Body**: `TicketCreate`
```json
{
  "session_id": 1,
  "seat_row": 5,
  "seat_number": 12,
  "seat_type": "standard",
  "price": 500.0
}
```
**Response**: Билет с QR-кодом

### 24. GET `/tickets`
**Описание**: Список билетов с фильтрацией  
**Авторизация**: Bearer token  
**Parameters**:
- `skip: int = 0`
- `limit: int = 100`
- `user_id: int = None` (только для админов)
- `session_id: int = None`
- `status: str = None`

### 25. GET `/tickets/{ticket_id}`
**Описание**: Получение билета по ID  
**Авторизация**: Bearer token (владелец или админ)  
**Path Parameters**: `ticket_id: int`

### 26. PUT `/tickets/{ticket_id}`
**Описание**: Обновление билета  
**Авторизация**: Bearer token (владелец или админ)  
**Path Parameters**: `ticket_id: int`  
**Body**: `TicketUpdate`

### 27. DELETE `/tickets/{ticket_id}`
**Описание**: Отмена бронирования  
**Авторизация**: Bearer token (владелец или админ)  
**Path Parameters**: `ticket_id: int`

### 28. PATCH `/tickets/{ticket_id}/pay`
**Описание**: Оплата билета  
**Авторизация**: Bearer token (владелец)  
**Path Parameters**: `ticket_id: int`  
**Body**:
```json
{
  "payment_method": "card",
  "card_token": "tok_visa_1234"
}
```

### 29. GET `/tickets/statistics`
**Описание**: Статистика по билетам  
**Авторизация**: Bearer token (роль MANAGER/ADMIN)  
**Parameters**:
- `start_date: date`
- `end_date: date`
- `cinema_id: int = None`

## ⭐ Отзывы (7 endpoint'ов)

### 30. POST `/reviews`
**Описание**: Создание отзыва о фильме  
**Авторизация**: Bearer token  
**Body**: `ReviewCreate`
```json
{
  "movie_id": 1,
  "rating": 9,
  "title": "Отличный фильм!",
  "content": "Великолепная работа режиссера и актеров...",
  "is_spoiler": false
}
```

### 31. GET `/reviews/movie/{movie_id}`
**Описание**: Отзывы о конкретном фильме  
**Авторизация**: Не требуется  
**Path Parameters**: `movie_id: int`  
**Parameters**:
- `skip: int = 0`
- `limit: int = 100`
- `rating: int = None` - Фильтр по рейтингу
- `is_approved: bool = True`

### 32. GET `/reviews/{review_id}`
**Описание**: Получение отзыва по ID  
**Авторизация**: Не требуется  
**Path Parameters**: `review_id: int`

### 33. PUT `/reviews/{review_id}`
**Описание**: Обновление отзыва  
**Авторизация**: Bearer token (автор или админ)  
**Path Parameters**: `review_id: int`  
**Body**: `ReviewUpdate`

### 34. DELETE `/reviews/{review_id}`
**Описание**: Удаление отзыва  
**Авторизация**: Bearer token (автор или админ)  
**Path Parameters**: `review_id: int`

### 35. POST `/reviews/{review_id}/vote`
**Описание**: Голосование за полезность отзыва  
**Авторизация**: Bearer token  
**Path Parameters**: `review_id: int`  
**Body**:
```json
{
  "vote_type": "helpful"  // or "unhelpful"
}
```

### 36. GET `/reviews/user/my-reviews`
**Описание**: Мои отзывы  
**Авторизация**: Bearer token  
**Parameters**: `skip: int = 0`, `limit: int = 100`

## 🔍 Дополнительные endpoint'ы

### Health Check
- `GET /health` - Проверка состояния API

### OpenAPI Documentation
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /openapi.json` - OpenAPI спецификация

## 📊 Модели данных

### Основные модели Pydantic:

1. **User / UserCreate / UserResponse** - Пользователи
2. **Movie / MovieCreate / MovieUpdate** - Фильмы  
3. **Cinema / CinemaCreate** - Кинотеатры
4. **Hall / HallCreate** - Залы
5. **Session / SessionCreate / SessionUpdate** - Сеансы
6. **Ticket / TicketCreate / TicketUpdate** - Билеты
7. **Review / ReviewCreate / ReviewUpdate** - Отзывы

### Стандартные HTTP статус коды:

- `200` - Успешный запрос
- `201` - Ресурс создан
- `400` - Ошибка валидации
- `401` - Не авторизован
- `403` - Доступ запрещен
- `404` - Ресурс не найден
- `422` - Ошибка обработки данных
- `500` - Внутренняя ошибка сервера

## 🔐 Система авторизации

### Роли пользователей:
- **CUSTOMER** - Обычный клиент (бронирование, отзывы)
- **MANAGER** - Менеджер (управление сеансами, просмотр статистики)
- **ADMIN** - Администратор (полный доступ)

### Аутентификация:
- JWT токены в заголовке `Authorization: Bearer <token>`
- Время жизни токена: 30 минут
- Алгоритм: HS256

## 📝 Примеры использования

### Полный цикл бронирования билета:

```bash
# 1. Регистрация пользователя
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com", 
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# 2. Авторизация
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=password123"

# 3. Получение списка фильмов
curl -X GET "http://localhost:8000/api/v1/movies" \
  -H "Authorization: Bearer <token>"

# 4. Получение сеансов фильма
curl -X GET "http://localhost:8000/api/v1/movies/1/sessions" \
  -H "Authorization: Bearer <token>"

# 5. Бронирование билета
curl -X POST "http://localhost:8000/api/v1/tickets" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "seat_row": 5,
    "seat_number": 12,
    "seat_type": "standard",
    "price": 500.0
  }'

# 6. Оплата билета
curl -X PATCH "http://localhost:8000/api/v1/tickets/1/pay" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "card"
  }'
```

## 🎯 Итоги

✅ **36 REST endpoint'ов** с полной OpenAPI документацией  
✅ **7 основных таблиц** с богатой структурой данных  
✅ **JWT аутентификация** с ролевой моделью доступа  
✅ **Валидация данных** через Pydantic схемы  
✅ **Swagger UI** для интерактивного тестирования  
✅ **Готовность к развертыванию** на VPS  

API полностью готов для использования в production среде с возможностью масштабирования и расширения функциональности. 