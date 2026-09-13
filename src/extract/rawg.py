import requests
from src.config.api_config import APIConfig
import logging

logger = logging.getLogger(__name__)


def fetch_games(session: requests.Session, page: int = 1) -> dict:
    """Fetch a page of games from the RAWG API"""
    response = session.get(
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


def fetch_game_pages():
    """Fetch all games from all available RAWG API pages."""
    games = []
    page = 1

    with requests.Session() as session:
        while True:
            data = fetch_games(session, page)

            yield data["results"]

            logger.info(f"Fetched page {page} with {len(data["results"])} games")

            if not data.get("next"):
                break

            page += 1

    return games
