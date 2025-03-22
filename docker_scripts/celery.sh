#!/bin/bash

celery -A app.api.celery_tasks worker --loglevel=info