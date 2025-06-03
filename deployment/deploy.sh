#!/bin/bash

# 🚀 Cinema Paradise Production Deployment Script
# Автоматический деплой на VPS

set -e  # Остановка при ошибке

echo "🎬 Cinema Paradise - Production Deployment"
echo "=========================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Проверка зависимостей
check_dependencies() {
    log "Проверка зависимостей..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker не установлен!"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose не установлен!"
    fi
    
    log "✅ Все зависимости установлены"
}

# Проверка переменных окружения
check_env() {
    log "Проверка переменных окружения..."
    
    if [ ! -f ".env.production" ]; then
        warn "Файл .env.production не найден!"
        echo "Создайте файл .env.production на основе env.production.example"
        echo "cp env.production.example .env.production"
        echo "Затем отредактируйте переменные в .env.production"
        exit 1
    fi
    
    log "✅ Файл переменных окружения найден"
}

# Создание резервной копии
backup_data() {
    log "Создание резервной копии данных..."
    
    BACKUP_DIR="backups/$(date +'%Y%m%d_%H%M%S')"
    mkdir -p "$BACKUP_DIR"
    
    if [ -f "../data/cinema_v2.db" ]; then
        cp "../data/cinema_v2.db" "$BACKUP_DIR/"
        log "✅ База данных скопирована в $BACKUP_DIR"
    fi
    
    if [ -d "ssl" ]; then
        cp -r ssl "$BACKUP_DIR/"
        log "✅ SSL сертификаты скопированы"
    fi
}

# Остановка старых контейнеров
stop_containers() {
    log "Остановка существующих контейнеров..."
    
    docker-compose -f docker-compose.production.yml down --remove-orphans || true
    
    # Очистка неиспользуемых образов
    docker system prune -f
    
    log "✅ Контейнеры остановлены"
}

# Сборка и запуск
deploy() {
    log "Сборка и запуск приложения..."
    
    # Загрузка переменных окружения
    export $(cat .env.production | grep -v '^#' | xargs)
    
    # Сборка образов
    docker-compose -f docker-compose.production.yml build --no-cache
    
    # Запуск контейнеров
    docker-compose -f docker-compose.production.yml up -d
    
    log "✅ Приложение запущено"
}

# Проверка здоровья
health_check() {
    log "Проверка работоспособности..."
    
    sleep 30  # Ждем запуска контейнеров
    
    # Проверка API
    if curl -f http://localhost/api/health > /dev/null 2>&1; then
        log "✅ API работает"
    else
        error "❌ API не отвечает"
    fi
    
    # Проверка контейнеров
    if docker-compose -f docker-compose.production.yml ps | grep -q "Up"; then
        log "✅ Контейнеры запущены"
    else
        error "❌ Проблемы с контейнерами"
    fi
}

# Показ статуса
show_status() {
    echo ""
    echo -e "${BLUE}🎉 Деплой завершен успешно!${NC}"
    echo "================================"
    echo ""
    echo "📱 Мобильное приложение: https://$(grep DOMAIN .env.production | cut -d'=' -f2)/mobile/"
    echo "🌐 Веб-интерфейс: https://$(grep DOMAIN .env.production | cut -d'=' -f2)/web/"
    echo "🔗 API документация: https://$(grep DOMAIN .env.production | cut -d'=' -f2)/api/docs"
    echo "📊 Мониторинг: http://$(grep DOMAIN .env.production | cut -d'=' -f2):3001"
    echo ""
    echo "📋 Полезные команды:"
    echo "  docker-compose -f docker-compose.production.yml logs -f    # Логи"
    echo "  docker-compose -f docker-compose.production.yml ps         # Статус"
    echo "  docker-compose -f docker-compose.production.yml restart    # Перезапуск"
    echo ""
}

# Основная функция
main() {
    cd "$(dirname "$0")"
    
    check_dependencies
    check_env
    backup_data
    stop_containers
    deploy
    health_check
    show_status
}

# Запуск с обработкой ошибок
if main "$@"; then
    log "🎉 Деплой завершен успешно!"
else
    error "💥 Ошибка при деплое!"
fi 