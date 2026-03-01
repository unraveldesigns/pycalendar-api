import datetime
import logging

import httpx

logger = logging.getLogger(__name__)


def add_timestamp(request):
    request.headers["x-timestamp"] = str(datetime.datetime.now().isoformat())
    return request


def build_client_headers(headers: dict=None):
    head = headers or {}
    rv = {
        "User-Agent": "python/httpx",
        "X-App-Agent": "AMK Client V 1.60",
        "X-HTTPX-VERSION": f"{httpx.__version__}",
        "X-CLIENT": "py-calendar-api",
    }
    rv.update(head)
    return rv


def get_http_client(
    base_url: str=None, headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=False, follow_redirects: bool=True
) -> httpx.Client:
    """Construit l'engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        httpx.Client: Client configuré
    """
    timeout = httpx.Timeout(timeout=timeout, read=timeout*5)
    transport = httpx.HTTPTransport(retries=retries, verify=verify)
    clt = httpx.Client(
        headers=build_client_headers(headers=headers),
        base_url=base_url, default_encoding=default_encoding,
        event_hooks={"request": [add_timestamp]},
        cookies=cookies, timeout=timeout, transport=transport, follow_redirects=follow_redirects
    )
    msg = f"Sync Client instancié {clt}"
    logger.info(msg)
    return clt


def get_http_client_async(
    base_url: str=None, headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=False, follow_redirects: bool=True
) -> httpx.AsyncClient:
    """Construit l'Async engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        httpx.AsyncClient: AsyncClient configuré
    """
    timeout = httpx.Timeout(timeout=timeout, read=timeout*5)
    transport = httpx.AsyncHTTPTransport(retries=retries, verify=verify)
    clt = httpx.AsyncClient(
        headers=build_client_headers(headers=headers),
        base_url=base_url, default_encoding=default_encoding,
        event_hooks={"request": [add_timestamp]},
        cookies=cookies, timeout=timeout, transport=transport, follow_redirects=follow_redirects
    )
    msg = f"Async Client instancié {clt}"
    logger.info(msg)
    return clt
