from pathlib import Path

from .config import Settings, load_settings
from .domains.bdays import BDaysResource
from .domains.health import ApiHealth, HealthsResource
from .domains.holidays import HolidaysResource


class CalendarApi:

    def __init__(self, apikey: str=None, config: Settings=None, **kwargs):
        self.config = config or Settings()
        if apikey:
            self.config.api.api_key = apikey

        self.client = self.config.create_http_client()
        # ------ Domains APIs ------
        self.bdays = BDaysResource(self.client)
        self.holidays = HolidaysResource(self.client)
        self.h = HealthsResource(self.client)

    def __repr__(self):
        rv = f"CalendarApi(base_url={self.config.api.api_base_url})"
        return rv

    @classmethod
    def from_env(cls) -> "CalendarApi":
        """Uses the API-KEY defined in the environment variable

        Returns:
            CalendarApi: Configured instance
        """
        conf = load_settings(from_env=True)
        return cls(config=conf)

    @classmethod
    def from_config_file(cls, fpath: str) -> "CalendarApi":
        """Load the configuration from the toml file.

        Args:
            fpath (str): Configuration path

        Returns:
            CalendarApi: Configured instance
        """
        conf = Settings.from_config_file(fpath)
        return cls(config=conf)

    def openapi_schema(self, fpath: Path|str) -> Path:
        """Download the Openapi schema from `calendar-api.ma`

        Args:
            fpath (Path | str): Path to save the file
        """
        return self.config.openapi_schema(fpath)

    def health(self) -> ApiHealth:
        return self.h.api()
