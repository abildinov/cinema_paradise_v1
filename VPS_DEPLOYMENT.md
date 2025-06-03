# 🚀 Cinema Paradise - VPS Deployment

Готовая система для развертывания Cinema Paradise на VPS сервере.

## ⚡ Быстрый старт

### 1. Требования VPS
- **CPU**: 2+ ядра
- **RAM**: 4+ GB  
- **Диск**: 20+ GB SSD
- **ОС**: Ubuntu 20.04+ / CentOS 8+
- **Домен**: Настроенный DNS

### 2. Подготовка сервера

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo reboot
```

### 3. Деплой системы

```bash
# Клонирование проекта
git clone https://github.com/YOUR_USERNAME/cinema-paradise.git
cd cinema-paradise/deployment

# Настройка переменных окружения
cp env.production.example .env.production
nano .env.production  # Измените DOMAIN, SECRET_KEY, EMAIL

# Настройка SSL
chmod +x setup-ssl.sh
./setup-ssl.sh

# Запуск системы
chmod +x deploy.sh
./deploy.sh
```

## 🌐 Результат

После деплоя система будет доступна:

- **📱 Мобильное приложение**: `https://your-domain.com/mobile/`
- **🌐 Веб-интерфейс**: `https://your-domain.com/web/`  
- **🔗 API документация**: `https://your-domain.com/api/docs`
- **📊 Мониторинг**: `http://your-domain.com:3001`

## 📁 Структура деплоя

```
deployment/
├── 🚀 deploy.sh                     # Автоматический деплой
├── 🔒 setup-ssl.sh                  # Настройка SSL
├── 💾 backup.sh                     # Резервное копирование
├── 📄 docker-compose.production.yml # Docker конфигурация
├── 🐳 Dockerfile.production         # Production образ
├── 📁 nginx/                        # Nginx конфигурации
├── 📁 monitoring/                   # Prometheus + Grafana
├── 🔧 env.production.example        # Пример переменных
└── 📖 README.md                     # Подробная документация
```

## 🔧 Основные возможности

### ✅ Production готовность
- **HTTPS** с автоматическими SSL сертификатами
- **Security headers** и rate limiting
- **Health checks** и автоперезапуск
- **Gzip сжатие** и кеширование

### ✅ Мониторинг и логи
- **Prometheus** для сбора метрик
- **Grafana** для визуализации
- **Централизованные логи** Docker
- **Автоматические алерты**

### ✅ Резервное копирование
- **Автоматические бэкапы** базы данных
- **Сохранение конфигурации** и SSL
- **Ротация старых бэкапов**
- **Поддержка облачных хранилищ**

### ✅ Простота управления
- **Один скрипт** для полного деплоя
- **Автоматическая настройка** SSL
- **Проверка зависимостей**
- **Подробные логи** процесса

## 🛠️ Управление системой

```bash
# Просмотр статуса
docker-compose -f docker-compose.production.yml ps

# Просмотр логов
docker-compose -f docker-compose.production.yml logs -f

# Перезапуск
docker-compose -f docker-compose.production.yml restart

# Резервное копирование
./backup.sh

# Обновление системы
git pull
./deploy.sh
```

## 📊 Мониторинг

- **Grafana**: `http://your-domain.com:3001`
  - Логин: `admin` 
  - Пароль: из `.env.production`

- **Метрики**:
  - Использование ресурсов
  - Количество запросов
  - Время ответа API
  - Статус контейнеров

## 🆘 Поддержка

Подробная документация: `deployment/README.md`

**Основные команды диагностики:**
```bash
# Проверка контейнеров
docker ps

# Проверка ресурсов
docker stats

# Проверка логов
docker logs cinema-api-prod

# Проверка SSL
openssl s_client -connect your-domain.com:443
```

## 🎉 Готово!

Ваша система Cinema Paradise готова к production использованию с:

- 🔒 **Безопасностью** (HTTPS, security headers)
- 📊 **Мониторингом** (Prometheus + Grafana)  
- 💾 **Бэкапами** (автоматическое резервное копирование)
- 🚀 **Производительностью** (nginx, кеширование, gzip)
- 🔧 **Простотой** (автоматизированный деплой)

**Система масштабируется и готова для реальных пользователей!** 