import io
import os.path
from pathlib import Path

import aiofiles
import pytest
import mimetypes

from httpx import AsyncClient

from sqlalchemy import select

from app.database import get_db_async_session, get_db_sync_session
from app.db.models import Document, DocumentText

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_FILES_DIR = BASE_DIR / "tests" / "test_files"

# @pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("url, file_name, status_code", [
    (str(TEST_FILES_DIR / 'gratis-png-yandex.png'),
     'gratis-png-yandex.png', 200),
    (str(TEST_FILES_DIR / 'd10c58e.jpeg'), 'd10c58e.jpeg', 200),
    (str(TEST_FILES_DIR / 'SOLID.jpg'), 'SOLID.jpg', 413),
])
async def test_upload_doc_file_too_large(url, file_name, status_code, ac: AsyncClient):

    async with aiofiles.open(url, 'rb') as f:
        file_data: bytes = await f.read()

    size = len(file_data)
    file = io.BytesIO(file_data)
    file.name = file_name
    content_type, _ = mimetypes.guess_type(file_name)

    response = await ac.post('http://localhost:8001/files/upload_doc', files={'file': (file_name, file, content_type)})

    assert response.status_code == status_code

@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("url, file_name, status_code", [
    (str(TEST_FILES_DIR / 'fgh.jpeg'), 'fgh.jpeg', 200),
    (str(TEST_FILES_DIR / 'Untitled Document 1'), 'Untitled Document 1', 415),
    (str(TEST_FILES_DIR / 'Основные команды Linux'), 'Основные команды Linux', 415),
])
async def test_upload_doc_file_image(url, file_name, status_code, ac: AsyncClient):

    async with aiofiles.open(url, 'rb') as f:
        file_data: bytes = await f.read()

    file = io.BytesIO(file_data)
    file.name = file_name

    content_type, _ = mimetypes.guess_type(file_name)

    response = await ac.post('http://localhost:8001/files/upload_doc',
                             files={'file': (file_name, file_data, content_type)})

    assert response.status_code == status_code

@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("url, file_name, status_code, must_in_db", [
    (str(TEST_FILES_DIR / 'SOLID.jpg'), 'SOLID.jpg', 413, False),
    (str(TEST_FILES_DIR / 'Untitled Document 1'), 'Untitled Document 1', 415, False),
    (str(TEST_FILES_DIR / 'solid.png'), 'solid.png', 200, True),
    (str(TEST_FILES_DIR / 'dbc582da9e391cca96f4ad0c978154f7.png'),
     'dbc582da9e391cca96f4ad0c978154f7.png', 200, True),
])
async def test_upload_doc_check_add_file_to_db(url, file_name, status_code, must_in_db, ac: AsyncClient):

    async with aiofiles.open(url, 'rb') as f:
        file_data: bytes = await f.read()

    file = io.BytesIO(file_data)
    file.name = file_name
    content_type, _ = mimetypes.guess_type(file_name)

    response = await ac.post('http://localhost:8001/files/upload_doc',
                             files={'file': (file_name, file, content_type)})

    async for db in get_db_async_session():
        query = await db.execute(select(Document).where(Document.path == f'/home/pavel/dev/fastapi_itm/'
                                                                         f'documents_for_tests/{file_name}'))
        existing_elem = query.scalars().first()
        assert (existing_elem is not None) == must_in_db

    assert response.status_code == status_code


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("id, status_code", [
    (4, 204),
    (5, 204),
    (10, 404),
])
async def test_doc_delete_file_from_db(id: int, status_code, ac: AsyncClient):

    url_files: list = []

    async for db in get_db_async_session():
        query = await db.execute(select(Document).where(Document.id == id))
        elem = query.scalars().first()
        if elem:
            url_files.append(elem.path)

    response = await ac.delete(f'http://localhost:8001/files/doc_delete/{id}')

    async for db in get_db_async_session():
        query = await db.execute(select(Document).where(Document.id == id))
        existing_elem = query.scalars().first()
        assert existing_elem == None

    for url in url_files:
        assert os.path.exists(url) == False

    assert response.status_code == status_code


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("id, text_load_to_db", [
    (1, True),
    (2, True),
    (3, True),
])
async def test_insert_text_in_db(id, text_load_to_db, ac: AsyncClient):

    response = await ac.post('http://localhost:8001/files/doc_analyze', json={'id': id})

    with get_db_sync_session() as db:
        query = db.execute(select(DocumentText).where(DocumentText.id == id))
        elem = query.scalars().first()
        assert (elem.text is not None) == True


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("id", [
    (1), (2), (3),
])
async def test_get_text_from_db(id, ac: AsyncClient):

    response = await ac.post(f'http://localhost:8001/files/get_text/{id}')

    assert response is not None