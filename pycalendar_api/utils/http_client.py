import datetime
import logging

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


def get_http_client(
    base_url: str="", headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=True, follow_redirects: bool=True,
    transport: httpx.BaseTransport=None,
) -> httpx.Client:
    """Construit l'engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives
        transport (httpx.BaseTransport, optional): Transport personnalisé (proxy, tests...). Remplace celui construit avec `retries` et `verify`

    Returns:
        httpx.Client: Client configuré
    """
    timeout = httpx.Timeout(timeout=timeout, read=timeout * 5)
    transport = transport or httpx.HTTPTransport(retries=retries, verify=verify)
    clt = httpx.Client(
        headers=build_client_headers(headers=headers),
        base_url=base_url, default_encoding=default_encoding,
        event_hooks={"request": [add_timestamp]},
        cookies=cookies, timeout=timeout, transport=transport, follow_redirects=follow_redirects
    )
    msg = f"Sync Client instanciated {clt}"
    logger.info(msg)
    return clt

def get_http_client_async(
    base_url: str="", headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=True, follow_redirects: bool=True,
    transport: httpx.AsyncBaseTransport=None,
) -> httpx.AsyncClient:
    """Construit l'Async engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives
        transport (httpx.AsyncBaseTransport, optional): Transport personnalisé (proxy, tests...). Remplace celui construit avec `retries` et `verify`

    Returns:
        httpx.AsyncClient: AsyncClient configuré
    """
    timeout = httpx.Timeout(timeout=timeout, read=timeout * 5)
    transport = transport or httpx.AsyncHTTPTransport(retries=retries, verify=verify)
    clt = httpx.AsyncClient(
        headers=build_client_headers(headers=headers),
        base_url=base_url, default_encoding=default_encoding,
        event_hooks={"request": [add_timestamp_async]},
        cookies=cookies, timeout=timeout, transport=transport, follow_redirects=follow_redirects
    )
    msg = f"Async Client instanciated {clt}"
    logger.info(msg)
    return clt
