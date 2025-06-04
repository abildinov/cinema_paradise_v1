#!/bin/bash

# 🛑 Cinema Paradise Stop Script
# Остановка всех сервисов

echo "🛑 Остановка Cinema Paradise..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Остановка по PID файлам
stop_by_pid() {
    local service=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            log "✅ $service остановлен (PID: $pid)"
        else
            warn "$service уже не запущен (PID: $pid)"
        fi
        rm -f "$pid_file"
    else
        warn "PID файл $pid_file не найден"
    fi
}

# Остановка сервисов
log "Остановка сервисов по PID файлам..."

stop_by_pid "API" "api.pid"
stop_by_pid "Frontend" "frontend.pid"
stop_by_pid "Mobile App" "mobile.pid"

# Дополнительная остановка по процессам
log "Принудительная остановка Python процессов..."

pkill -f "python.*stable_api.py" && log "✅ API процессы остановлены" || true
pkill -f "python.*http.server.*3000" && log "✅ Frontend процессы остановлены" || true
pkill -f "python.*http.server.*3002" && log "✅ Mobile процессы остановлены" || true

log "🎉 Все сервисы остановлены!"

# Показать оставшиеся Python процессы
echo ""
echo "Оставшиеся Python процессы:"
ps aux | grep python | grep -v grep || echo "Нет активных Python процессов" 