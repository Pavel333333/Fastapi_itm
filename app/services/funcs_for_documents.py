import os
import shutil

from fastapi import UploadFile, File, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from starlette import status
from starlette.responses import JSONResponse, Response

from app.config import settings
from app.database import get_db_async_session
from app.db.models import Document, DocumentText


class FuncsForDocuments:

    @staticmethod
    def check_files_size(file: UploadFile = File(...)):

        if file.size > 100 * 1024:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='файл больше 100кб')

    @staticmethod
    def check_files_type(file: UploadFile = File(...)):

        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='здесь ходят только картинки')

    @staticmethod
    def check_folder_documents(folder):

        if not os.path.isdir(folder):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='папка documents не найдена')

    @staticmethod
    async def check_elem_in_db_by_path(db_table_name, upload_file_path: str, db: AsyncSession):

        query = await db.execute(select(db_table_name).where(db_table_name.path == upload_file_path))
        existing_elem = query.scalars().first()

        if existing_elem:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Такая запись уже существует')

    @classmethod
    async def upload(cls, file: UploadFile = File(...), db: AsyncSession = get_db_async_session):

        cls.check_files_size(file)

        cls.check_files_type(file)

        if settings.MODE == 'DEV':
            upload_folder = os.path.join(os.getcwd(), 'documents')
        else:
            upload_folder = os.path.join(os.getcwd(), 'documents_for_tests')

        cls.check_folder_documents(upload_folder)

        upload_file_path = os.path.join(upload_folder, file.filename)

        with open(upload_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        await cls.check_elem_in_db_by_path(Document, upload_file_path, db)

        new_file = Document(path=upload_file_path)

        db.add(new_file)

        return JSONResponse(content='Файл загружен в папку documents на диске и создана запись в базе',
                            status_code=status.HTTP_200_OK)


    @staticmethod
    async def check_elem_in_db_by_id(db_table_name, id: int, db: AsyncSession):

        query_elem = await db.execute(select(db_table_name).where(db_table_name.id == id))
        elem = query_elem.scalars().first()

        if not elem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой записи нет в базе данных')

        return elem


    @classmethod
    async def delete(cls, id: int, db: AsyncSession = get_db_async_session):

        elem_for_del = await cls.check_elem_in_db_by_id(Document, id, db)

        elem_for_del_path: Mapped[str] = elem_for_del.path

        await db.delete(elem_for_del)

        os.remove(elem_for_del_path)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


    @classmethod
    async def get_text(cls, id: int, db: AsyncSession = get_db_async_session):

        elem_for_get_text = await cls.check_elem_in_db_by_id(DocumentText, id, db)

        text = elem_for_get_text.text

        return Response(content=text, status_code=status.HTTP_200_OK, media_type="text/plain")

