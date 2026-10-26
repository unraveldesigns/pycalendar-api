import inspect

import httpx
import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi, Settings
from pycalendar_api.config import CONSTANTS, ConfigurationError, load_settings
from pycalendar_api.domains.bdays import AsyncBDaysResource, BDaysResource
from pycalendar_api.utils import get_http_client, get_http_client_async

pytestmark = pytest.mark.client


@pytest.fixture(name='clear_settings_cache', autouse=True)
def fx_clear_settings_cache():
    load_settings.cache_clear()
    yield
    load_settings.cache_clear()


# ---- Constructors ----
def test_apikey_does_not_mutate_the_shared_config():
    config = Settings()
    api = CalendarApi('my-key', config=config)
    assert api.config.api.api_key == 'my-key'
    assert config.api.api_key == 'UNDEFINED'
    assert api.client.headers[CONSTANTS.AUTH_API_HEADER_KEY] == 'my-key'
    api.close()


def test_custom_host_is_used_by_the_client():
    config = Settings(api={'host': 'https://staging.example.test'})
    with CalendarApi('key', config=config) as api:
        assert str(api.client.base_url) == 'https://staging.example.test/api/v1/'
        assert api.h.host_url() == 'https://staging.example.test'
        assert api.openapi_schema_url == 'https://staging.example.test/schema/openapi.json'


def test_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(CONSTANTS.APPLICATION_APIKEY, 'env-key')
    with CalendarApi.from_env() as api:
        assert isinstance(api, CalendarApi)
        assert api.config.api.api_key == 'env-key'


def test_from_env_missing_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(CONSTANTS.APPLICATION_APIKEY, raising=False)
    with pytest.raises(ConfigurationError):
        CalendarApi.from_env()


def test_from_config_file(tmp_path):
    fpath = tmp_path / 'pycalendar-api.toml'
    Settings(api={'api_key': 'file-key'}).save_current_config(fpath)
    with CalendarApi.from_config_file(fpath) as api:
        assert api.config.api.api_key == 'file-key'


@pytest.mark.anyio
async def test_async_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(CONSTANTS.APPLICATION_APIKEY, 'env-key')
    async with AsyncCalendarApi.from_env() as api:
        assert isinstance(api, AsyncCalendarApi)
        assert isinstance(api.client, httpx.AsyncClient)
        assert api.client.headers[CONSTANTS.AUTH_API_HEADER_KEY] == 'env-key'
    assert api.client.is_closed


# ---- Sync / Async parity ----
@pytest.mark.parametrize(("sync_cls", "async_cls"), [(CalendarApi, AsyncCalendarApi), (BDaysResource, AsyncBDaysResource)])
def test_async_interface_mirrors_sync(sync_cls: type, async_cls: type):
    # Operations defined by the sync class itself, inherited helpers (endpoint_by_operation...) stay sync
    public = {name for name, attr in vars(sync_cls).items() if inspect.isfunction(attr) and not name.startswith('_')}
    assert public
    for name in public - {'close'}:
        assert inspect.iscoroutinefunction(getattr(async_cls, name)), f"{async_cls.__name__}.{name} must be async"


def test_context_manager_closes_the_client():
    with CalendarApi('key') as api:
        assert not api.client.is_closed
    assert api.client.is_closed


def test_repr():
    assert repr(CalendarApi('key')) == 'CalendarApi(base_url=https://calendar-api.ma/api/v1)'
    assert repr(AsyncCalendarApi('key')) == 'AsyncCalendarApi(base_url=https://calendar-api.ma/api/v1)'


# ---- HTTP clients ----
def test_http_clients_defaults():
    with get_http_client(base_url='https://example.test') as clt:
        assert clt.headers['X-CLIENT'] == 'pycalendar-api'
    aclt = get_http_client_async(base_url='https://example.test')
    assert aclt.headers['X-CLIENT'] == 'pycalendar-api'
    # httpx.AsyncClient event hooks must be coroutines
    assert all(inspect.iscoroutinefunction(hook) for hook in aclt.event_hooks['request'])
    # TLS verification must be on by default for both clients
    assert inspect.signature(get_http_client_async).parameters['verify'].default is True
