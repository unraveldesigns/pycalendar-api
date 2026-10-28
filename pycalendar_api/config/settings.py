from dataclasses import dataclass, field, fields, replace
from typing import ClassVar, TypedDict

import httpx

from pycalendar_api.utils import get_http_client, get_http_client_async

from .base import ConfigSection
from .constants import CONSTANTS


@dataclass
class ApiConfig(ConfigSection):
    """API server config section"""
    section: ClassVar = 'api'
    host: str = "https://calendar-api.ma"
    api_endpoint: str = "/api/v1"
    api_key: str = "UNDEFINED"

    @property
    def api_base_url(self) -> str:
        return f"{self.host}/{self.api_endpoint.lstrip('/')}"

    @property
    def api_key_header(self) -> dict:
        if self.api_key:
            return {CONSTANTS.AUTH_API_HEADER_KEY: self.api_key}
        return {}


@dataclass
class HTTPClientConfig(ConfigSection):
    """HTTP client config section (`[http_client]` in the toml file). Every field is an option of `get_http_client`

    Attributes:
        default_encoding: Encoding of the responses without charset
        timeout: Connect/write/pool timeout in seconds
        read_timeout: Read timeout in seconds. Default: `timeout * 5`
        retries: Retries on connection errors
        verify: Verify the server certificate (`true`/`false`), or path to a CA bundle file or directory
        cert: Client certificate file (PEM), for mutual TLS
        cert_key: Private key file of `cert`, when not included in it
        proxy: Proxy URL, ie: `http://user:pass@proxy:3128`
        trust_env: When `proxy` is not set, use `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` / `NO_PROXY`.
            When `verify=true`, use `SSL_CERT_FILE` / `SSL_CERT_DIR`
        follow_redirects: Follow the HTTP redirects
    """
    section: ClassVar = 'http_client'
    default_encoding: str = "utf-8"
    timeout: float = 10
    read_timeout: float | None = None
    retries: int = 3
    verify: bool | str = True
    cert: str | None = None
    cert_key: str | None = None
    proxy: str | None = None
    trust_env: bool = True
    follow_redirects: bool = True

    def override(self, **options) -> "HTTPClientConfig":
        """Copy of this section with some options replaced

        Raises:
            TypeError: Unknown option
        """
        unknown = set(options) - {f.name for f in fields(self)}
        if unknown:
            msg = f"Unknown HTTP client option(s) {sorted(unknown)}. Valid options: {[f.name for f in fields(self)]}"
            raise TypeError(msg)
        return replace(self, **options)


class HTTPClientOptions(TypedDict, total=False):
    """Keyword arguments accepted by `CalendarApi` / `AsyncCalendarApi` to override `HTTPClientConfig`"""
    default_encoding: str
    timeout: float
    read_timeout: float | None
    retries: int
    verify: bool | str
    cert: str | None
    cert_key: str | None
    proxy: str | None
    trust_env: bool
    follow_redirects: bool


@dataclass
class Settings(ConfigSection):
    """pycalendar_api client config file"""
    section: ClassVar = 'root'
    api: ApiConfig = field(default_factory=ApiConfig)
    http_client: HTTPClientConfig = field(default_factory=HTTPClientConfig)

    def __post_init__(self):
        """One level config File"""
        for f in fields(self):
            attr = getattr(self, f.name)
            if isinstance(attr, dict):
                instance = f.type(**attr)
                setattr(self, f.name, instance)

    def create_http_client(self, transport: httpx.BaseTransport=None, client_kwargs: dict=None) -> httpx.Client:
        return get_http_client(
            transport=transport,
            base_url=self.api.api_base_url,
            headers=self.api.api_key_header,
            **self.http_client.to_dict(),
            **(client_kwargs or {}),
        )

    def create_http_client_async(self, transport: httpx.AsyncBaseTransport=None, client_kwargs: dict=None) -> httpx.AsyncClient:
        return get_http_client_async(
            transport=transport,
            base_url=self.api.api_base_url,
            headers=self.api.api_key_header,
            **self.http_client.to_dict(),
            **(client_kwargs or {}),
        )
