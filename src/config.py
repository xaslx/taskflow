from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    fastapi_port: int = Field(alias='FASTAPI_PORT')

    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_db: str = Field(alias='POSTGRES_DB')
    postgres_host: str = Field(alias='POSTGRES_HOST')
    postgres_port: int = Field(alias='POSTGRES_PORT', default=5432)

    pgadmin_default_email: str = Field(alias='PGADMIN_DEFAULT_EMAIL')
    pgadmin_default_password: str = Field(alias='PGADMIN_DEFAULT_PASSWORD')

    jwt_secret_key: str = Field(alias='JWT_SECRET_KEY')
    refresh_secret_key: str = Field(alias='REFRESH_SECRET_KEY')
    algorithm: str = Field(alias='ALGORITHM')
    access_token_expire_minutes: int = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_days: int = Field(alias='REFRESH_TOKEN_EXPIRE_DAYS')

    model_config = SettingsConfigDict(env_file='.env')