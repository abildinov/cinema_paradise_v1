# ОТЧЕТ
## по лабораторной работе
### "Разработка REST API для системы управления кинотеатром"

---

**Выполнил:** [Ваше имя]  
**Группа:** [Ваша группа]  
**Дисциплина:** Методы объектно-ориентированного программирования  
**Дата:** Июнь 2025

---

## Цель работы

Выбрать любую предметную область (банкинг, доставка и т.д.) и описать архитектуру верхнего уровня разрабатываемого распределенного сервиса (UML).

Привести ER-диаграмму БД и спецификацию REST API в формате OpenAPI v3.

## Ход Работы

Темой разрабатываемого сервиса стал **«Кинотеатр Cinema Paradise»**.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               CINEMA PARADISE                                   │
│                          UML Component Diagram                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      User       │    │     Movie       │    │     Cinema      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ +user_id        │    │ +movie_id       │    │ +cinema_id      │
│ +username       │    │ +title          │    │ +name           │
│ +email          │    │ +duration       │    │ +address        │
│ +role           │    │ +genre          │    │ +city           │
│ +first_name     │    │ +director       │    │ +phone          │
│ +last_name      │    │ +rating         │    │ +halls[]        │
│ +phone          │    │ +poster_url     │    │ +is_active      │
│ +loyalty_points │    │ +is_active      │    │ +created_at     │
│ +created_at     │    │ +created_at     │    │ +updated_at     │
│ +updated_at     │    │ +updated_at     │    └─────────────────┘
└─────────────────┘    └─────────────────┘              │
        │                       │                       │
        │                       │                ┌─────────────────┐
        │                ┌─────────────────┐     │      Hall       │
        │                │    Session      │     ├─────────────────┤
        │                ├─────────────────┤     │ +hall_id        │
        │                │ +session_id     │◄────│ +cinema_id      │
        │                │ +movie_id       │     │ +name           │
        │                │ +hall_id        │     │ +total_seats    │
        │                │ +start_time     │     │ +rows           │
        │                │ +end_time       │     │ +screen_type    │
        │                │ +date           │     │ +sound_system   │
        │                │ +base_price     │     │ +is_active      │
        │                │ +available_seats│     │ +created_at     │
        │                │ +is_active      │     │ +updated_at     │
        │                │ +created_at     │     └─────────────────┘
        │                │ +updated_at     │
        │                └─────────────────┘
        │                        │
        │                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Ticket      │    │     Review      │    │     Payment     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ +ticket_id      │    │ +review_id      │    │ +payment_id     │
