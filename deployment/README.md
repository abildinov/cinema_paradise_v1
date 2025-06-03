# 🚀 Cinema Paradise - Production Deployment

Полное руководство по развертыванию системы Cinema Paradise на VPS сервере.

## 📋 Содержание

- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Подробная настройка](#подробная-настройка)
- [SSL сертификаты](#ssl-сертификаты)
- [Мониторинг](#мониторинг)
- [Резервное копирование](#резервное-копирование)
- [Обслуживание](#обслуживание)

## 🔧 Требования

### Минимальные требования VPS:
- **CPU**: 2 ядра
- **RAM**: 4 GB
- **Диск**: 20 GB SSD
- **ОС**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **Сеть**: Статический IP адрес

### Программное обеспечение:
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Nginx (опционально, если не используете Docker)

## ⚡ Быстрый старт

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка для применения изменений
sudo reboot
```

### 2. Клонирование проекта

```bash
git clone https://github.com/YOUR_USERNAME/cinema-paradise.git
cd cinema-paradise/deployment
```

### 3. Настройка переменных окружения

```bash
# Копирование примера конфигурации
cp env.production.example .env.production

# Редактирование конфигурации
nano .env.production
```

**Обязательно измените:**
- `SECRET_KEY` - уникальный секретный ключ (минимум 32 символа)
- `DOMAIN` - ваш домен
- `LETSENCRYPT_EMAIL` - ваш email для SSL сертификатов
- `GRAFANA_PASSWORD` - пароль для Grafana

### 4. Настройка SSL

```bash
# Автоматическая настройка SSL с Let's Encrypt
chmod +x setup-ssl.sh
./setup-ssl.sh
```

### 5. Запуск системы

```bash
# Автоматический деплой
chmod +x deploy.sh
./deploy.sh
```

## 🔧 Подробная настройка

### Структура файлов

```
deployment/
├── 📄 docker-compose.production.yml  # Основная конфигурация
├── 🐳 Dockerfile.production          # Production образ API
├── 📁 nginx/                         # Конфигурации Nginx
│   ├── nginx.conf                    # Основной reverse proxy
│   ├── frontend.conf                 # Веб-приложение
│   └── mobile.conf                   # PWA приложение
├── 📁 monitoring/                    # Мониторинг
│   └── prometheus.yml                # Конфигурация Prometheus
├── 📁 ssl/                          # SSL сертификаты
├── 🔧 env.production.example         # Пример переменных окружения
├── 🚀 deploy.sh                     # Скрипт деплоя
├── 🔒 setup-ssl.sh                  # Настройка SSL
├── 💾 backup.sh                     # Резервное копирование
└── 📖 README.md                     # Эта документация
```

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|---------|
| `ENVIRONMENT` | Режим работы | `production` |
| `SECRET_KEY` | JWT секретный ключ | `your-super-secret-key...` |
| `DOMAIN` | Основной домен | `cinema.example.com` |
| `CORS_ORIGINS` | Разрешенные домены | `https://cinema.example.com` |
| `LETSENCRYPT_EMAIL` | Email для SSL | `admin@example.com` |
| `GRAFANA_PASSWORD` | Пароль Grafana | `secure-password` |

## 🔒 SSL сертификаты

### Автоматическая настройка (Let's Encrypt)

```bash
./setup-ssl.sh
# Выберите опцию 1 для Let's Encrypt
```

### Ручная настройка

```bash
# Получение сертификата
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Копирование в проект
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/
sudo chown $USER:$USER ssl/*.pem
```

### Автообновление сертификатов

Скрипт автоматически настраивает cron задачу для обновления сертификатов.

## 📊 Мониторинг

### Доступ к системам мониторинга:

- **Grafana**: `http://your-domain.com:3001`
  - Логин: `admin`
  - Пароль: из переменной `GRAFANA_PASSWORD`

- **Prometheus**: `http://your-domain.com:9090` (только с сервера)

### Основные метрики:

- Использование CPU и памяти
- Количество запросов к API
- Время ответа
- Статус контейнеров
- Использование диска

## 💾 Резервное копирование

### Автоматическое резервное копирование

```bash
# Ручной запуск
chmod +x backup.sh
./backup.sh

# Настройка автоматического бэкапа (каждый день в 2:00)
(crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup.sh") | crontab -
```

### Что включается в бэкап:

- База данных SQLite
- Конфигурационные файлы
- SSL сертификаты
- Логи системы

### Восстановление из бэкапа

```bash
# Распаковка бэкапа
cd backups
tar -xzf cinema_paradise_YYYYMMDD_HHMMSS.tar.gz

# Восстановление базы данных
cp cinema_paradise_YYYYMMDD_HHMMSS/cinema_v2.db ../data/

# Восстановление SSL
cp -r cinema_paradise_YYYYMMDD_HHMMSS/ssl ../

# Перезапуск системы
cd ..
docker-compose -f docker-compose.production.yml restart
```

## 🔧 Обслуживание

### Полезные команды

```bash
# Просмотр логов
docker-compose -f docker-compose.production.yml logs -f

# Статус контейнеров
docker-compose -f docker-compose.production.yml ps

# Перезапуск системы
docker-compose -f docker-compose.production.yml restart

# Остановка системы
docker-compose -f docker-compose.production.yml down

# Обновление образов
docker-compose -f docker-compose.production.yml pull
docker-compose -f docker-compose.production.yml up -d
```

### Мониторинг ресурсов

```bash
# Использование Docker
docker stats

# Использование диска
df -h

# Использование памяти
free -h

# Загрузка CPU
top
```

### Очистка системы

```bash
# Очистка неиспользуемых образов
docker system prune -f

# Очистка логов Docker
sudo sh -c 'echo "" > $(docker inspect --format="{{.LogPath}}" container_name)'

# Очистка старых бэкапов (автоматически через 30 дней)
find backups/ -name "*.tar.gz" -mtime +30 -delete
```

## 🌐 Доступ к приложению

После успешного деплоя система будет доступна по адресам:

- **📱 Мобильное приложение**: `https://your-domain.com/mobile/`
- **🌐 Веб-интерфейс**: `https://your-domain.com/web/`
- **🔗 API документация**: `https://your-domain.com/api/docs`
- **📊 Мониторинг**: `http://your-domain.com:3001`

## 🆘 Устранение неполадок

### Проблемы с SSL

```bash
# Проверка сертификатов
openssl x509 -in ssl/fullchain.pem -text -noout

# Тест SSL соединения
openssl s_client -connect your-domain.com:443
```

### Проблемы с контейнерами

```bash
# Проверка логов конкретного контейнера
docker logs cinema-api-prod

# Вход в контейнер для диагностики
docker exec -it cinema-api-prod /bin/bash
```

### Проблемы с базой данных

```bash
# Проверка базы данных
sqlite3 ../data/cinema_v2.db ".tables"

# Проверка размера базы
ls -lh ../data/cinema_v2.db
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что все порты открыты
3. Проверьте DNS настройки домена
4. Убедитесь в корректности SSL сертификатов

## 🎉 Готово!

Ваша система Cinema Paradise готова к работе в production среде!

**Основные преимущества этого деплоя:**

- ✅ **Безопасность**: HTTPS, security headers, rate limiting
- ✅ **Масштабируемость**: Docker контейнеры, nginx load balancing
- ✅ **Мониторинг**: Prometheus + Grafana
- ✅ **Надежность**: Health checks, автоперезапуск
- ✅ **Резервное копирование**: Автоматические бэкапы
- ✅ **Простота**: Один скрипт для деплоя 