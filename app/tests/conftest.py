import os

import pytest
import pytest_asyncio

from app.config import settings
from app.db.models import Base, Document, DocumentText
from app.database import engine_async
from app.main import app
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope='session', autouse=True)
async def clean_test_database():

    assert settings.MODE == "TEST"

    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest_asyncio.fixture(scope='function')
async def ac():

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        print(f" 🐝 Using ac fixture")
        yield ac
        await ac.aclose() # у Шумейко этого нет

@pytest.fixture(scope='session')
def app_url():
    url = os.getenv("APP_URL", "http://localhost:8001")
    print(f" 👀 Using APP_URL: {url}")
    return url # os.getenv("APP_URL", "http://localhost:8001")  # Дефолт для локального запуска

# @pytest.fixture(scope='function')
# def tc():
#     with TestClient(app) as tc:
#         yield tc