│ +session_id     │◄───│ +movie_id       │    │ +user_id        │
│ +user_id        │    │ +user_id        │    │ +ticket_id      │
│ +seat_row       │    │ +rating         │    │ +amount         │
│ +seat_number    │    │ +title          │    │ +payment_method │
│ +price          │    │ +content        │    │ +status         │
│ +booking_ref    │    │ +is_spoiler     │    │ +payment_date   │
│ +status         │    │ +helpful_votes  │    │ +created_at     │
│ +is_paid        │    │ +is_approved    │    │ +updated_at     │
│ +booking_time   │    │ +created_at     │    └─────────────────┘
│ +created_at     │    │ +updated_at     │
└─────────────────┘    └─────────────────┘
```

**Рисунок 1 – UML-диаграмма**

### Объяснение основных компонентов:

**1. User (Пользователь)**
• Основной класс для всех пользователей системы
• Содержит базовую информацию о пользователе
• Имеет связи с билетами, отзывами и платежами

**2. Movie (Фильм)**
• Представляет фильмы в каталоге
• Содержит информацию о названии, режиссере, жанре и рейтинге
• Связан с сеансами и отзывами

**3. Cinema (Кинотеатр)**
• Управляет информацией о кинотеатрах
• Содержит адрес, контакты и список залов
• Связан с залами

**4. Hall (Зал)**
• Представляет залы в кинотеатрах
• Содержит информацию о вместимости, типе экрана и звуковой системе
• Связан с сеансами

**5. Session (Сеанс)**
• Управляет сеансами фильмов
• Связан с конкретным фильмом и залом
• Содержит расписание и ценовую информацию

**6. Ticket (Билет)**
• Управляет бронированием билетов
• Связан с пользователем и сеансом
• Отслеживает статус бронирования

**7. Review (Отзыв)**
• Управляет отзывами о фильмах
• Связан с пользователем и фильмом
• Содержит рейтинг и текст отзыва

**8. Payment (Платеж)**
• Управляет платежами за билеты
• Содержит информацию о способах оплаты и статусах
• Связан с пользователем и билетами

### Основные связи:

• Один пользователь может иметь множество билетов
• Один пользователь может оставить множество отзывов
• Один фильм может иметь множество сеансов
• Один сеанс может иметь множество билетов
• Один кинотеатр может иметь множество залов
• Один пользователь может иметь множество платежей

---

## ER-диаграмма базы данных

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CINEMA PARADISE DATABASE                             │
│                                         ER-DIAGRAM                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────┐          ┌────────────────────────────────────┐
│               USERS                │          │              MOVIES                │
├────────────────────────────────────┤          ├────────────────────────────────────┤
│ PK  id: INTEGER                    │          │ PK  id: INTEGER                    │
│ UK  username: VARCHAR(50)          │          │     title: VARCHAR(255)            │
│ UK  email: VARCHAR(255)            │          │     original_title: VARCHAR(255)   │
│     hashed_password: VARCHAR(255)  │          │     description: TEXT              │
│     first_name: VARCHAR(100)       │          │     synopsis: TEXT                 │
│     last_name: VARCHAR(100)        │          │     duration_minutes: INTEGER      │
│     phone: VARCHAR(20)             │          │     genre: ENUM(MovieGenre)        │
│     date_of_birth: DATETIME        │          │     director: VARCHAR(255)         │
│     role: ENUM(UserRole)           │          │     producer: VARCHAR(255)         │
│     is_active: BOOLEAN             │          │     writer: VARCHAR(255)           │
│     is_verified: BOOLEAN           │          │     cast: TEXT                     │
│     avatar_url: VARCHAR(500)       │          │     release_year: INTEGER          │
│     address: TEXT                  │          │     release_date: DATETIME         │
│     city: VARCHAR(100)             │          │     country: VARCHAR(100)          │
│     postal_code: VARCHAR(20)       │          │     language: VARCHAR(50)          │
│     loyalty_points: INTEGER        │          │     age_rating: VARCHAR(10)        │
│     total_spent: DECIMAL(10,2)     │          │     rating: FLOAT                  │
│     created_at: DATETIME           │          │     imdb_rating: FLOAT             │
│     updated_at: DATETIME           │          │     budget: DECIMAL(15,2)          │
│     last_login: DATETIME           │          │     box_office: DECIMAL(15,2)      │
└────────────────────────────────────┘          │     poster_url: VARCHAR(500)       │
                │                               │     trailer_url: VARCHAR(500)      │
                │                               │     backdrop_url: VARCHAR(500)     │
                │                               │     is_active: BOOLEAN             │
                │                               │     is_featured: BOOLEAN           │
                │                               │     awards: TEXT                   │
                │                               │     tags: TEXT                     │
                │                               │     created_at: DATETIME           │
                │                               │     updated_at: DATETIME           │
                │                               └────────────────────────────────────┘
                │                                              │
                │                                              │
                │                                              │
┌────────────────────────────────────┐          ┌────────────────────────────────────┐
│             TICKETS                │          │             SESSIONS               │
├────────────────────────────────────┤          ├────────────────────────────────────┤
│ PK  id: INTEGER                    │          │ PK  id: INTEGER                    │
│ FK  session_id: INTEGER            │────────  │ FK  movie_id: INTEGER              │──────┘
│ FK  user_id: INTEGER               │──────────│ FK  hall_id: INTEGER               │
│     seat_row: INTEGER              │          │     start_time: DATETIME           │
│     seat_number: INTEGER           │          │     end_time: DATETIME             │
│     seat_type: VARCHAR(20)         │          │     date: DATETIME                 │
│     price: DECIMAL(8,2)            │          │     base_price: DECIMAL(8,2)       │
│     discount_applied: DECIMAL(8,2) │          │     vip_price: DECIMAL(8,2)        │
│     final_price: DECIMAL(8,2)      │          │     premium_price: DECIMAL(8,2)    │
│ UK  booking_reference: VARCHAR(20) │          │     available_seats: INTEGER       │
│     status: VARCHAR(20)            │          │     sold_tickets: INTEGER          │
│     payment_method: VARCHAR(50)    │          │     reserved_tickets: INTEGER      │
│     payment_transaction_id: VARCHAR│          │     is_active: BOOLEAN             │
│     qr_code: VARCHAR(500)          │          │     is_sold_out: BOOLEAN           │
│     is_paid: BOOLEAN               │          │     language: VARCHAR(50)          │
│     booking_time: DATETIME         │          │     subtitles: VARCHAR(50)         │
│     payment_time: DATETIME         │          │     format_3d: BOOLEAN             │
│     cancellation_time: DATETIME    │          │     format_imax: BOOLEAN           │
│     used_time: DATETIME            │          │     early_bird_discount: FLOAT     │
│     created_at: DATETIME           │          │     late_show_surcharge: FLOAT     │
└────────────────────────────────────┘          │     created_at: DATETIME           │
                                                │     updated_at: DATETIME           │
                                                └────────────────────────────────────┘
                                                               │
                                                               │
                                                               │
┌────────────────────────────────────┐          ┌────────────────────────────────────┐
│             REVIEWS                │          │               HALLS                │
├────────────────────────────────────┤          ├────────────────────────────────────┤
│ PK  id: INTEGER                    │          │ PK  id: INTEGER                    │
│ FK  movie_id: INTEGER              │──────────│ FK  cinema_id: INTEGER             │
│ FK  user_id: INTEGER               │          │     name: VARCHAR(100)             │
│     rating: INTEGER (1-10)         │          │     hall_number: INTEGER           │
│     title: VARCHAR(255)            │          │     total_seats: INTEGER           │
│     content: TEXT                  │          │     rows: INTEGER                  │
│     is_spoiler: BOOLEAN            │          │     seats_per_row: INTEGER         │
│     is_verified_purchase: BOOLEAN  │          │     screen_type: VARCHAR(50)       │
│     helpful_votes: INTEGER         │          │     sound_system: VARCHAR(50)      │
│     unhelpful_votes: INTEGER       │          │     accessibility: BOOLEAN         │
│     is_approved: BOOLEAN           │          │     vip_seats: INTEGER             │
│     created_at: DATETIME           │          │     premium_seats: INTEGER         │
│     updated_at: DATETIME           │          │     standard_seats: INTEGER        │
└────────────────────────────────────┘          │     seat_map: TEXT                 │
                │                               │     is_active: BOOLEAN             │
                └───────────────────────────────│     created_at: DATETIME           │
                                                │     updated_at: DATETIME           │
                                                └────────────────────────────────────┘
                                                               │
                                                               │
                                                               │
                                                ┌────────────────────────────────────┐
                                                │             CINEMAS                │
                                                ├────────────────────────────────────┤
                                                │ PK  id: INTEGER                    │
                                                │     name: VARCHAR(255)             │
                                                │     address: TEXT                  │
                                                │     city: VARCHAR(100)             │
                                                │     postal_code: VARCHAR(20)       │
                                                │     phone: VARCHAR(20)             │
                                                │     email: VARCHAR(255)            │
                                                │     website: VARCHAR(500)          │
                                                │     latitude: FLOAT                │
                                                │     longitude: FLOAT               │
                                                │     opening_time: TIME             │
                                                │     closing_time: TIME             │
                                                │     facilities: TEXT               │
                                                │     parking_available: BOOLEAN     │
                                                │     is_active: BOOLEAN             │
                                                │     created_at: DATETIME           │
                                                │     updated_at: DATETIME           │
                                                └────────────────────────────────────┘
```

