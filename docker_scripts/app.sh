#!/bin/bash

# Проверка на существование файла wait-for-it.sh
# это скрипт для ожидания готовности одного сервиса до запуска другого
# Этот подход особенно полезен, когда контейнеры зависят друг от друга,
# и один контейнер не может начать работу, пока другой не станет доступен.
if [ ! -f /usr/local/bin/wait-for-it ]; then
    echo "wait-for-it не найден, скачиваю..."
    curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it
    chmod +x /usr/local/bin/wait-for-it
else
    echo "wait-for-it уже установлен."
fi

## Ждем, пока база данных будет доступна
## Прошлая версия
#echo "Waiting for database to be ready..."
#wait-for-it $DB_HOST:$DB_PORT --timeout=60 -- alembic upgrade head

# Ждем базу данных в зависимости от режима. Версия при настройке ci/cd
if [ "$MODE" = "TEST" ]; then
    echo "Waiting for test database to be ready..."
    wait-for-it $TEST_DB_HOST:$TEST_DB_PORT --timeout=89
else
    echo "Waiting for main database to be ready..."
    wait-for-it $DB_HOST:$DB_PORT --timeout=89 -- alembic upgrade head
fi

if [ $? -ne 0 ]; then
    echo "Alembic migrations failed"
    exit 1
fi

echo "Migrations complete"

sleep 15

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000