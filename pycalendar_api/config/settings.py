from dataclasses import dataclass, field, fields
from typing import ClassVar

import httpx

from pycalendar_api.utils import get_http_client, get_http_client_async

from .base import ConfigSection
from .constants import CONSTANTS


@dataclass
class ApiConfig(ConfigSection):
    """Application Instance configuration. Litestar"""
    section: ClassVar = 'api'
    host: str = "https://calendar-api.ma"
    api_endpoint: str = "/api/v1"
    api_key: str = "UNDEFINED"
    timezone: str = CONSTANTS.TIMEZONE

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
    """Application Instance configuration. Litestar"""
    section: ClassVar = 'http-client'
    default_encoding: str = "utf-8"
    timeout: int = 10
    retries: int = 2
    verify: bool = False
    follow_redirects: bool = True


@dataclass
class Settings(ConfigSection):
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

    def create_http_client(self) -> httpx.Client:
        return get_http_client(
            base_url=self.api.api_base_url,
            headers=self.api.api_key_header,
            default_encoding=self.http_client.default_encoding,
            timeout=self.http_client.timeout,
            retries=self.http_client.retries,
            verify=self.http_client.verify,
            follow_redirects=self.http_client.follow_redirects,
        )

    def create_http_client_async(self) -> httpx.AsyncClient:
        return get_http_client_async(
            base_url=self.api.api_base_url,
            headers=self.api.api_key_header,
            default_encoding=self.http_client.default_encoding,
            timeout=self.http_client.timeout,
            retries=self.http_client.retries,
            verify=self.http_client.verify,
            follow_redirects=self.http_client.follow_redirects,
        )