**Рисунок 2 – ER-диаграмма**

Ниже приведена спецификация REST API в формате OpenAPI v3, а также список основных эндпоинтов.

---

## REST API Спецификация (OpenAPI v3.0)

```yaml
openapi: 3.0.0
info:
  title: Cinema Paradise API
  description: API для системы управления кинотеатром
  version: 2.0.0
  contact:
    name: API Support
    email: support@cinemaparadise.com

servers:
  - url: http://localhost:8000/api
    description: Локальный сервер разработки

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        user_id:
          type: string
          format: uuid
        username:
          type: string
          format: string
        email:
          type: string
          format: email
        first_name:
          type: string
        last_name:
          type: string
        phone:
          type: string
        role:
          type: string
          enum: [customer, manager, admin]
        loyalty_points:
          type: integer
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Movie:
      type: object
      properties:
        movie_id:
          type: string
          format: uuid
        title:
          type: string
        description:
          type: string
        duration_minutes:
          type: integer
          description: Длительность в минутах
        genre:
          type: string
          enum: [action, comedy, drama, horror, romance, sci_fi, thriller]
        director:
          type: string
        rating:
          type: number
          format: float
        poster_url:
          type: string
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time

    Session:
      type: object
      properties:
        session_id:
          type: string
          format: uuid
        movie_id:
          type: string
          format: uuid
        hall_id:
          type: string
          format: uuid
        start_time:
          type: string
          format: date-time
        end_time:
          type: string
          format: date-time
        base_price:
          type: number
          format: decimal
        available_seats:
          type: integer
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time

    Ticket:
      type: object
      properties:
        ticket_id:
          type: string
          format: uuid
        session_id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        seat_row:
          type: integer
        seat_number:
          type: integer
        price:
          type: number
          format: decimal
        booking_reference:
          type: string
        status:
          type: string
          enum: [reserved, confirmed, cancelled]
        is_paid:
          type: boolean
        booking_time:
          type: string
          format: date-time

paths:
  /auth/register:
    post:
      summary: Регистрация нового пользователя
      tags: [Авторизация]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - username
                - email
                - password
                - first_name
                - last_name
              properties:
                username:
                  type: string
                email:
                  type: string
                  format: email
                password:
                  type: string
                  format: password
                first_name:
                  type: string
                last_name:
                  type: string
                phone:
                  type: string
      responses:
        '201':
          description: Пользователь успешно создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Неверные данные
        '409':
          description: Email уже существует

  /auth/login:
    post:
      summary: Вход в систему
      tags: [Авторизация]
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
                  format: password
      responses:
        '200':
          description: Успешный вход
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'
        '401':
          description: Неверные учетные данные

  /auth/me:
    get:
      summary: Получить профиль пользователя
      tags: [Авторизация]
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Профиль пользователя
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Не авторизован

  /movies:
    get:
      summary: Получить список фильмов
      tags: [Фильмы]
      parameters:
        - in: query
          name: skip
          schema:
            type: integer
            default: 0
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
        - in: query
          name: genre
          schema:
            type: string
      responses:
        '200':
          description: Список фильмов
          content:
            application/json:
              schema:
                type: object
                properties:
                  movies:
                    type: array
                    items:
                      $ref: '#/components/schemas/Movie'
                  total:
                    type: integer
                  page:
                    type: integer
                  limit:
                    type: integer

  /sessions:
    get:
      summary: Получить список сеансов
      tags: [Сеансы]
      parameters:
        - in: query
          name: movie_id
          schema:
            type: string
            format: uuid
        - in: query
          name: date
          schema:
            type: string
            format: date
        - in: query
          name: skip
          schema:
            type: integer
            default: 0
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: Список сеансов
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Session'

  /sessions/{session_id}/tickets:
    get:
      summary: Получить билеты сеанса
      tags: [Билеты]
      parameters:
        - in: path
          name: session_id
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Список билетов сеанса
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Ticket'

  /tickets:
    post:
      summary: Забронировать билет
      tags: [Билеты]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - session_id
                - seat_row
                - seat_number
              properties:
                session_id:
                  type: string
                  format: uuid
                seat_row:
                  type: integer
                seat_number:
                  type: integer
      responses:
        '201':
          description: Билет успешно забронирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Ticket'
        '400':
          description: Неверные данные
        '409':
          description: Место уже занято

  /tickets/my:
    get:
      summary: Получить мои билеты
      tags: [Билеты]
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Список билетов пользователя
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Ticket'

  /admin/users:
    get:
      summary: Получить список всех пользователей
      tags: [Администрирование]
      security:
        - bearerAuth: []
      parameters:
        - in: query
          name: role
          schema:
            type: string
            enum: [customer, manager, admin]
        - in: query
          name: skip
          schema:
            type: integer
            default: 0
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: Список пользователей
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '403':
          description: Недостаточно прав

  /admin/tickets:
    get:
      summary: Получить список всех билетов
      tags: [Администрирование]
      security:
        - bearerAuth: []
      parameters:
        - in: query
          name: status
          schema:
            type: string
            enum: [reserved, confirmed, cancelled]
        - in: query
          name: skip
          schema:
            type: integer
            default: 0
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: Список билетов
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Ticket'
        '403':
          description: Недостаточно прав

  /:
    get:
      summary: Главная страница API
      tags: [Общие]
      responses:
        '200':
          description: Информация об API
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  version:
                    type: string
                  status:
                    type: string

  /health:
    get:
      summary: Проверка состояния сервиса
      tags: [Общие]
      responses:
        '200':
          description: Сервис работает
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  timestamp:
                    type: string
                    format: date-time
```

---

## Основные эндпоинты:

### 1. Авторизация (/auth):
- **POST** /auth/register - Регистрация пользователя
- **POST** /auth/login - Вход в систему  
- **GET** /auth/me - Профиль пользователя

### 2. Фильмы (/movies):
- **GET** /movies - Список фильмов с фильтрацией

### 3. Сеансы (/sessions):
- **GET** /sessions - Получение расписания сеансов
- **GET** /sessions/{id}/tickets - Билеты конкретного сеанса

### 4. Билеты (/tickets):
- **POST** /tickets - Бронирование билета
- **GET** /tickets/my - Список билетов пользователя

### 5. Администрирование (/admin):
- **GET** /admin/users - Управление пользователями
- **GET** /admin/tickets - Управление билетами

### 6. Общие эндпоинты:
- **GET** / - Главная страница API
- **GET** /health - Проверка состояния системы
- **GET** /demo/populate - Заполнение демо-данными

---

**Итого:** 13 активных эндпоинтов  
**Версия API:** 2.0  
**Формат данных:** JSON  
**Авторизация:** JWT Bearer токены  
**База данных:** SQLite с 7 таблицами  
**Технологии:** Python, FastAPI, SQLAlchemy, Pydantic 