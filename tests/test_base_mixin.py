from dataclasses import dataclass

import httpx
import pytest

from pycalendar_api.domains.base import ApiCall, BaseMixin, SyncResourceMixin
from pycalendar_api.exceptions import (
    CalendarAPIAuthError,
    CalendarAPIClientError,
    CalendarAPIParamError,
    CalendarAPIStructError,
)

pytestmark = pytest.mark.client


@dataclass
class Dummy:
    name: str
    value: int = 0


class DummyResource(SyncResourceMixin):
    resource_name = "dummy"
    model_type = Dummy


ENDPOINTS = {'dummy:one': '/dummy/{key}', 'dummy:many': '/dummy'}


@pytest.fixture(name='resource')
def fx_resource():
    with httpx.Client(base_url="https://example.test/api/v1") as client:
        yield DummyResource(client, endpoints=ENDPOINTS)


def response(status_code: int, **kwargs) -> httpx.Response:
    return httpx.Response(status_code, request=httpx.Request("GET", "https://example.test/api/v1/dummy"), **kwargs)


# ---- Base Mixin ----
def test_endpoints_are_required():
    with pytest.raises(CalendarAPIClientError), httpx.Client() as client:
        BaseMixin(client)


def test_endpoint_by_operation(resource: DummyResource):
    assert resource.endpoint_by_operation('one') == '/dummy/{key}'
    with pytest.raises(CalendarAPIParamError):
        resource.endpoint_by_operation('unknown')


def test_host_url_follows_the_client_base_url(resource: DummyResource):
    assert resource.host_url() == "https://example.test"


def test_struct_model(resource: DummyResource):
    assert resource._struct_model({'name': 'a'}) == Dummy('a')
    assert resource._struct_model({'name': 'a', 'value': 1}, extra_dict={'value': 2}) == Dummy('a', 2)

    with pytest.raises(CalendarAPIStructError):
        resource._struct_model({'unexpected': 'field'})

    with pytest.raises(CalendarAPIStructError):
        resource._struct_model(['not', 'a', 'dict'])


def test_struct_model_without_model_type():
    with httpx.Client() as client:
        res = SyncResourceMixin(client, endpoints=ENDPOINTS)
        with pytest.raises(CalendarAPIStructError):
            res._struct_model({'name': 'a'})


@pytest.mark.parametrize(
    ("status_code", "exc_class"),
    [(400, CalendarAPIClientError), (401, CalendarAPIAuthError), (403, CalendarAPIAuthError), (404, CalendarAPIClientError)],
)
def test_json_or_raise_http_errors(status_code: int, exc_class: type[Exception]):
    with pytest.raises(exc_class, match="boom"):
        BaseMixin.json_from_response_or_raise(response(status_code, json={'detail': 'boom'}))


def test_json_or_raise_non_json_error():
    """A proxy/gateway error page is not Json: the error still carries the status and the body"""
    with pytest.raises(CalendarAPIClientError, match="status_code=502"):
        BaseMixin.json_from_response_or_raise(response(502, text="<html>Bad Gateway</html>"))


def test_json_or_raise_non_json_success():
    with pytest.raises(CalendarAPIClientError):
        BaseMixin.json_from_response_or_raise(response(200, text="not json"))


def test_json_or_raise_ok():
    assert BaseMixin.json_from_response_or_raise(response(200, json={'name': 'a'})) == {'name': 'a'}


def test_fetch_one_and_many():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith('/dummy'):
            return httpx.Response(200, json=[{'name': 'a'}, {'name': 'b', 'value': 2}])
        return httpx.Response(200, json={'name': request.url.path.rsplit('/', 1)[-1]})

    with httpx.Client(base_url="https://example.test/api/v1", transport=httpx.MockTransport(handler)) as client:
        res = DummyResource(client, endpoints=ENDPOINTS)
        assert res._fetch(ApiCall('/dummy/x', model_type=Dummy)) == Dummy('x')
        assert res._fetch(ApiCall('/dummy', model_type=Dummy, many=True)) == [Dummy('a'), Dummy('b', 2)]
