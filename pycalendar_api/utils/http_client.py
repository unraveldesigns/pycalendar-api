import datetime
import logging
import ssl
import urllib.request
from pathlib import Path
from typing import Any

import httpx

from .app_utils import get_app_version

logger = logging.getLogger(__name__)


def add_timestamp(request):
    request.headers["x-timestamp"] = str(datetime.datetime.now().isoformat())
    return request

async def add_timestamp_async(request):
    """`httpx.AsyncClient` event hooks must be coroutines"""
    return add_timestamp(request)

def set_encoding(response: httpx.Response, default_encoding: str='utf-8'):
    response.encoding = default_encoding
    return response

def build_client_headers(headers: dict=None):
    head = headers or {}
    app_version = get_app_version()
    rv = {
        "X-CLIENT": "pycalendar-api",
        "X-CLIENT-VERSION": app_version['version_id']
    }
    rv.update(head)
    return rv


def build_ssl_context(verify: bool|str=True, cert: str=None, cert_key: str=None, trust_env: bool=True) -> ssl.SSLContext:
    """Build the TLS context of the transport

    Args:
        verify (bool | str, optional): Verify the server certificate. A path to a CA bundle file (or directory) replaces the default CAs
        cert (str, optional): Client certificate file (PEM), for mutual TLS. May also contain the private key
        cert_key (str, optional): Private key file of `cert`, when not included in it
        trust_env (bool, optional): Use the `SSL_CERT_FILE` / `SSL_CERT_DIR` environment variables when `verify=True`

    Returns:
        ssl.SSLContext: TLS context
    """
    if isinstance(verify, bool):
        ctx = httpx.create_ssl_context(verify=verify, trust_env=trust_env)
    elif Path(verify).is_dir():
        ctx = ssl.create_default_context(capath=verify)
    else:
        ctx = ssl.create_default_context(cafile=verify)

    if cert:
        ctx.load_cert_chain(cert, keyfile=cert_key)
    return ctx


def resolve_proxy(base_url: str="", proxy: str=None, trust_env: bool=True) -> str|None:
    """Proxy used to reach `base_url`

    An explicit `proxy` always wins. Otherwise, when `trust_env` is True, the standard environment variables
    `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` are used, unless the host is excluded by `NO_PROXY`.

    Returns:
        str | None: Proxy URL or None for a direct connection
    """
    if proxy or not trust_env:
        return proxy or None

    proxies = urllib.request.getproxies_environment()
    url = httpx.URL(base_url)
    if url.host and urllib.request.proxy_bypass_environment(url.host, proxies):
        return None
    return proxies.get(url.scheme or "https") or proxies.get("all")


def _client_options(
    *, transport_cls: type, hook, base_url: str, headers: dict, cookies: dict,
    default_encoding: str, timeout: float, read_timeout: float|None, retries: int,
    verify: bool|str, cert: str|None, cert_key: str|None, proxy: str|None, trust_env: bool, follow_redirects: bool,
    transport, client_kwargs: dict,
) -> dict[str, Any]:
    """Keyword arguments of `httpx.Client` / `httpx.AsyncClient`, shared by both factories"""
    if transport is None:
        transport = transport_cls(
            retries=retries,
            verify=build_ssl_context(verify=verify, cert=cert, cert_key=cert_key, trust_env=trust_env),
            proxy=resolve_proxy(base_url, proxy=proxy, trust_env=trust_env),
        )

    # User hooks run after ours
    event_hooks = client_kwargs.pop("event_hooks", {})
    event_hooks = {
        "request": [hook, *event_hooks.get("request", [])],
        "response": list(event_hooks.get("response", [])),
    }
    return {
        "headers": build_client_headers(headers=headers),
        "base_url": base_url,
        "default_encoding": default_encoding,
        "event_hooks": event_hooks,
        "cookies": cookies,
        "timeout": httpx.Timeout(timeout=timeout, read=read_timeout or timeout * 5),
        "transport": transport,
        "trust_env": trust_env,
        "follow_redirects": follow_redirects,
        **client_kwargs,
    }


def get_http_client(
    base_url: str="", headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: float=10, read_timeout: float=None, retries: int=3,
    verify: bool|str=True, cert: str=None, cert_key: str=None, proxy: str=None, trust_env: bool=True,
    follow_redirects: bool=True, transport: httpx.BaseTransport=None, **client_kwargs,
) -> httpx.Client:
    """Build the HTTP client. The options match the `[http_client]` section of the configuration (`HTTPClientConfig`)

    Args:
        base_url (str, optional): Base URL of the requests
        headers (dict, optional): Headers merged with the default ones
        timeout (float, optional): Connect/write/pool timeout in seconds
        read_timeout (float, optional): Read timeout in seconds. Default: `timeout * 5`
        retries (int, optional): Retries on connection errors
        verify (bool | str, optional): Verify the server certificate, or path to a CA bundle. See `build_ssl_context`
        cert (str, optional): Client certificate file (PEM)
        cert_key (str, optional): Private key file of `cert`
        proxy (str, optional): Proxy URL (ie: `http://user:pass@proxy:3128`). See `resolve_proxy`
        trust_env (bool, optional): Use the proxy and certificates environment variables
        transport (httpx.BaseTransport, optional): Custom transport (tests...). Replaces the one built with `retries`, `verify`, `cert` and `proxy`
        **client_kwargs: Extra `httpx.Client` arguments (`limits`, `auth`, `event_hooks`...)

    Returns:
        httpx.Client: Configured client
    """
    clt = httpx.Client(**_client_options(
        transport_cls=httpx.HTTPTransport, hook=add_timestamp, base_url=base_url, headers=headers, cookies=cookies,
        default_encoding=default_encoding, timeout=timeout, read_timeout=read_timeout, retries=retries,
        verify=verify, cert=cert, cert_key=cert_key, proxy=proxy, trust_env=trust_env, follow_redirects=follow_redirects,
        transport=transport, client_kwargs=client_kwargs,
    ))
    msg = f"Sync Client instanciated {clt}"
    logger.info(msg)
    return clt

def get_http_client_async(
    base_url: str="", headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: float=10, read_timeout: float=None, retries: int=3,
    verify: bool|str=True, cert: str=None, cert_key: str=None, proxy: str=None, trust_env: bool=True,
    follow_redirects: bool=True, transport: httpx.AsyncBaseTransport=None, **client_kwargs,
) -> httpx.AsyncClient:
    """Build the async HTTP client. Same options as `get_http_client`

    Returns:
        httpx.AsyncClient: Configured async client
    """
    clt = httpx.AsyncClient(**_client_options(
        transport_cls=httpx.AsyncHTTPTransport, hook=add_timestamp_async, base_url=base_url, headers=headers, cookies=cookies,
        default_encoding=default_encoding, timeout=timeout, read_timeout=read_timeout, retries=retries,
        verify=verify, cert=cert, cert_key=cert_key, proxy=proxy, trust_env=trust_env, follow_redirects=follow_redirects,
        transport=transport, client_kwargs=client_kwargs,
    ))
    msg = f"Async Client instanciated {clt}"
    logger.info(msg)
    return clt
