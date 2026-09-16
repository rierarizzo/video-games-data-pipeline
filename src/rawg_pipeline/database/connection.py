from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from rawg_pipeline.config.database import DB_CONFIG


def create_db_engine() -> Engine:
    return create_engine(DB_CONFIG.url)
