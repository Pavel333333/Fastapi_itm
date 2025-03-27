import os
import time

from celery import Celery

from app.database import get_db_sync_session
from app.db.models import Document, DocumentText

import requests
import json
import pika

# Получаем хост RabbitMQ из переменной окружения, по умолчанию localhost для DEV
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'pavel')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'pavel')

celery_app = Celery('celery_fastapi_itm', broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672//',
                    backend='rpc://', broker_connection_retry_on_startup=True)

celery_app.conf.update(task_always_eager=True, task_get_db_session=get_db_sync_session)

def publish_result_to_rabbitmq(result, queue='doc_analyze_results'):
    try:
        # Подключение к RabbitMQ с использованием переменной окружения
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, 5672,
                                                                       credentials=pika.PlainCredentials(RABBITMQ_USER,
                                                                                                         RABBITMQ_PASS)))
        channel = connection.channel()
        # Объявляем очередь для результатов, durable=True для сохранения сообщений
        channel.queue_declare(queue=queue, durable=True)
        # Публикуем результат в очередь с постоянным режимом доставки
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(result),
                              properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
    except Exception as e:
        print(f"🔴 Failed to connect to RabbitMQ: {str(e)}")

@celery_app.task
def get_text_from_foto(id: int):
    # Выполнение задачи по распознаванию текста
    try:
        with celery_app.conf.task_get_db_session() as db:
            # Проверка наличия документа в базе
            check_doc_in_db = db.query(Document).filter_by(id=id).one_or_none()

            if not check_doc_in_db:
                # Если документа нет, формируем результат ошибки
                result = {'id': id, 'message': 'такой записи нет в базе'}
                publish_result_to_rabbitmq(result)  # Публикуем результат в очередь
                return result

            # Проверяем, есть ли уже запись в DocumentText
            query_related_documents = db.query(DocumentText).filter_by(id_doc=id).first()

            if query_related_documents:
                # Если запись уже есть, формируем результат ошибки
                result = {'id': id, 'text': query_related_documents.text}
                publish_result_to_rabbitmq(result)  # Публикуем результат в очередь
                return result

            # Получаем путь к изображению
            image_path: str = check_doc_in_db.path
            # Распознаём текст с помощью OCR
            json_from_file = ocr_space_file(image_url=image_path, api_key='K89023680188957', language='rus')
            json_from_file = json.loads(json_from_file)

            # Проверка наличия данных в ParsedResults
            if not json_from_file.get("ParsedResults"):
                result = {'id': id, 'text': 'No parsed results from OCR'}
                publish_result_to_rabbitmq(result)
                return result

            text_from_file = json_from_file["ParsedResults"][0]["ParsedText"]

            # Создаём новую запись в DocumentText
            new_entry_in_doc_text = DocumentText(document=check_doc_in_db, text=text_from_file)
            db.add(new_entry_in_doc_text)
            db.commit()

            # Формируем успешный результат
            result = {'id': id, 'text': text_from_file}
            publish_result_to_rabbitmq(result)  # Публикуем результат в очередь
            return result

    except Exception as e:
        # В случае ошибки формируем результат с исключением
        result = {'id': id, 'error': str(e)}
        publish_result_to_rabbitmq(result)  # Публикуем результат в очередь
        return result


def ocr_space_file(image_url, overlay=False, api_key='helloworld', language='eng'):

    payload = {'isOverlayRequired': overlay, 'apikey': api_key, 'language': language}
    with open(image_url, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image', files={image_url: f}, data=payload)
    return r.content.decode()