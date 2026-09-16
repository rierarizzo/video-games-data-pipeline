from datetime import datetime

from sqlalchemy import text
from sqlalchemy.engine import Engine


def get_existing_game_ids(engine: Engine) -> set[int]:
    """Get IDs of games already stored in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id FROM raw_games"))

        return set(result.scalars())


def get_latest_game_updated(engine: Engine) -> datetime | None:
    """Get latest game updated date already stored in the database"""
    with engine.connect() as connection:
        result = connection.execute(
            text("""SELECT MAX((data ->> 'updated')::timestamptz) AS last_updated
                        FROM raw_games;""")
        )

        return result.scalar()
