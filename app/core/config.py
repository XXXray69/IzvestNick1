from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    APP_NAME: str = 'IzvestNick'
    API_V1_PREFIX: str = '/api/v1'

    SECRET_KEY: str = 'CHANGE_ME_TO_LONG_RANDOM_SECRET'
    JWT_ALG: str = 'HS256'

    ACCESS_TOKEN_MINUTES: int = 30
    REFRESH_TOKEN_DAYS: int = 30

    DATABASE_URL: str = 'sqlite:///./izvestnick.db'

    CORS_ORIGINS: str = 'http://localhost:3000,http://127.0.0.1:3000'
    MEDIA_DIR: str = './media'
    MAX_PROFILE_PHOTOS: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(',') if x.strip()]


settings = Settings()
