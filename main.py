from src.extract.rawg import fetch_game_pages
from src.db import create_db_engine
from src.load.database import ensure_raw_games_table, insert_data_in_raw_games_table
import logging


def main():
    # Setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    engine = create_db_engine()

    # Extract
    game_pages = fetch_game_pages()

    # Load
    ensure_raw_games_table(engine)
    for games in game_pages:
        insert_data_in_raw_games_table(engine, games)


if __name__ == "__main__":
    main()
