#!/bin/bash

# 🔒 SSL Certificate Setup for Cinema Paradise
# Автоматическая настройка SSL сертификатов с Let's Encrypt

set -e

echo "🔒 Cinema Paradise - SSL Setup"
echo "=============================="

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

# Проверка переменных окружения
check_env() {
    if [ ! -f ".env.production" ]; then
        error "Файл .env.production не найден!"
    fi
    
    source .env.production
    
    if [ -z "$DOMAIN" ] || [ -z "$LETSENCRYPT_EMAIL" ]; then
        error "Переменные DOMAIN и LETSENCRYPT_EMAIL должны быть установлены в .env.production"
    fi
    
    log "✅ Переменные окружения проверены"
}

# Установка Certbot
install_certbot() {
    log "Установка Certbot..."
    
    if command -v certbot &> /dev/null; then
        log "✅ Certbot уже установлен"
        return
    fi
    
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y certbot
    # CentOS/RHEL
    elif command -v yum &> /dev/null; then
        sudo yum install -y certbot
    else
        error "Неподдерживаемая операционная система"
    fi
    
    log "✅ Certbot установлен"
}

# Получение сертификата
obtain_certificate() {
    log "Получение SSL сертификата для $DOMAIN..."
    
    # Создаем директорию для SSL
    mkdir -p ssl
    
    # Временно останавливаем nginx если он запущен
    docker-compose -f docker-compose.production.yml stop nginx || true
    
    # Получаем сертификат
    sudo certbot certonly \
        --standalone \
        --email "$LETSENCRYPT_EMAIL" \
        --agree-tos \
        --no-eff-email \
        --domains "$DOMAIN" \
        --domains "www.$DOMAIN"
    
    # Копируем сертификаты в нашу директорию
    sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ssl/
    sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ssl/
    
    # Устанавливаем правильные права
    sudo chown $(whoami):$(whoami) ssl/*.pem
    chmod 600 ssl/privkey.pem
    chmod 644 ssl/fullchain.pem
    
    log "✅ SSL сертификат получен"
}

# Настройка автообновления
setup_renewal() {
    log "Настройка автообновления сертификата..."
    
    # Создаем скрипт обновления
    cat > ssl/renew.sh << 'EOF'
#!/bin/bash
# Обновление SSL сертификата

DOMAIN=$(grep DOMAIN /path/to/deployment/.env.production | cut -d'=' -f2)
cd /path/to/deployment

# Обновляем сертификат
certbot renew --quiet

# Копируем новые сертификаты
cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ssl/
cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ssl/

# Перезапускаем nginx
docker-compose -f docker-compose.production.yml restart nginx

echo "SSL certificate renewed successfully"
EOF
    
    # Заменяем путь на текущий
    sed -i "s|/path/to/deployment|$(pwd)|g" ssl/renew.sh
    chmod +x ssl/renew.sh
    
    # Добавляем в crontab
    (crontab -l 2>/dev/null; echo "0 3 * * * $(pwd)/ssl/renew.sh >> $(pwd)/ssl/renew.log 2>&1") | crontab -
    
    log "✅ Автообновление настроено (каждый день в 3:00)"
}

# Создание самоподписанного сертификата для разработки
create_self_signed() {
    log "Создание самоподписанного сертификата для разработки..."
    
    mkdir -p ssl
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/privkey.pem \
        -out ssl/fullchain.pem \
        -subj "/C=RU/ST=Moscow/L=Moscow/O=Cinema Paradise/CN=$DOMAIN"
    
    chmod 600 ssl/privkey.pem
    chmod 644 ssl/fullchain.pem
    
    warn "⚠️  Создан самоподписанный сертификат!"
    warn "⚠️  Браузеры будут показывать предупреждение о безопасности"
    warn "⚠️  Для production используйте Let's Encrypt"
}

# Основная функция
main() {
    cd "$(dirname "$0")"
    
    check_env
    source .env.production
    
    echo "Выберите тип сертификата:"
    echo "1) Let's Encrypt (рекомендуется для production)"
    echo "2) Самоподписанный (для разработки/тестирования)"
    read -p "Введите номер (1 или 2): " choice
    
    case $choice in
        1)
            install_certbot
            obtain_certificate
            setup_renewal
            ;;
        2)
            create_self_signed
            ;;
        *)
            error "Неверный выбор"
            ;;
    esac
    
    log "🎉 SSL настройка завершена!"
    log "Сертификаты находятся в директории ssl/"
}

main "$@" 