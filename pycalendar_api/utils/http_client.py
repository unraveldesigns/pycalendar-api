import datetime
import logging
from functools import partial

import niquests

from .app_utils import get_app_version

logger = logging.getLogger(__name__)


def add_timestamp(request):
    request.headers["x-timestamp"] = str(datetime.datetime.now().isoformat())
    return request

def set_encoding(response: niquests.Response, default_encoding: str='utf-8'):
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
) -> niquests.Session:
    """Construit l'engine HTTP des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        niquests.Session: Client configuré
    """
    timeout = niquests.TimeoutConfiguration(connect=timeout, read=timeout*5)
    clt = niquests.Session(
        headers=build_client_headers(headers=headers),
        retries=retries,
        base_url=base_url,
        timeout=timeout,
    )
    clt.hooks['request'] = [add_timestamp]
    clt.hooks['response'] = [partial(set_encoding, default_encoding=default_encoding)]
    clt.cookies.update(cookies or {})
    clt.verify = verify
    if follow_redirects is False:
        clt.max_redirects = 0
    msg = f"Sync Session instanciated {clt}"
    logger.info(msg)
    return clt


def get_http_client_async(
    base_url: str=None, headers: dict=None, cookies: dict=None,
    default_encoding: str="utf-8", timeout: int=10, retries: int=2, verify: bool=True, follow_redirects: bool=True
) -> niquests.AsyncSession:
    """Construit l'Async HTTPEngine des connections

    Args:
        headers (dict, optional): Headers qui seront mergé avec ceux par défaut
        base_url (str, optional): URL de base des connexions successives

    Returns:
        niquests.AsyncSession: Async Client configuré
    """
    timeout = niquests.TimeoutConfiguration(connect=timeout, read=timeout*5)
    clt = niquests.AsyncSession(
        headers=build_client_headers(headers=headers),
        retries=retries,
        base_url=base_url,
        timeout=timeout,
    )
    clt.hooks['request'] = [add_timestamp]
    clt.hooks['response'] = [partial(set_encoding, default_encoding=default_encoding)]
    clt.cookies.update(cookies or {})
    clt.verify = verify
    if follow_redirects is False:
        clt.max_redirects = 0
    msg = f"Async Session instanciated {clt}"
    logger.info(msg)
    return clt
