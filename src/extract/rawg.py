from sqlalchemy.engine import Engine
from sqlalchemy import text
import requests
from src.config.api_config import APIConfig


def ensure_raw_games_table(engine: Engine) -> None:
    """Create the raw_games table if it does not exist."""
    with engine.begin() as connection:
        connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS raw_games (
                                id INTEGER PRIMARY KEY,
                                data JSONB NOT NULL,
                                extracted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                            );
                        """))


def get_existing_game_ids(engine: Engine) -> set[int]:
    """Get IDs of games already stored in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id FROM raw_games"))

        return set(result.scalars())


def fetch_games(page: int = 1) -> dict:
    """Fetch a page of games from the RAWG API"""
    response = requests.get(
        url=APIConfig.games_url,
        params={
            "key": APIConfig.api_key,
            "page": page,
            "page_size": APIConfig.max_per_page,
        },
        timeout=APIConfig.timeout_seconds,
    )

    response.raise_for_status()

    return response.json()


def fetch_all_games() -> list[dict]:
    """Fetch all games from all available RAWG API pages."""
    games = []
    page = 1

    while True:
        data = fetch_games(page)
        print(data)
        games.extend(data["results"])

        if not data.get("next"):
            break

        page += 1

    return games
