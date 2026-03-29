from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "IzvestNick Messenger API"
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "CHANGE_ME_TO_LONG_RANDOM_SECRET"
    JWT_ALG: str = "HS256"

    ACCESS_TOKEN_MINUTES: int = 30
    REFRESH_TOKEN_DAYS: int = 30

    DATABASE_URL: str = "sqlite:///./aurora.db"

    CORS_ORIGINS: str = "*"

    MEDIA_DIR: str = "./media"
    MAX_PROFILE_PHOTOS: int = 30


settings = Settings()
