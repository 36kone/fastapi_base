from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE: int = 0
    OTEL_SERVICE_NAME: str = ""
    OTEL_COLLECTOR_LOGS: str = ""
    BUCKET_ENDPOINT: str = ""
    BUCKET_ACCESS_KEY: str = ""
    BUCKET_SECRET: str = ""
    BUCKET_NAME: str = ""
    ECOMMERCE_URL: str = ""
    MAIL_HOST: str = ""
    MAIL_PORT: int = 0
    MAIL_SECURE: bool = False
    MAIL_USER: str = ""
    MAIL_PASS: SecretStr = SecretStr("")
    MAIL_FROM: str = ""


settings = Settings()