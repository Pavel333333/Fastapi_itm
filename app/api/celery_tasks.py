from celery import Celery

from app.database import get_db_sync_session
from app.db.models import Document, DocumentText

import requests
import json

celery_app = Celery('celery_fastapi_itm', broker='amqp://pavel:pavel@localhost:5672//',
                    backend='rpc://')

celery_app.conf.update(task_always_eager=True, task_get_db_session=get_db_sync_session)

@celery_app.task
def get_text_from_foto(id: int):

    try:

        with celery_app.conf.task_get_db_session() as db:

            check_doc_in_db = db.query(Document).filter_by(id=id).one_or_none()

            if check_doc_in_db is None:
                return {'message': 'такой записи нет в базе'}

            image_path: str = check_doc_in_db.path

            json_from_file = ocr_space_file(image_url=image_path, api_key='K89023680188957', language='rus')

            json_from_file = json.loads(json_from_file)

            text_from_file = json_from_file["ParsedResults"][0]["ParsedText"]

            query_related_documents = db.query(DocumentText).filter_by(id_doc=id).first()

            if query_related_documents:
                return {'message': f'у элемента {id} уже есть запись в таблице DocumentText'}

            new_entry_in_doc_text = DocumentText(document=check_doc_in_db, text=text_from_file)

            db.add(new_entry_in_doc_text)

            db.commit()

    except Exception as e:
        print(f'ОШИБКА {e}')


def ocr_space_file(image_url, overlay=False, api_key='helloworld', language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(image_url, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={image_url: f},
                          data=payload,
                          )
    return r.content.decode()