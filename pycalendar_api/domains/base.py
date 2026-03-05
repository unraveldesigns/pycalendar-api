from httpx import Client, Response

from pycalendar_api.exceptions import (
    CalendarAPIClientError,
    CalendarAPIParamError,
    CalendarAPIStructError,
    default_message,
)

ModelT = "ModelT"
_UNSET = type("_UNSET", (object,), {})()


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

    def __init__(self, client: Client, endpoints: dict = None, **kwargs):
        self.client: Client = client
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
        base, path = str(self.client.base_url), self.client.base_url.path
        return base.removesuffix(path)

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
        d = {**model_dict, **extra_dict}
        model_type = model_type or self.model_type

        try:
            if model_type in (None, _UNSET):
                msg = f"Model Type is not defined for {self.__class__.__qualname__}"
                raise CalendarAPIStructError(msg)

            if hasattr(model_type, "from_json"):
                return model_type.from_json(d)

            return self.model_type(**d)
        except (AttributeError, TypeError):
            msg = f"Error while instanciating {model_type}\nGot: {d=}"
            raise CalendarAPIStructError(msg)

    @staticmethod
    def json_from_response_or_raise(response: Response, *, error_key: str = "detail") -> dict:
        """Extract the json payload from the Response.

        Args:
            response (Response): httpx Response
            error_key (str, 'detail'): Error key name in the Json body

        Returns:
            dict: Json extracted from the response

        Raises:
            CalendarAPIClientError: If the HTTP response status is >= 400
        """
        if response.status_code >= 400:
            raise CalendarAPIClientError(response.json().get(error_key, default_message(response, error_key)))

        return response.json()
