import logging
from datetime import date, timedelta

from rawg_pipeline.config.api import API_CONFIG
from rawg_pipeline.database.connection import create_db_engine
from rawg_pipeline.database.games import get_games_watermark, set_games_watermark
from rawg_pipeline.extract.rawg import (
    fetch_game_pages,
    fetch_genres,
    fetch_parent_platforms,
    fetch_platforms,
    fetch_stores,
)
from rawg_pipeline.load.games import (
    ensure_tables,
    insert_data_in_raw_games_table,
    insert_data_in_raw_genres_table,
    insert_data_in_raw_parent_platforms_table,
    insert_data_in_raw_platforms_table,
    insert_data_in_raw_stores_table,
)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    engine = create_db_engine()
    ensure_tables(engine)

    genres = fetch_genres()
    platforms = fetch_platforms()
    parent_platforms = fetch_parent_platforms()
    stores = fetch_stores()

    insert_data_in_raw_genres_table(engine, genres)
    insert_data_in_raw_platforms_table(engine, platforms)
    insert_data_in_raw_parent_platforms_table(engine, parent_platforms)
    insert_data_in_raw_stores_table(engine, stores)

    games_watermark = get_games_watermark(engine)
    if games_watermark is None:
        day = API_CONFIG.min_updated_date
    else:
        day = games_watermark + timedelta(days=1)

    yesterday = date.today() - timedelta(days=1)

    while day <= yesterday:
        game_pages = fetch_game_pages(day=day)
        for games in game_pages:
            insert_data_in_raw_games_table(engine, games)

        set_games_watermark(engine, day)
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
