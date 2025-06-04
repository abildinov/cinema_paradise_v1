# ER-диаграмма базы данных Cinema Paradise

## Концептуальная диаграмма

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

## Детальная диаграмма с кардинальностью

```
USERS ||──o{ TICKETS : "бронирует"
  │
  ├── id (PK)
  ├── username (UK)
  ├── email (UK) 
  ├── role (admin|manager|customer)
  └── ... (остальные поля)

MOVIES ||──o{ SESSIONS : "показывается в"
  │
  ├── id (PK)
  ├── title
  ├── genre (action|comedy|drama|...)
  └── ... (остальные поля)

MOVIES ||──o{ REVIEWS : "получает отзывы"

CINEMAS ||──o{ HALLS : "содержит"
  │
  ├── id (PK)
  ├── name
  ├── address
  └── ... (остальные поля)

HALLS ||──o{ SESSIONS : "проводит сеансы"
  │
  ├── id (PK)
  ├── cinema_id (FK)
  ├── total_seats
  └── ... (остальные поля)

SESSIONS ||──o{ TICKETS : "продает билеты"
  │
  ├── id (PK)
  ├── movie_id (FK)
  ├── hall_id (FK)
  ├── start_time
  ├── base_price
  └── ... (остальные поля)

TICKETS
  │
  ├── id (PK)
  ├── session_id (FK)
  ├── user_id (FK)
  ├── seat_row
  ├── seat_number
  ├── booking_reference (UK)
  └── ... (остальные поля)

REVIEWS
  │
  ├── id (PK)
  ├── movie_id (FK)
  ├── user_id (FK)
  ├── rating (1-10)
  └── ... (остальные поля)
```

## Связи и ограничения

### Типы связей:
- **USERS → TICKETS**: One-to-Many (1:N)
- **SESSIONS → TICKETS**: One-to-Many (1:N)
- **MOVIES → SESSIONS**: One-to-Many (1:N)
- **HALLS → SESSIONS**: One-to-Many (1:N)
- **CINEMAS → HALLS**: One-to-Many (1:N)
- **MOVIES → REVIEWS**: One-to-Many (1:N)
- **USERS → REVIEWS**: One-to-Many (1:N)

### Уникальные ключи:
- `users.username` - уникальное имя пользователя
- `users.email` - уникальный email
- `tickets.booking_reference` - уникальный номер брони

### Составные ограничения:
- `(sessions.movie_id, sessions.hall_id, sessions.start_time)` - нет пересекающихся сеансов в одном зале
- `(tickets.session_id, tickets.seat_row, tickets.seat_number)` - одно место на сеанс

### Перечисления (ENUM):
- **UserRole**: admin, manager, customer
- **MovieGenre**: action, comedy, drama, horror, romance, sci_fi, thriller, documentary, animation, fantasy

## Индексы

### Первичные ключи (Primary Keys):
- `users.id`
- `movies.id`
- `cinemas.id`
- `halls.id`
- `sessions.id`
- `tickets.id`
- `reviews.id`

### Внешние ключи (Foreign Keys):
- `tickets.session_id → sessions.id`
- `tickets.user_id → users.id`
- `sessions.movie_id → movies.id`
- `sessions.hall_id → halls.id`
- `halls.cinema_id → cinemas.id`
- `reviews.movie_id → movies.id`
- `reviews.user_id → users.id`

### Индексы для оптимизации:
- `users.username` (уникальный)
- `users.email` (уникальный)
- `sessions.start_time`
- `sessions.date`
- `tickets.booking_reference` (уникальный)
- `movies.title`

## Бизнес-правила

### Ограничения целостности:
1. **Билет не может быть забронирован на прошедший сеанс**
2. **Количество проданных билетов не может превышать вместимость зала**
3. **Сеанс не может начинаться раньше времени открытия кинотеатра**
4. **Один пользователь не может оставить несколько отзывов на один фильм**
5. **Место в зале не может быть забронировано дважды на один сеанс**

### Каскадное удаление:
- При удалении **пользователя** → удаляются его **билеты** и **отзывы**
- При удалении **фильма** → удаляются связанные **сеансы** и **отзывы**
- При удалении **сеанса** → удаляются связанные **билеты**
- При удалении **кинотеатра** → удаляются связанные **залы** и **сеансы**
- При удалении **зала** → удаляются связанные **сеансы**

---

**Всего таблиц:** 7  
**Всего связей:** 7  
**Всего полей:** 95+  
**Версия схемы:** 2.0 