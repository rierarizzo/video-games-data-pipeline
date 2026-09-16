import logging

from sqlalchemy import bindparam, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def ensure_raw_games_table(engine: Engine) -> None:
    """Create the raw_games table if it does not exist."""
    with engine.begin() as connection:
        connection.execute(
            text("""
                            CREATE TABLE IF NOT EXISTS raw_games (
                                id INTEGER PRIMARY KEY,
                                data JSONB NOT NULL,
                                extracted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                            );
                        """)
        )


def get_existing_game_ids(engine: Engine) -> set[int]:
    """Get IDs of games already stored in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id FROM raw_games"))

        return set(result.scalars())


def insert_data_in_raw_games_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_games table"""
    existing_game_ids = get_existing_game_ids(engine)
    rows = [
        {"id": game["id"], "data": game}
        for game in data
        if game["id"] not in existing_game_ids
    ]

    if len(rows) != 0:
        logger.info(
            f"Inserting from game #{rows[0]['id']} "
            f"to game #{rows[-1]['id']} into the database"
        )

        with engine.begin() as connection:
            connection.execute(
                text("""
                            INSERT INTO raw_games (id, data) 
                            VALUES (:id, :data)
                        """).bindparams(bindparam("data", type_=JSONB)),
                rows,
            )
    else:
        logger.info("There are no new records to insert into the database")
