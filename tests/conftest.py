from typing import Literal

import pytest

from pycalendar_api import CalendarApi
from pycalendar_api.config import CONSTANTS
from pycalendar_api.domains.urls import ENDPOINTS

ChoicesScope = Literal['function', 'class', 'module', 'package', 'session']

@pytest.fixture(scope="session", name='api_client')
def fx_client():
    return CalendarApi.from_env()


@pytest.fixture(scope="session", name='endpoints')
def fx_endpoints():
    endpoints = ENDPOINTS.copy()
    return endpoints


@pytest.fixture(scope="session", name='constants')
def fx_constants():
    return CONSTANTS
