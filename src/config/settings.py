from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    APP_NAME: str = 'Cooking Calculator'
    APP_VERSION: str = '0.1'

    API_PREFIX: str = "/v1"

    SECRET_KEY: str

    LOGGING_LEVEL: str = 'INFO'

    SERVER_PORT: int = 8000
    SERVER_WORKER_NUMBER: int = 4

    DATABASE_URL: PostgresDsn | None = None
    TEST_DATABASE_URL: PostgresDsn | None = None

    ENABLE_SQL_ECHO: bool | None = True
    ENABLE_WEB_SERVER_AUTORELOAD: bool | None = True

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
