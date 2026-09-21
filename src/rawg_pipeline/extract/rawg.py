import logging
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from rawg_pipeline.config.api import API_CONFIG

logger = logging.getLogger(__name__)


def fetch_games(
    session: requests.Session, from_date: datetime | None, page: int = 1
) -> dict:
    """Fetch a page of games from the RAWG API"""
    params = {
        "key": API_CONFIG.api_key,
        "ordering": API_CONFIG.ordering,
        "page_size": API_CONFIG.max_per_page,
        "page": page,
    }

    if from_date is not None:
        params["updated"] = f"{from_date:%Y-%m-%d},{API_CONFIG.max_date:%Y-%m-%d}"

    response = session.get(
        url=API_CONFIG.games_url,
        params=params,
        timeout=API_CONFIG.timeout_seconds,
    )

    response.raise_for_status()

    return response.json()


def fetch_game_pages(from_date: datetime | None):
    """Fetch all games from all available RAWG API pages."""
    page = 1
    last_inserted_date: datetime | None = None

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
            # Workaround: RAWG API consistely returns 404 when requesting page 251.
            if page == 251:
                page = 1
                from_date = last_inserted_date

            data = fetch_games(session, from_date, page)
            logger.info(
                f"Fetched page {page} with {len(data['results'])} "
                f"(from_date={from_date.isoformat() if from_date else None})"
            )
            yield data["results"]

            if not data.get("next"):
                break

            last_inserted_date = datetime.fromisoformat(data["results"][-1]["updated"])
            page += 1
