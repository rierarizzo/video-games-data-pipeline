from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIConfig:
    """API configuration for RAWG data fetching."""

    use_mock: bool = True
    api_key: str = os.getenv("RAWG_API_KEY", "")
    base_url: str = "https://api.rawg.io/api"
    games_url: str = f"{base_url}/games"
    max_per_page: int = 40
    timeout_seconds: int = 30

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_per_page <= 0:
            raise ValueError("max_per_page must be positive")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


API_CONFIG = APIConfig()
