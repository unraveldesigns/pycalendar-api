"""HTTP client configuration: `[http_client]` section, client overrides, proxies and TLS"""
import inspect
import ssl
import typing
from pathlib import Path

import certifi
import httpcore
import httpx
import pytest

from pycalendar_api import AsyncCalendarApi, CalendarApi, HTTPClientConfig, Settings
from pycalendar_api.config import HTTPClientOptions, load_settings
from pycalendar_api.utils import get_http_client, get_http_client_async
from pycalendar_api.utils.http_client import build_ssl_context, resolve_proxy

from .conftest import FakeServer

pytestmark = pytest.mark.client

PROXY = "http://user:pass@proxy.test:3128"
ENV_PROXY = "http://env-proxy.test:8080"
PROXY_ENV_VARS = ('HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY', 'REQUEST_METHOD')


@pytest.fixture(name='clean_env', autouse=True)
def fx_clean_env(monkeypatch: pytest.MonkeyPatch):
    """Isolate the tests from the proxy variables of the machine running them"""
    for var in PROXY_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
        monkeypatch.delenv(var.lower(), raising=False)
    load_settings.cache_clear()
    yield monkeypatch
    load_settings.cache_clear()


def pool_of(client: httpx.Client | httpx.AsyncClient):
    """httpcore pool of the client transport"""
    return client._transport._pool


def is_proxied(client: httpx.Client | httpx.AsyncClient) -> bool:
    return isinstance(pool_of(client), (httpcore.HTTPProxy, httpcore.AsyncHTTPProxy))


# ---- Config section ----
def test_options_match_the_client_factories():
    """Every config field is an option of both factories, and a client override"""
    options = set(HTTPClientConfig().to_dict())
    assert options == set(typing.get_type_hints(HTTPClientOptions))
    for factory in (get_http_client, get_http_client_async):
        params = inspect.signature(factory).parameters
        assert options <= set(params)
        for name in options:
            assert params[name].default == getattr(HTTPClientConfig, name), f"{factory.__name__}({name}=) default differs"


def test_override_returns_a_copy():
    conf = HTTPClientConfig()
    new = conf.override(timeout=30, proxy=PROXY)
    assert (new.timeout, new.proxy) == (30, PROXY)
    assert (conf.timeout, conf.proxy) == (10, None)


def test_override_rejects_unknown_options():
    with pytest.raises(TypeError, match="proxies"):
        HTTPClientConfig().override(proxies=PROXY)


def test_toml_round_trip(tmp_path):
    fpath = tmp_path / 'pycalendar-api.toml'
    Settings(http_client={'proxy': PROXY, 'verify': certifi.where(), 'timeout': 2.5}).save_current_config(fpath)
    conf = Settings.from_config_file(fpath).http_client
    assert (conf.proxy, conf.verify, conf.timeout) == (PROXY, certifi.where(), 2.5)
    assert conf.cert is None, "Unset options must be read back as None"


# ---- Client overrides ----
@pytest.mark.parametrize("api_cls", [CalendarApi, AsyncCalendarApi])
def test_client_overrides(api_cls: type):
    config = Settings()
    api = api_cls('key', config=config, proxy=PROXY, timeout=30, read_timeout=60)
    assert api.config.http_client.proxy == PROXY
    assert config.http_client.proxy is None, "Overrides must not mutate the given config"
    assert is_proxied(api.client)
    assert api.client.timeout == httpx.Timeout(30, read=60)


def test_overrides_without_apikey_do_not_mutate_the_cached_settings(clean_env: pytest.MonkeyPatch):
    clean_env.setenv('PYCALENDAR_APIKEY', 'env-key')
    with CalendarApi.from_env(proxy=PROXY) as api:
        assert api.config.http_client.proxy == PROXY
    assert load_settings(from_env=True).http_client.proxy is None


def test_from_config_file_overrides_the_file(tmp_path):
    fpath = tmp_path / 'pycalendar-api.toml'
    Settings(http_client={'timeout': 5, 'retries': 1}).save_current_config(fpath)
    with CalendarApi.from_config_file(fpath, retries=5) as api:
        assert (api.config.http_client.timeout, api.config.http_client.retries) == (5, 5)


