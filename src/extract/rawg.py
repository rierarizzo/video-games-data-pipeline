import requests
from src.config.api_config import APIConfig
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


def fetch_games(session: requests.Session, page: int = 1) -> dict:
    """Fetch a page of games from the RAWG API"""
    response = session.get(
        url=APIConfig.games_url,
        params={
            "key": APIConfig.api_key,
            "page": page,
            "page_size": APIConfig.max_per_page,
            "ordering": APIConfig.ordering,
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
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        while True:
            data = fetch_games(session, page)
            logger.info(f"Fetched page {page} with {len(data["results"])} games")
            yield data["results"]

            if not data.get("next"):
                break

            page += 1

    return games
