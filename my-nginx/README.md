#!/bin/bash

# === Настройка окружения ===
echo "=== Обновление системы и установка пакетов ==="
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git postgresql postgresql-contrib

# === Настройка PostgreSQL ===
echo "=== Настройка PostgreSQL ==="
sudo -u postgres psql -c "CREATE DATABASE netology_stocks_products;"
sudo -u postgres psql -c "CREATE USER myuser WITH PASSWORD 'mypassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netology_stocks_products TO myuser;"

# === Клонирование проекта ===
echo "=== Клонирование проекта ==="
if [ ! -d "dj-homeworks" ]; then
    git clone https://github.com/netology-code/dj-homeworks
fi
cd dj-homeworks/3.2-crud/stocks_products || exit

# === Настройка виртуального окружения ===
echo "=== Настройка виртуального окружения ==="
python3 -m venv venv
source venv/bin/activate

# === Установка зависимостей ===
echo "=== Установка зависимостей ==="
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# === Настройка Django ===
echo "=== Настройка Django ==="
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

cat > stocks_products/settings_prod.py <<EOF
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netology_stocks_products',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = '$SECRET_KEY'
EOF

# === Применение миграций ===
echo "=== Применение миграций ==="
python manage.py migrate --settings=stocks_products.settings_prod
python manage.py collectstatic --noinput --settings=stocks_products.settings_prod

# === Настройка Gunicorn (systemd) ===
echo "=== Настройка Gunicorn ==="
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:$(pwd)/stocks_products.sock stocks_products.wsgi:application --settings=stocks_products.settings_prod

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# === Настройка Nginx ===
echo "=== Настройка Nginx ==="
SERVER_IP=$(curl -s ifconfig.me)

sudo tee /etc/nginx/sites-available/stocks_products > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    location /static/ {
        alias $(pwd)/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/stocks_products.sock;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/stocks_products /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# === Завершение настройки ===
echo "=== Настройка завершена! ==="
echo "Сервер должен быть доступен по адресу: http://$SERVER_IP"
echo "Для создания суперпользователя выполните:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo "  python manage.py createsuperuser --settings=stocks_products.settings_prod"
