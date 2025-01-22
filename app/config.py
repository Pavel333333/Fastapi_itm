from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST']

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


    @property
    def get_async_db_url(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @property
    def get_sync_db_url(self):
        return (f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str


    @property
    def get_async_test_db_url(self):
        return (f'postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@'
                f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}')

    @property
    def get_sync_test_db_url(self):
        return (f'postgresql+psycopg2://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@'
                f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}')

    model_config = SettingsConfigDict(env_file='.env')

# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# logger.info("DB_USER: %s", settings.DB_USER)
# logger.info("DB_PASSWORD: %s", settings.DB_PASSWORD)
# logger.info("DB_HOST: %s", settings.DB_HOST)
# logger.info("DB_PORT: %s", settings.DB_PORT)
# logger.info("DB_NAME: %s", settings.DB_NAME)

settings = Settings()