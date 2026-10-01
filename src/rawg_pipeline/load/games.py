import logging
from pathlib import Path

from sqlalchemy import bindparam, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def ensure_raw_tables(engine: Engine) -> None:
    """Create the raw_games table if it does not exist."""
    raw_games_sql = Path("sql/001_create_raw_games.sql").read_text(encoding="utf-8")
    raw_genres_sql = Path("sql/002_create_raw_genres.sql").read_text(encoding="utf-8")
    raw_platforms_sql = Path("sql/003_create_raw_platforms.sql").read_text(
        encoding="utf-8"
    )
    raw_parent_platforms_sql = Path(
        "sql/004_create_raw_parent_platforms.sql"
    ).read_text(encoding="utf-8")

    with engine.begin() as connection:
        connection.exec_driver_sql(raw_games_sql)
        connection.exec_driver_sql(raw_genres_sql)
        connection.exec_driver_sql(raw_platforms_sql)
        connection.exec_driver_sql(raw_parent_platforms_sql)


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
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data
                    WHERE raw_games.data IS DISTINCT FROM EXCLUDED.data""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )


def insert_data_in_raw_genres_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_genres table"""
    rows = [{"id": genre["id"], "data": genre} for genre in data]

    logger.info("Inserting genres")

    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO raw_genres (id, data)
                    VALUES (:id, :data)
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data
                    WHERE raw_genres.data IS DISTINCT FROM EXCLUDED.data""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )


def insert_data_in_raw_platforms_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_platforms table"""
    rows = [{"id": genre["id"], "data": genre} for genre in data]

    logger.info("Inserting platforms")

    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO raw_platforms (id, data)
                    VALUES (:id, :data)
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data
                    WHERE raw_platforms.data 
                    IS DISTINCT FROM EXCLUDED.data""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )


def insert_data_in_raw_parent_platforms_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_parent_platforms table"""
    rows = [{"id": genre["id"], "data": genre} for genre in data]

    logger.info("Inserting parent platforms")

    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO raw_parent_platforms (id, data)
                    VALUES (:id, :data)
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data
                    WHERE raw_parent_platforms.data 
                    IS DISTINCT FROM EXCLUDED.data""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )
