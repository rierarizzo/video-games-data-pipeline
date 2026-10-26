from datetime import date

from sqlalchemy import text
from sqlalchemy.engine import Engine

SOURCE = "rawg_games"


def get_games_watermark(engine: Engine) -> date | None:
    """Return the last day of games fully processed by the pipeline.

    The watermark lives in ``etl_state`` under the ``rawg_games`` source.
    ``None`` means no day has been completed yet, so the caller must bootstrap
    from a configured start date instead of assuming an empty range.

    Args:
        engine: Database engine used to reach the ``etl_state`` table.

    Returns:
        The last completed day, or ``None`` if no watermark is set.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("""SELECT last_completed_day FROM etl_state 
                    WHERE source=:source;"""),
            {"source": SOURCE},
        )

        return result.scalar_one_or_none()


def set_games_watermark(engine: Engine, day: date) -> None:
    """Mark ``day`` as fully processed for the games source.

    Upserts the ``rawg_games`` watermark in ``etl_state``. Call it only after
    every page of ``day`` has been stored: the watermark is the promise that
    lets the next run skip that day without losing data.

    Args:
        engine: Database engine used to reach the ``etl_state`` table.
        day: Last day whose games were completely loaded.
    """
    with engine.begin() as connection:
        connection.execute(
            text("""INSERT INTO etl_state (source, last_completed_day) 
                VALUES (:source, :day)
                ON CONFLICT (source) DO UPDATE
                SET last_completed_day = EXCLUDED.last_completed_day;"""),
            {"source": SOURCE, "day": day},
        )
