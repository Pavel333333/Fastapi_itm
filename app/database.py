from contextlib import contextmanager

from typing import AsyncGenerator
from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

if settings.MODE == 'DEV':

    DATABASE_URL_SYNC = settings.get_sync_db_url
    engine_sync = create_engine(DATABASE_URL_SYNC, echo=True)

    DATABASE_URL_ASYNC = settings.get_async_db_url
    engine_async = create_async_engine(DATABASE_URL_ASYNC, echo=True)

else:

    DATABASE_URL_SYNC_TEST = settings.get_sync_test_db_url
    engine_sync = create_engine(DATABASE_URL_SYNC_TEST, echo=True)

    DATABASE_URL_ASYNC_TEST = settings.get_async_test_db_url
    engine_async = create_async_engine(DATABASE_URL_ASYNC_TEST, poolclass=NullPool)


sync_session_maker = sessionmaker(bind=engine_sync, class_=Session)
async_session_maker = async_sessionmaker(bind=engine_async, class_=AsyncSession)


async def get_db_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker.begin() as async_session:
        yield async_session
        await async_session.commit()


@contextmanager
def get_db_sync_session():

    sync_session = sync_session_maker()
    try:
        yield sync_session
    finally:
        sync_session.close()