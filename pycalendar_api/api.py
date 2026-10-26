from pathlib import Path
from typing import Self

import httpx

from .config import CONSTANTS, Settings, load_settings
from .domains.bdays import AsyncBDaysResource, BDaysResource
from .domains.health import ApiHealth, AsyncHealthsResource, HealthsResource
from .domains.holidays import AsyncHolidaysResource, HolidaysResource


class _BaseCalendarApi:
    """Configuration and constructors shared by `CalendarApi` and `AsyncCalendarApi`"""

    def __init__(self, apikey: str=None, config: Settings=None, *, transport=None, **kwargs):
        self.config = config or Settings()
        if apikey:
            # Do not mutate a shared (possibly cached by `load_settings`) configuration
            self.config = self.config.duplicate()
            self.config.api.api_key = apikey

        self.client = self._create_client(transport)

    def _create_client(self, transport=None) -> httpx.Client | httpx.AsyncClient:
        raise NotImplementedError

    def __repr__(self):
        rv = f"{self.__class__.__name__}(base_url={self.config.api.api_base_url})"
        return rv

    @classmethod
    def from_env(cls) -> Self:
        """Uses the API-KEY defined in the environment variable

        Returns:
            Self: Configured instance
        """
        conf = load_settings(from_env=True)
        return cls(config=conf)

    @classmethod
    def from_config_file(cls, fpath: str) -> Self:
        """Load the configuration from the toml file.

        Args:
            fpath (str): Configuration path

        Returns:
            Self: Configured instance
        """
        conf = Settings.from_config_file(fpath)
        return cls(config=conf)

    @property
    def openapi_schema_url(self) -> str:
        """URL of the Openapi schema (`openapi.json`), served at the host root"""
        return self.config.api.host.rstrip("/") + CONSTANTS.OPENAPI_SCHEMA_ENDPOINT

    @staticmethod
    def _save_openapi_schema(response: httpx.Response, fpath: Path|str) -> Path:
        response.raise_for_status()
        fpath = Path(fpath).absolute()
        fpath.write_bytes(response.content)
        return fpath


class CalendarApi(_BaseCalendarApi):
    """Sync client of Calendar API.

    Can be used as a context manager to close the underlying HTTP connections:

        with CalendarApi.from_env() as api:
            api.health()
    """
    client: httpx.Client

    def __init__(self, apikey: str=None, config: Settings=None, *, transport: httpx.BaseTransport=None, **kwargs):
        super().__init__(apikey=apikey, config=config, transport=transport, **kwargs)
        # ------ Domains APIs ------
        self.bdays = BDaysResource(self.client)
        self.holidays = HolidaysResource(self.client)
        self.h = HealthsResource(self.client)

    def _create_client(self, transport: httpx.BaseTransport=None) -> httpx.Client:
        return self.config.create_http_client(transport=transport)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info):
        self.close()

    def close(self):
        """Close the underlying HTTP connections"""
        self.client.close()

    def health(self) -> ApiHealth:
        return self.h.api()

    def openapi_schema(self, fpath: Path|str) -> Path:
        """Download the Openapi schema from `calendar-api.ma`

        Args:
            fpath (Path | str): Path to save the file

        Returns:
            Path: Absolute path of the saved file
        """
        return self._save_openapi_schema(self.client.get(self.openapi_schema_url), fpath)


class AsyncCalendarApi(_BaseCalendarApi):
    """Async client of Calendar API. Exposes the same domains as `CalendarApi`, their operations are awaitable.

    Can be used as an async context manager to close the underlying HTTP connections:

        async with AsyncCalendarApi.from_env() as api:
            await api.health()
    """
    client: httpx.AsyncClient

    def __init__(self, apikey: str=None, config: Settings=None, *, transport: httpx.AsyncBaseTransport=None, **kwargs):
        super().__init__(apikey=apikey, config=config, transport=transport, **kwargs)
        # ------ Domains APIs ------
        self.bdays = AsyncBDaysResource(self.client)
        self.holidays = AsyncHolidaysResource(self.client)
        self.h = AsyncHealthsResource(self.client)

    def _create_client(self, transport: httpx.AsyncBaseTransport=None) -> httpx.AsyncClient:
        return self.config.create_http_client_async(transport=transport)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info):
        await self.aclose()

    async def aclose(self):
        """Close the underlying HTTP connections"""
        await self.client.aclose()

    async def health(self) -> ApiHealth:
        return await self.h.api()

    async def openapi_schema(self, fpath: Path|str) -> Path:
        """Download the Openapi schema from `calendar-api.ma`. See `CalendarApi.openapi_schema`"""
        return self._save_openapi_schema(await self.client.get(self.openapi_schema_url), fpath)
