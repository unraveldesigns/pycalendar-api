import datetime
import logging

import httpxyz

from .app_utils import get_app_version

logger = logging.getLogger(__name__)


def add_timestamp(request):
    request.headers["x-timestamp"] = str(datetime.datetime.now().isoformat())
    return request

def set_encoding(response: httpxyz.Response, default_encoding: str='utf-8'):
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
    base_url: str=None, headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=True, follow_redirects: bool=True
) -> httpxyz.Client:
    """Construit l'engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        httpxyz.Client: Client configuré
    """
    timeout = httpxyz.Timeout(timeout=timeout, read=timeout * 5)
    transport = httpxyz.HTTPTransport(retries=retries, verify=verify)
    clt = httpxyz.Client(
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
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify=False, follow_redirects=True
) -> httpxyz.AsyncClient:
    """Construit l'Async engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        httpxyz.AsyncClient: AsyncClient configuré
    """
    timeout = httpxyz.Timeout(timeout=timeout, read=timeout * 5)
    transport = httpxyz.AsyncHTTPTransport(retries=retries, verify=verify)
    return httpxyz.AsyncClient(
        headers=build_client_headers(headers=headers),
        base_url=base_url, default_encoding=default_encoding,
        event_hooks={"request": [add_timestamp]},
        cookies=cookies, timeout=timeout, transport=transport, follow_redirects=follow_redirects
    )
