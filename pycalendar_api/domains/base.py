from dataclasses import dataclass, field

from httpx import AsyncClient, Client, Response

from pycalendar_api.exceptions import (
    CalendarAPIAuthError,
    CalendarAPIClientError,
    CalendarAPIParamError,
    CalendarAPIStructError,
    default_message,
)

ModelT = "ModelT"
_UNSET = type("_UNSET", (object,), {})()


@dataclass(frozen=True)
class ApiCall:
    """Description of a GET request to the API and how to deserialize its response.

    Built once by the resource operations and executed by either the sync or the async client.

    Attributes:
        url (str): Endpoint URL, relative to the client `base_url` or absolute
        params (dict): Query parameters
        model_type (ModelT): Model class used for deserialization
        many (bool): The response is a list of `model_type`
    """
    url: str
    params: dict = field(default_factory=dict)
    model_type: ModelT = None
    many: bool = False


class BaseMixin:
    """Mixin Base class for resource-interaction with Calendar API.

    Attributes:
        resource_name (str): Resource canonical name
        model_type (ModelT): Default model class of an endpoint
        endpoints (dict): A mapping of operation keys and endpoint URLS. Each operation has a unique key in the dict
    """
    resource_name: str = _UNSET
    model_type: ModelT = _UNSET
    endpoints: dict = _UNSET

    def __init__(self, client: Client | AsyncClient, endpoints: dict = None, **kwargs):
        self.client: Client | AsyncClient = client
        if endpoints:
            self.endpoints = endpoints

        if self.endpoints is _UNSET:
            msg = f"endpoint not defined for the resource {self.resource_name}. {self.endpoints=}"
            raise CalendarAPIClientError(msg)

    def endpoint_by_operation(self, method: str) -> str:
        """Retrieve the endpoint URL from the deined method key in URLS (self.endpoints)
        the key is in the form of {self.resource_name}:{method}.

        Args:
            method (str): Operation key

        Returns:
            str: Endpoint URL

        Raises:
            CalendarAPIParamError: Method not defined
        """
        try:
            return self.endpoints[self._endpoint_key(method)]
        except KeyError as err:
            msg = f"{method} not defined in self.endpoints de key={err}.\n{self.endpoints=}"
            raise CalendarAPIParamError(msg)

    def host_url(self) -> str:
        """Returns the host url from the client. `self.client.base_url` contains the `/api/v1` path to ease the definition of operation keys.
        """
        return str(self.client.base_url.join("/")).rstrip("/")

    def _endpoint_key(self, method: str) -> str:
        """Construit la clé de l'endpoint défini par cette ressource en combinant resource_name et method

        Args:
            method (str): method one of (many, filter, mapping)

        Returns:
            str: `resource_name:method`. ie: emetteurs:one, emetteurs:mapping
        """
        return f"{self.resource_name}:{method}"

    def _struct_model(self, model_dict: dict, *, extra_dict: dict=None, model_type=None, **kwargs) -> ModelT:
        """Build the model object from the response.

        Args:
            model_dict (dict): Json payload of the response
            extra_dict (dict, optional): Allows to inject values not present in the response. duplicate keys are overridden.

        Returns:
            ModelT: Model class used for deserialization
        """
        extra_dict = extra_dict or {}
        model_type = model_type or self.model_type

        try:
            d = {**model_dict, **extra_dict}
            if model_type in (None, _UNSET):
                msg = f"Model Type is not defined for {self.__class__.__qualname__}"
                raise CalendarAPIStructError(msg)

            if hasattr(model_type, "from_json"):
                return model_type.from_json(d)

            return model_type(**d)
        except (AttributeError, TypeError):
            msg = f"Error while instanciating {model_type}\nGot: {model_dict=}"
            raise CalendarAPIStructError(msg)

    def _parse(self, call: ApiCall, response: Response) -> "ModelT | list[ModelT]":
        """Deserialize the response of an `ApiCall`"""
        data = self.json_from_response_or_raise(response)
        if call.many:
            return [self._struct_model(d, model_type=call.model_type) for d in data]
        return self._struct_model(data, model_type=call.model_type)

    @staticmethod
    def json_from_response_or_raise(response: Response, *, error_key: str = "detail") -> dict:
        """Extract the json payload from the Response.

        Args:
            response (Response): httpx Response
            error_key (str, 'detail'): Error key name in the Json body

        Returns:
            dict: Json extracted from the response

        Raises:
            CalendarAPIAuthError: If the HTTP response status is 401 or 403
            CalendarAPIClientError: If the HTTP response status is >= 400 or the body is not a valid Json
        """
        try:
            payload = response.json()
        except ValueError:
            payload = None

        if response.status_code >= 400:
            message = payload.get(error_key) if isinstance(payload, dict) else None
            exc_class = CalendarAPIAuthError if response.status_code in (401, 403) else CalendarAPIClientError
            raise exc_class(message or default_message(response, error_key))

        if payload is None:
            raise CalendarAPIClientError(default_message(response, error_key))

        return payload


class SyncResourceMixin(BaseMixin):
    """Executes the `ApiCall` of a resource with a sync `httpx.Client`"""
    client: Client

    def _fetch(self, call: ApiCall) -> "ModelT | list[ModelT]":
        response = self.client.get(call.url, params=call.params)
        return self._parse(call, response)


class AsyncResourceMixin(BaseMixin):
    """Executes the `ApiCall` of a resource with an `httpx.AsyncClient`"""
    client: AsyncClient

    async def _fetch(self, call: ApiCall) -> "ModelT | list[ModelT]":
        response = await self.client.get(call.url, params=call.params)
        return self._parse(call, response)
