import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DBConfig:
    """Database configuration for PostgreSQL connection."""

    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    database: str = os.getenv("DB_NAME", "videogames")
    args: str = os.getenv("DB_ARGS", "")
    user: str = os.getenv("DB_USER", "")
    password: str = os.getenv("DB_PASSWORD", "")

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


DB_CONFIG = DBConfig()
