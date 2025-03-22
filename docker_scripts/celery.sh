#!/bin/bash

# celery -A app.api.celery_tasks worker --loglevel=info
celery -A app.api.celery_tasks worker --loglevel=info -b "amqp://$RABBITMQ_USER:$RABBITMQ_PASS@$RABBITMQ_HOST:5672/$RABBITMQ_VHOST"