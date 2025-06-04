#!/bin/bash

# 🚀 Cinema Paradise Simple Deployment Script
# Простой деплой на VPS без Docker

set -e  # Остановка при ошибке

echo "🎬 Cinema Paradise - Simple Deployment"
echo "======================================"

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
    
    if ! command -v python3 &> /dev/null; then
        error "Python3 не установлен!"
    fi
    
    if ! command -v nginx &> /dev/null; then
        warn "Nginx не установлен - установите для продакшена"
    fi
    
    log "✅ Основные зависимости найдены"
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

# Остановка старых процессов
stop_services() {
    log "Остановка существующих процессов..."
    
    # Останавливаем процессы Python API
    pkill -f "python.*stable_api.py" || true
    pkill -f "python.*cinema_api" || true
    
    # Останавливаем процессы веб-серверов
    pkill -f "python.*http.server.*3000" || true
    pkill -f "python.*http.server.*3002" || true
    
    log "✅ Старые процессы остановлены"
}

# Установка зависимостей
install_deps() {
    log "Установка зависимостей Python..."
    
    cd ..
    
    # Проверяем и создаем виртуальное окружение
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log "✅ Виртуальное окружение создано"
    fi
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    
    # Устанавливаем зависимости
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log "✅ Зависимости установлены"
}

# Настройка Nginx
setup_nginx() {
    log "Настройка Nginx..."
    
    if command -v nginx &> /dev/null; then
        sudo cp nginx/nginx.conf /etc/nginx/sites-available/cinema-paradise
        sudo ln -sf /etc/nginx/sites-available/cinema-paradise /etc/nginx/sites-enabled/
        sudo nginx -t && sudo systemctl reload nginx
        log "✅ Nginx настроен"
    else
        warn "Nginx не установлен - пропускаем настройку"
    fi
}

# Запуск приложения
start_services() {
    log "Запуск сервисов..."
    
    cd ..
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    
    # Загружаем переменные окружения
    if [ -f "deployment/.env.production" ]; then
        export $(cat deployment/.env.production | grep -v '^#' | xargs)
    fi
    
    # Запускаем API в фоне
    nohup python stable_api.py > logs/api.log 2>&1 &
    API_PID=$!
    echo $API_PID > deployment/api.pid
    
    # Запускаем фронтенд в фоне
    cd frontend
    nohup python -m http.server 3000 > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../deployment/frontend.pid
    
    # Запускаем мобильное приложение в фоне
    cd ../mobile_app
    nohup python -m http.server 3002 --bind 0.0.0.0 > ../logs/mobile.log 2>&1 &
    MOBILE_PID=$!
    echo $MOBILE_PID > ../deployment/mobile.pid
    
    cd ..
    
    log "✅ Сервисы запущены"
    log "API PID: $API_PID"
    log "Frontend PID: $FRONTEND_PID" 
    log "Mobile PID: $MOBILE_PID"
}

# Проверка здоровья
health_check() {
    log "Проверка работоспособности..."
    
    sleep 10  # Ждем запуска сервисов
    
    # Проверка API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log "✅ API работает на порту 8000"
    else
        warn "❌ API не отвечает на порту 8000"
    fi
    
    # Проверка фронтенда
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log "✅ Frontend работает на порту 3000"
    else
        warn "❌ Frontend не отвечает на порту 3000"
    fi
    
    # Проверка мобильного приложения
    if curl -f http://localhost:3002 > /dev/null 2>&1; then
        log "✅ Mobile app работает на порту 3002"
    else
        warn "❌ Mobile app не отвечает на порту 3002"
    fi
}

# Показ статуса
show_status() {
    echo ""
    echo -e "${BLUE}🎉 Деплой завершен успешно!${NC}"
    echo "================================"
    echo ""
    echo "🔗 API: http://localhost:8000/docs"
    echo "🌐 Веб-интерфейс: http://localhost:3000"
    echo "📱 Мобильное приложение: http://localhost:3002"
    echo ""
    echo "📂 Логи:"
    echo "  API: logs/api.log"
    echo "  Frontend: logs/frontend.log"  
    echo "  Mobile: logs/mobile.log"
    echo ""
    echo "📋 Полезные команды:"
    echo "  ./stop.sh                        # Остановка всех сервисов"
    echo "  tail -f logs/api.log            # Просмотр логов API"
    echo "  ps aux | grep python            # Проверка процессов"
    echo ""
}

# Создание директории для логов
setup_logs() {
    mkdir -p logs
    mkdir -p backups
}

# Основная функция
main() {
    cd "$(dirname "$0")"
    
    setup_logs
    check_dependencies
    check_env
    backup_data
    stop_services
    install_deps
    setup_nginx
    start_services
    health_check
    show_status
}

# Запуск с обработкой ошибок
if main "$@"; then
    log "🎉 Деплой завершен успешно!"
else
    error "💥 Ошибка при деплое!"
fi 