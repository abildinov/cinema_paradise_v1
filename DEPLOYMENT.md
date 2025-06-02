# Cinema API - Руководство по развертыванию на VPS

## 🎯 Цель
Развертывание Cinema API на VPS провайдере (например, Cloud.ru) с полной производственной конфигурацией.

## 📋 Требования к серверу

### Минимальные характеристики VPS
- **CPU**: 2 ядра
- **RAM**: 4 GB
- **Storage**: 40 GB SSD
- **OS**: Ubuntu 20.04 LTS или выше
- **Network**: Белый IP адрес
- **Bandwidth**: 100 Mbps

### Рекомендуемые характеристики
- **CPU**: 4 ядра
- **RAM**: 8 GB
- **Storage**: 80 GB SSD

## 🚀 Пошаговое развертывание

### Шаг 1: Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y curl wget git vim htop

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

### Шаг 2: Клонирование репозитория

```bash
# Клонирование проекта
git clone <your-repository-url> cinema_api
cd cinema_api

# Настройка переменных окружения
cp .env.example .env
vim .env
```

### Шаг 3: Конфигурация

#### Файл .env
```env
# Database
DATABASE_URL=postgresql://postgres:SecurePassword123@postgres:5432/cinema_api

# Security
SECRET_KEY=your-very-secure-secret-key-here-64-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False
ENVIRONMENT=production
API_V1_STR=/api/v1

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External APIs
MOVIE_API_KEY=your-movie-api-key
```

#### Nginx конфигурация (nginx.conf)
```nginx
events {
    worker_connections 1024;
}

http {
    upstream cinema_api {
        server cinema-api:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com www.your-domain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # API endpoints
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://cinema_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Documentation
        location /docs {
            proxy_pass http://cinema_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://cinema_api;
            access_log off;
        }

        # Static files (if any)
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### Шаг 4: SSL сертификаты

```bash
# Установка Certbot
sudo apt install -y certbot

# Получение SSL сертификата
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Копирование сертификатов для Docker
sudo mkdir -p ./ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/
sudo chown -R $USER:$USER ./ssl/

# Автообновление сертификатов
sudo crontab -e
# Добавить строку:
# 0 3 * * * certbot renew --quiet && docker-compose restart nginx
```

### Шаг 5: Запуск приложения

```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f cinema-api
```

### Шаг 6: Инициализация базы данных

```bash
# Создание таблиц
docker-compose exec cinema-api python -c "
from app.database import engine
from app import models
models.Base.metadata.create_all(bind=engine)
print('Database initialized successfully')
"

# Создание администратора (опционально)
docker-compose exec cinema-api python -c "
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash
from datetime import datetime

db = SessionLocal()
admin = User(
    username='admin',
    email='admin@cinema.com',
    hashed_password=get_password_hash('admin123'),
    first_name='Admin',
    last_name='User',
    role=UserRole.ADMIN,
    is_active=True,
    created_at=datetime.utcnow()
)
db.add(admin)
db.commit()
print('Admin user created')
"
```

## 🔧 Мониторинг и обслуживание

### Проверка работоспособности

```bash
# Проверка API
curl -X GET "https://your-domain.com/api/v1/movies" -H "accept: application/json"

# Проверка документации
curl -I https://your-domain.com/docs

# Проверка базы данных
docker-compose exec postgres psql -U postgres -d cinema_api -c "SELECT COUNT(*) FROM users;"
```

### Логи и мониторинг

```bash
# Просмотр логов приложения
docker-compose logs -f cinema-api

# Просмотр логов базы данных
docker-compose logs -f postgres

# Просмотр логов Nginx
docker-compose logs -f nginx

# Мониторинг ресурсов
docker stats

# Дисковое пространство
df -h
```

### Резервное копирование

```bash
# Создание backup базы данных
docker-compose exec postgres pg_dump -U postgres cinema_api > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление из backup
docker-compose exec -T postgres psql -U postgres cinema_api < backup_20241220_120000.sql

# Автоматическое резервное копирование (cron)
# 0 2 * * * /path/to/backup_script.sh
```

## 🛡 Безопасность

### Рекомендации по безопасности

1. **Смена паролей по умолчанию**
   ```bash
   # Сгенерировать надежные пароли
   openssl rand -base64 32
   ```

2. **Настройка файрвола**
   ```bash
   # Закрыть ненужные порты
   sudo ufw deny 5432  # PostgreSQL (только для Docker)
   sudo ufw deny 6379  # Redis (только для Docker)
   ```

3. **Обновление зависимостей**
   ```bash
   # Регулярное обновление образов Docker
   docker-compose pull
   docker-compose up -d
   ```

4. **Мониторинг безопасности**
   ```bash
   # Установка fail2ban
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

## 📊 Производительность

### Оптимизация PostgreSQL

```sql
-- Настройки в postgresql.conf
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Перезагрузка конфигурации
SELECT pg_reload_conf();
```

### Индексы для оптимизации

```sql
-- Индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);
CREATE INDEX IF NOT EXISTS idx_movies_genre ON movies(genre);
CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_session_id ON tickets(session_id);
```

## 🚨 Устранение неполадок

### Типичные проблемы

1. **Контейнер не запускается**
   ```bash
   # Проверка логов
   docker-compose logs container-name
   
   # Пересборка без кеша
   docker-compose build --no-cache
   ```

2. **Проблемы с базой данных**
   ```bash
   # Проверка подключения
   docker-compose exec postgres psql -U postgres -c "SELECT version();"
   
   # Восстановление соединения
   docker-compose restart postgres
   ```

3. **SSL проблемы**
   ```bash
   # Проверка сертификата
   openssl x509 -in ./ssl/fullchain.pem -text -noout
   
   # Обновление сертификата
   sudo certbot renew
   ```

## 📈 Масштабирование

### Горизонтальное масштабирование

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  cinema-api:
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Мониторинг производительности

- **Grafana**: http://your-domain.com:3000 (admin/admin)
- **Prometheus**: http://your-domain.com:9090

## 🎯 Финальная проверка

После успешного развертывания проверьте:

1. ✅ API доступен по https://your-domain.com/api/v1/
2. ✅ Документация доступна по https://your-domain.com/docs
3. ✅ SSL сертификат действителен
4. ✅ База данных работает корректно
5. ✅ Мониторинг настроен
6. ✅ Логи записываются
7. ✅ Резервное копирование настроено

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи всех сервисов
2. Убедитесь в корректности конфигурации
3. Проверьте доступность портов
4. Проверьте SSL сертификаты
5. Мониторьте использование ресурсов

**API Endpoints для проверки:**
- Health Check: `GET /health`
- API Documentation: `GET /docs`
- Movies List: `GET /api/v1/movies`
- User Registration: `POST /api/v1/auth/register` 