def test_unknown_option_raises():
    with pytest.raises(TypeError, match="Valid options"):
        CalendarApi('key', proxies=PROXY)


def test_client_kwargs(fake_server: FakeServer):
    """Extra httpx arguments are passed through, user event hooks run after the default ones"""
    responses = []
    fake_server.route('/health', {'api_status': 'UP', 'appname': 'calendar-api'})
    client_kwargs = {
        'event_hooks': {'response': [responses.append]},
        'limits': httpx.Limits(max_connections=1),
    }
    with CalendarApi('key', transport=httpx.MockTransport(fake_server), client_kwargs=client_kwargs) as api:
        api.health()
    assert len(responses) == 1
    assert 'x-timestamp' in fake_server.last.headers


# ---- Proxies ----
def test_explicit_proxy_wins_over_the_environment(clean_env: pytest.MonkeyPatch):
    clean_env.setenv('HTTPS_PROXY', ENV_PROXY)
    assert resolve_proxy('https://calendar-api.ma', proxy=PROXY) == PROXY


@pytest.mark.parametrize("var", ['HTTPS_PROXY', 'https_proxy', 'ALL_PROXY'])
def test_environment_proxy(clean_env: pytest.MonkeyPatch, var: str):
    clean_env.setenv(var, ENV_PROXY)
    assert resolve_proxy('https://calendar-api.ma') == ENV_PROXY
    with CalendarApi('key') as api:
        assert is_proxied(api.client), "Env proxies were ignored before 0.9.0"


def test_environment_proxy_follows_the_scheme(clean_env: pytest.MonkeyPatch):
    clean_env.setenv('HTTP_PROXY', ENV_PROXY)
    assert resolve_proxy('https://calendar-api.ma') is None
    assert resolve_proxy('http://localhost:8000') == ENV_PROXY


@pytest.mark.parametrize("no_proxy", ['calendar-api.ma', '.calendar-api.ma', 'example.test,calendar-api.ma', '*'])
def test_no_proxy(clean_env: pytest.MonkeyPatch, no_proxy: str):
    clean_env.setenv('HTTPS_PROXY', ENV_PROXY)
    clean_env.setenv('NO_PROXY', no_proxy)
    assert resolve_proxy('https://calendar-api.ma') is None


def test_trust_env_false_ignores_the_environment(clean_env: pytest.MonkeyPatch):
    clean_env.setenv('HTTPS_PROXY', ENV_PROXY)
    assert resolve_proxy('https://calendar-api.ma', trust_env=False) is None
    with CalendarApi('key', trust_env=False) as api:
        assert not is_proxied(api.client)


@pytest.mark.anyio
async def test_async_client_uses_the_proxy():
    async with AsyncCalendarApi('key', proxy=PROXY) as api:
        assert is_proxied(api.client)


# ---- TLS ----
def test_ssl_context_verify():
    assert build_ssl_context().verify_mode == ssl.CERT_REQUIRED
    unverified = build_ssl_context(verify=False)
    assert unverified.verify_mode == ssl.CERT_NONE
    assert not unverified.check_hostname


def test_ssl_context_ca_bundle(tmp_path):
    assert build_ssl_context(verify=certifi.where()).cert_store_stats()['x509_ca'] > 0
    (tmp_path / 'ca.pem').write_bytes(Path(certifi.where()).read_bytes())
    # A directory is used as `capath`, the certificates are loaded lazily
    assert build_ssl_context(verify=str(tmp_path)).verify_mode == ssl.CERT_REQUIRED


def test_ssl_context_client_cert(tmp_path):
    with pytest.raises(FileNotFoundError):
        build_ssl_context(cert=str(tmp_path / 'missing.pem'))


def test_ca_bundle_is_used_by_the_client():
    with CalendarApi('key', verify=certifi.where()) as api:
        assert pool_of(api.client)._ssl_context.verify_mode == ssl.CERT_REQUIRED
    with CalendarApi('key', verify=False) as api:
        assert pool_of(api.client)._ssl_context.verify_mode == ssl.CERT_NONE
