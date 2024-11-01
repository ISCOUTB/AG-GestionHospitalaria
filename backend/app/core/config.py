import secrets
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, MongoDsn, computed_field

from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from os import getenv
from dotenv import load_dotenv

load_dotenv()

def parse_cors(v: Any) -> list[str] | str:
    """
    Función para analizar los valores de CORS, que pueden venir en formato de cadena o lista.

    Args:
        v (Any): Valor que puede ser una cadena o lista de orígenes permitidos.

    Returns:
        list[str] | str: Lista de orígenes permitidos, o la cadena original si ya es una lista o cadena.

    Raises:
        ValueError: Si el valor no es de tipo válido.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    API_V1_STR: str
    STACK_NAME: str
    PROJECT_NAME: str
    NBYTES: int

    SECRET_KEY: str = secrets.token_urlsafe(int(getenv('NBYTES')))

    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DOMAIN: str
    ENVIRONMENT: Literal["local", "staging", "production"]

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int

    @computed_field
    @property
    def MONGO_URI(self) -> MongoDsn:
        return MultiHostUrl.build(
            scheme="mongodb",
            username=self.MONGO_INITDB_ROOT_USERNAME,
            password=self.MONGO_INITDB_ROOT_PASSWORD,
            host=self.MONGO_HOST,
            port=self.MONGO_PORT,
        )


settings = Settings()
