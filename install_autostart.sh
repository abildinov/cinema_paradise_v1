#!/bin/bash
echo "⚙️ Настройка автозапуска Cinema Paradise"
echo "======================================="

PROJECT_DIR="$PWD"
USER=$(whoami)

# Создаем systemd сервис
SERVICE_FILE="/etc/systemd/system/cinema-paradise.service"

echo "📝 Создание systemd сервиса..."

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Cinema Paradise - Movie Theater Management System
After=network.target

[Service]
Type=forking
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=/usr/bin:/bin:/usr/local/bin
ExecStart=$PROJECT_DIR/start_all_server.sh
ExecStop=$PROJECT_DIR/stop_all_server.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Делаем скрипты исполняемыми
chmod +x start_all_server.sh
chmod +x stop_all_server.sh
chmod +x status_server.sh

# Перезагружаем systemd и включаем автозапуск
echo "🔄 Настройка systemd..."
sudo systemctl daemon-reload
sudo systemctl enable cinema-paradise.service

echo "✅ Автозапуск настроен!"
echo ""
echo "📋 Управление сервисом:"
echo "  🚀 Запуск:    sudo systemctl start cinema-paradise"
echo "  🛑 Остановка: sudo systemctl stop cinema-paradise"
echo "  🔄 Перезапуск: sudo systemctl restart cinema-paradise"
echo "  📊 Статус:    sudo systemctl status cinema-paradise"
echo "  📝 Логи:      sudo journalctl -u cinema-paradise -f"
echo ""
echo "💡 Автозапуск включен! Сервис запустится автоматически при перезагрузке сервера." 