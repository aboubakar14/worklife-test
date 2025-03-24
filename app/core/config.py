from typing import Any, Optional, Union
from pydantic import (
    field_validator,
    PostgresDsn,
    ValidationInfo,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "technical-test"
    VERSION: str = "0.2.0"
    POSTGRES_SERVER: Optional[str] = "localhost"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: Optional[str] = "postgres"
    POSTGRES_DB: Optional[str] = "test_db"
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    model_config = SettingsConfigDict()

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER", "postgres"),
            password=values.data.get("POSTGRES_PASSWORD", "postgres"),
            host=values.data.get("POSTGRES_SERVER", "localhost"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
