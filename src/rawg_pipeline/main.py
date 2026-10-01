import logging

from rawg_pipeline.database.connection import create_db_engine
from rawg_pipeline.database.games import get_latest_game_updated
from rawg_pipeline.extract.rawg import (
    fetch_game_pages,
    fetch_genres,
    fetch_parent_platforms,
    fetch_platforms,
)
from rawg_pipeline.load.games import (
    ensure_raw_tables,
    insert_data_in_raw_games_table,
    insert_data_in_raw_genres_table,
    insert_data_in_raw_parent_platforms_table,
    insert_data_in_raw_platforms_table,
)


def main():
    # Setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    engine = create_db_engine()
    ensure_raw_tables(engine)

    # Extract
    last_updated = get_latest_game_updated(engine)
    game_pages = fetch_game_pages(from_date=last_updated)
    genres = fetch_genres()
    platforms = fetch_platforms()
    parent_platforms = fetch_parent_platforms()

    # Load
    insert_data_in_raw_genres_table(engine, genres)
    insert_data_in_raw_platforms_table(engine, platforms)
    insert_data_in_raw_parent_platforms_table(engine, parent_platforms)
    for games in game_pages:
        insert_data_in_raw_games_table(engine, games)


if __name__ == "__main__":
    main()
