from fastapi import APIRouter, UploadFile, Depends, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.celery_tasks import get_text_from_foto
from app.api.models_pydantic import DocDeleteRequest, ResponseModel
from app.database import get_db_async_session
from app.services.funcs_for_documents import FuncsForDocuments

router = APIRouter(prefix='/files', tags=['Files'])

@router.post('/upload_doc', summary='загрузка картинок',
             description='принимаем картинку, загружаем её в папку documents, добавляем запись с адресом картинки '
                         'на диске в таблицу Documents')
async def upload_doc(file: UploadFile = File(...), db: AsyncSession = Depends(get_db_async_session)):

    """Ручка принимает файлы, проверяет, что это картинки, и загружает на диск файлы и информацию о них в базу"""

    return await FuncsForDocuments.upload(file, db)

@router.delete('/doc_delete/{id}', summary='удаление картинок', description='ручка принимает id документа, '
                                                                            'удаляет его из базы и с диска')
async def delete_doc(id: int, db: AsyncSession = Depends(get_db_async_session)):

    """Ручка принимает один или несколько id картинок и удаляет их с диска и записи в базе"""

    return await FuncsForDocuments.delete(id, db)

@router.post('/doc_analyze', response_model=ResponseModel, summary='конвертация картинок в текст',
             description='ручка принимает id документа, передаёт задание в селери, где с картинки считывается текст '
                         'и записывается в базу в таблицу DocumentText')
def insert_text_in_db(request: DocDeleteRequest, background_tasks: BackgroundTasks):
    """
    Эндпоинт для запуска задачи анализа текста на изображении.
    Принимает id документа и отправляет задачу в Celery через background_tasks.
    """
    id = request.id  # Извлекаем id из запроса
    # Запускаем задачу Celery асинхронно через background_tasks
    background_tasks.add_task(get_text_from_foto.delay, id)
    # Возвращаем подтверждение клиенту
    return ResponseModel(message='Задача отправлена', detail='Текст с картинки считывается и будет записан в базу')


@router.get('/get_text/{id}', summary='выдача текста из базы',
             description='ручка принимает id_doc документа и возвращает текст из DocumentText')
async def get_text(id: int, db: AsyncSession = Depends(get_db_async_session)):

    """Ручка принимает один или несколько id файлов и выдаёт текст(-ы) из базы"""

    return await FuncsForDocuments.get_text(id, db)