import os
from typing import Literal

import httpx
import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi
from pycalendar_api.config import CONSTANTS
from pycalendar_api.domains.urls import ENDPOINTS

ChoicesScope = Literal['function', 'class', 'module', 'package', 'session']

FAKE_APIKEY = "test-apikey"


# ---- Live API (needs the PYCALENDAR_APIKEY environment variable) ----
@pytest.fixture(scope="session", name='api_client')
def fx_client():
    if not os.environ.get(CONSTANTS.APPLICATION_APIKEY):
        pytest.skip(f"Live test: `{CONSTANTS.APPLICATION_APIKEY}` environment variable not defined")
    with CalendarApi.from_env() as api:
        yield api


@pytest.fixture(name='async_api_client')
async def fx_async_client():
    if not os.environ.get(CONSTANTS.APPLICATION_APIKEY):
        pytest.skip(f"Live test: `{CONSTANTS.APPLICATION_APIKEY}` environment variable not defined")
    async with AsyncCalendarApi.from_env() as api:
        yield api


@pytest.fixture(scope="session", name='endpoints')
def fx_endpoints():
    endpoints = ENDPOINTS.copy()
    return endpoints


@pytest.fixture(scope="session", name='constants')
def fx_constants():
    return CONSTANTS


@pytest.fixture(scope="session")
def anyio_backend():
    """Async tests run with the anyio pytest plugin (shipped with httpx) on asyncio only"""
    return "asyncio"


# ---- Offline API: the real clients plugged on an `httpx.MockTransport` ----
class FakeServer:
    """Minimal Calendar API double. Routes are `path -> (status_code, json_payload)`, requests are recorded."""

    def __init__(self):
        self.routes: dict[str, tuple[int, object]] = {}
        self.requests: list[httpx.Request] = []

    def route(self, path: str, payload: object, status_code: int = 200):
        self.routes[path] = (status_code, payload)

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        try:
            status_code, payload = self.routes[request.url.path]
        except KeyError:
            return httpx.Response(404, json={"detail": f"Not Found {request.url.path}"})
        return httpx.Response(status_code, json=payload)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


@pytest.fixture(name='fake_server')
def fx_fake_server() -> FakeServer:
    return FakeServer()


@pytest.fixture(name='fake_api')
def fx_fake_api(fake_server: FakeServer):
    with CalendarApi(FAKE_APIKEY, transport=httpx.MockTransport(fake_server)) as api:
        yield api


@pytest.fixture(name='fake_async_api')
async def fx_fake_async_api(fake_server: FakeServer):
    async with AsyncCalendarApi(FAKE_APIKEY, transport=httpx.MockTransport(fake_server)) as api:
        yield api
