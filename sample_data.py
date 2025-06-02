"""
Скрипт для добавления тестовых данных в Cinema API
Запустите после создания базы данных для демонстрации функционала
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Тестовые данные фильмов
movies_data = [
    {
        "title": "Матрица",
        "description": "Компьютерный хакер узнает от таинственных повстанцев о настоящей природе своей реальности",
        "duration_minutes": 136,
        "genre": "Научная фантастика",
        "director": "Лана Вачовски, Лилли Вачовски",
        "release_year": 1999,
        "rating": 8.7,
        "poster_url": "https://example.com/matrix.jpg"
    },
    {
        "title": "Интерстеллар",
        "description": "Команда исследователей путешествует через червоточину в космосе",
        "duration_minutes": 169,
        "genre": "Научная фантастика",
        "director": "Кристофер Нолан",
        "release_year": 2014,
        "rating": 8.6,
        "poster_url": "https://example.com/interstellar.jpg"
    },
    {
        "title": "Криминальное чтиво",
        "description": "Жизни двух киллеров пересекаются с жизнями других преступников",
        "duration_minutes": 154,
        "genre": "Криминал",
        "director": "Квентин Тарантино",
        "release_year": 1994,
        "rating": 8.9,
        "poster_url": "https://example.com/pulp_fiction.jpg"
    }
]

def create_movies():
    """Создание тестовых фильмов"""
    print("Создание фильмов...")
    movie_ids = []
    
    for movie in movies_data:
        response = requests.post(f"{BASE_URL}/api/v1/movies/", json=movie)
        if response.status_code == 200:
            movie_data = response.json()
            movie_ids.append(movie_data["id"])
            print(f"✓ Создан фильм: {movie['title']} (ID: {movie_data['id']})")
        else:
            print(f"✗ Ошибка создания фильма {movie['title']}: {response.text}")
    
    return movie_ids

def create_sessions(movie_ids):
    """Создание тестовых сеансов"""
    print("\nСоздание сеансов...")
    session_ids = []
    
    # Создаем сеансы на следующие несколько дней
    base_date = datetime.now() + timedelta(days=1)
    
    for i, movie_id in enumerate(movie_ids):
        # Создаем по 2 сеанса для каждого фильма
        times = [
            (base_date.replace(hour=14, minute=0), base_date.replace(hour=16, minute=30)),
            (base_date.replace(hour=19, minute=0), base_date.replace(hour=21, minute=30))
        ]
        
        for j, (start_time, end_time) in enumerate(times):
            session_data = {
                "movie_id": movie_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "hall_number": (i % 3) + 1,  # Залы 1, 2, 3
                "total_seats": 50,
                "price": 350.0 + (i * 50)  # Разные цены для разных фильмов
            }
            
            response = requests.post(f"{BASE_URL}/api/v1/sessions/", json=session_data)
            if response.status_code == 200:
                session_data_resp = response.json()
                session_ids.append(session_data_resp["id"])
                print(f"✓ Создан сеанс: фильм ID {movie_id}, зал {session_data['hall_number']}, "
                      f"время {start_time.strftime('%H:%M')} (ID: {session_data_resp['id']})")
            else:
                print(f"✗ Ошибка создания сеанса: {response.text}")
    
    return session_ids

def create_sample_tickets(session_ids):
    """Создание примеров билетов"""
    print("\nСоздание примеров билетов...")
    
    sample_customers = [
        {"name": "Иван Иванов", "email": "ivan@example.com", "phone": "+7-900-123-45-67"},
        {"name": "Мария Петрова", "email": "maria@example.com", "phone": "+7-900-234-56-78"},
        {"name": "Алексей Сидоров", "email": "alexey@example.com", "phone": "+7-900-345-67-89"},
        {"name": "Елена Козлова", "email": "elena@example.com", "phone": "+7-900-456-78-90"},
    ]
    
    ticket_ids = []
    
    for i, session_id in enumerate(session_ids[:4]):  # Создаем билеты только для первых 4 сеансов
        customer = sample_customers[i % len(sample_customers)]
        
        # Получаем информацию о сеансе для определения цены
        session_response = requests.get(f"{BASE_URL}/api/v1/sessions/{session_id}")
        if session_response.status_code == 200:
            session_data = session_response.json()
            
            ticket_data = {
                "session_id": session_id,
                "seat_number": (i % 10) + 1,  # Места 1-10
                "customer_name": customer["name"],
                "customer_email": customer["email"],
                "customer_phone": customer["phone"],
                "price": session_data["price"]
            }
            
            response = requests.post(f"{BASE_URL}/api/v1/tickets/", json=ticket_data)
            if response.status_code == 200:
                ticket_data_resp = response.json()
                ticket_ids.append(ticket_data_resp["id"])
                print(f"✓ Создан билет: {customer['name']}, место {ticket_data['seat_number']}, "
                      f"сеанс {session_id} (ID: {ticket_data_resp['id']})")
                
                # Оплачиваем каждый второй билет
                if i % 2 == 0:
                    pay_response = requests.patch(f"{BASE_URL}/api/v1/tickets/{ticket_data_resp['id']}/pay")
                    if pay_response.status_code == 200:
                        print(f"  ✓ Билет {ticket_data_resp['id']} оплачен")
            else:
                print(f"✗ Ошибка создания билета: {response.text}")
    
    return ticket_ids

def main():
    """Основная функция создания тестовых данных"""
    print("🎬 Создание тестовых данных для Cinema API\n")
    
    try:
        # Проверяем доступность API
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code != 200:
            print("❌ API недоступно. Убедитесь, что сервер запущен на http://localhost:8000")
            return
        
        print("✅ API доступно\n")
        
        # Создаем данные
        movie_ids = create_movies()
        if movie_ids:
            session_ids = create_sessions(movie_ids)
            if session_ids:
                ticket_ids = create_sample_tickets(session_ids)
        
        print(f"\n🎉 Тестовые данные созданы успешно!")
        print(f"📽 Фильмов: {len(movie_ids)}")
        print(f"🎭 Сеансов: {len(session_ids) if 'session_ids' in locals() else 0}")
        print(f"🎫 Билетов: {len(ticket_ids) if 'ticket_ids' in locals() else 0}")
        print(f"\n📚 Документация API: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 