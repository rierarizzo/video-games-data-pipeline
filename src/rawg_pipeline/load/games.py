import logging
from pathlib import Path

from sqlalchemy import bindparam, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def ensure_schema(engine: Engine) -> None:
    """Bring the database to the state the pipeline expects.

    Creates the control table ``etl_state``, the ``raw_*`` tables and the
    ``stg_*`` views. Call it once at startup, before extracting or loading
    anything.

    Safe to call on every run: every script is idempotent, so a second call
    leaves the database unchanged. All statements run inside a single
    transaction, so either every object is created or none is.

    Files in ``sql/`` are executed in ascending filename order, so the
    zero-padded numeric prefix defines dependency order: a script that reads
    from an object must have a higher prefix than the script that creates it.
    Each file must contain exactly one statement.

    Args:
        engine: Database engine used to reach the database.
    """
    sql_dir = Path("sql")
    sql_files = sorted(sql_dir.glob("*.sql"))

    if not sql_files:
        raise RuntimeError(f"No SQL scripts found in {sql_dir.resolve()}")

    with engine.begin() as connection:
        for sql_file in sql_files:
            logger.info("Executing SQL script %s", sql_file.name)
            connection.exec_driver_sql(sql_file.read_text(encoding="utf-8"))


def insert_data_in_raw_games_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_games table"""
    if not data:
        return

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


def insert_data_in_raw_stores_table(engine: Engine, data: list[dict]) -> None:
    """Insert data in raw_stores table"""
    rows = [{"id": genre["id"], "data": genre} for genre in data]

    logger.info("Inserting stores")

    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO raw_stores (id, data)
                    VALUES (:id, :data)
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data
                    WHERE raw_stores.data 
                    IS DISTINCT FROM EXCLUDED.data""").bindparams(
                bindparam("data", type_=JSONB)
            ),
            rows,
        )
