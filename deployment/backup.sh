#!/bin/bash

# 💾 Cinema Paradise Backup Script
# Автоматическое резервное копирование данных

set -e

echo "💾 Cinema Paradise - Backup"
echo "=========================="

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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

# Настройки
BACKUP_DIR="backups"
DATE=$(date +'%Y%m%d_%H%M%S')
BACKUP_NAME="cinema_paradise_$DATE"
RETENTION_DAYS=30

# Создание директории для бэкапов
create_backup_dir() {
    mkdir -p "$BACKUP_DIR/$BACKUP_NAME"
    log "✅ Создана директория бэкапа: $BACKUP_DIR/$BACKUP_NAME"
}

# Резервное копирование базы данных
backup_database() {
    log "Резервное копирование базы данных..."
    
    if [ -f "../data/cinema_v2.db" ]; then
        cp "../data/cinema_v2.db" "$BACKUP_DIR/$BACKUP_NAME/"
        log "✅ База данных скопирована"
    else
        warn "База данных не найдена"
    fi
}

# Резервное копирование конфигурации
backup_config() {
    log "Резервное копирование конфигурации..."
    
    # Переменные окружения (без секретов)
    if [ -f ".env.production" ]; then
        grep -v "PASSWORD\|SECRET\|KEY" .env.production > "$BACKUP_DIR/$BACKUP_NAME/env.backup" || true
        log "✅ Конфигурация скопирована (без секретов)"
    fi
    
    # Docker compose файлы
    cp docker-compose.production.yml "$BACKUP_DIR/$BACKUP_NAME/"
    cp -r nginx "$BACKUP_DIR/$BACKUP_NAME/"
    cp -r monitoring "$BACKUP_DIR/$BACKUP_NAME/"
    
    log "✅ Конфигурационные файлы скопированы"
}

# Резервное копирование SSL сертификатов
backup_ssl() {
    log "Резервное копирование SSL сертификатов..."
    
    if [ -d "ssl" ]; then
        cp -r ssl "$BACKUP_DIR/$BACKUP_NAME/"
        log "✅ SSL сертификаты скопированы"
    else
        warn "SSL сертификаты не найдены"
    fi
}

# Резервное копирование логов
backup_logs() {
    log "Резервное копирование логов..."
    
    mkdir -p "$BACKUP_DIR/$BACKUP_NAME/logs"
    
    # Docker логи
    docker-compose -f docker-compose.production.yml logs --no-color > "$BACKUP_DIR/$BACKUP_NAME/logs/docker.log" 2>/dev/null || true
    
    # Системные логи nginx
    if [ -d "/var/log/nginx" ]; then
        sudo cp /var/log/nginx/access.log "$BACKUP_DIR/$BACKUP_NAME/logs/" 2>/dev/null || true
        sudo cp /var/log/nginx/error.log "$BACKUP_DIR/$BACKUP_NAME/logs/" 2>/dev/null || true
    fi
    
    log "✅ Логи скопированы"
}

# Создание архива
create_archive() {
    log "Создание архива..."
    
    cd "$BACKUP_DIR"
    tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
    rm -rf "$BACKUP_NAME"
    
    log "✅ Архив создан: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
}

# Очистка старых бэкапов
cleanup_old_backups() {
    log "Очистка старых бэкапов (старше $RETENTION_DAYS дней)..."
    
    find "$BACKUP_DIR" -name "cinema_paradise_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    
    log "✅ Старые бэкапы удалены"
}

# Отправка в облако (опционально)
upload_to_cloud() {
    if [ -n "$BACKUP_S3_BUCKET" ] && command -v aws &> /dev/null; then
        log "Загрузка в S3..."
        aws s3 cp "$BACKUP_DIR/$BACKUP_NAME.tar.gz" "s3://$BACKUP_S3_BUCKET/cinema-paradise/"
        log "✅ Бэкап загружен в S3"
    fi
    
    if [ -n "$BACKUP_GDRIVE_FOLDER" ] && command -v rclone &> /dev/null; then
        log "Загрузка в Google Drive..."
        rclone copy "$BACKUP_DIR/$BACKUP_NAME.tar.gz" "gdrive:$BACKUP_GDRIVE_FOLDER"
        log "✅ Бэкап загружен в Google Drive"
    fi
}

# Проверка размера бэкапа
check_backup_size() {
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)
    log "📊 Размер бэкапа: $BACKUP_SIZE"
    
    # Проверка свободного места
    FREE_SPACE=$(df -h "$BACKUP_DIR" | awk 'NR==2 {print $4}')
    log "💾 Свободное место: $FREE_SPACE"
}

# Основная функция
main() {
    cd "$(dirname "$0")"
    
    log "🚀 Начало резервного копирования..."
    
    create_backup_dir
    backup_database
    backup_config
    backup_ssl
    backup_logs
    create_archive
    check_backup_size
    cleanup_old_backups
    upload_to_cloud
    
    log "🎉 Резервное копирование завершено!"
    log "📁 Бэкап сохранен: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
}

# Запуск
main "$@" 