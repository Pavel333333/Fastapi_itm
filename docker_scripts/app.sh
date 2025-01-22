#!/bin/bash

# Проверка на существование файла wait-for-it.sh
if [ ! -f /usr/local/bin/wait-for-it ]; then
    echo "wait-for-it не найден, скачиваю..."
    curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it
    chmod +x /usr/local/bin/wait-for-it
else
    echo "wait-for-it уже установлен."
fi

# Ждем, пока база данных будет доступна
echo "Waiting for database to be ready..."
wait-for-it container_db:5432 --timeout=60 -- alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Alembic migrations failed"
    exit 1
fi

echo "Migrations complete"

sleep 15

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000