import logging

from sqlalchemy import bindparam, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def ensure_raw_games_table(engine: Engine) -> None:
    """Create the raw_games table if it does not exist."""
    with engine.begin() as connection:
        connection.execute(
            text("""CREATE TABLE IF NOT EXISTS raw_games (
                    id INTEGER PRIMARY KEY,
                    data JSONB NOT NULL,
                    extracted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )


def insert_data_in_raw_games_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_games table"""
    rows = [{"id": game["id"], "data": game} for game in data]

    logger.info(
        "Inserting games updated from %s to %s",
        rows[0]["data"]["updated"],
        rows[-1]["data"]["updated"],
    )

    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO raw_games (id, data) 
                    VALUES (:id, :data)
                    ON CONFLICT (id) DO NOTHING""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )
