#!/bin/bash

# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Создаем директорию для приложения
sudo mkdir -p /opt/webplayer
sudo chown $USER:$USER /opt/webplayer
cd /opt/webplayer

# Копируем файлы (предполагается, что они уже загружены)
# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем systemd сервис
sudo tee /etc/systemd/system/webplayer.service > /dev/null <<EOF
[Unit]
Description=WebPlayer FastAPI app
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/webplayer
Environment=PATH=/opt/webplayer/venv/bin
ExecStart=/opt/webplayer/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Запускаем сервис
sudo systemctl daemon-reload
sudo systemctl enable webplayer
sudo systemctl start webplayer

echo "WebPlayer запущен на порту 8000"
echo "Статус: sudo systemctl status webplayer"