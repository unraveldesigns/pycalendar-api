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
    """Base Mixin qui expose les méthodes d'interaction avec les ressources API d'Atlas Market

    Attributes:
        resource_name (str): Nom de la resource
        resource_key (str): Nom du path param d'identification d'un API resource
        model_type (ModelT): Classe de désérialisation de la structure de retour
    """

    resource_name: str = _UNSET
    resource_key: str = _UNSET
    model_type: ModelT = _UNSET
    endpoints: dict = _UNSET

    def __init__(self, client: Client, endpoints: dict = None, **kwargs):
        self.client: Client = client
        if endpoints:
            self.endpoints = endpoints

        if self.endpoints is _UNSET:
            msg = f"Définir endpoints de la ressource {self.resource_name}. {self.endpoints=}"
            raise CalendarAPIClientError(msg)

    def _endpoint_key(self, method: str) -> str:
        """Construit la clé de l'endpoint défini par cette ressource en combinant resource_name et method

        Args:
            method (str): method one of (many, filter, mapping)

        Returns:
            str: `resource_name:method`. ie: emetteurs:one, emetteurs:mapping
        """
        return f"{self.resource_name}:{method}"

    def _url_with_key(self, method: str, key: str) -> str:
        """Similaire à self._endpoint_key mais formatte l'URL avec resource key.
        Renseigne les PathParams

        Args:
            method (str): method one of (one, filter, mapping)
            key (str): key id de l'entité désirée

        Returns:
            str: L'URL de la methode formatté avec key id . ie: emetteurs:one, emetteurs:mapping
        """
        endpoint = self.endpoints[f"{self.resource_name}:{method}"]
        return endpoint.format(**{self.resource_key: key})

    def _struct_model(self, model_dict: dict, *, extra_dict: dict=None, model_type=None, **kwargs) -> ModelT:
        """Méthode construction du `model_type` depuis la réponse json.
        `model_type` représente la classe principale du domaine (Indiceref, EmetteurRef, OPCRef, ...)

        `extra_dict` permet d'injecter des variables ou valeurs supplémentaires en mettant à jour model_dict. Les clés dupliquées seront écrasées.

        Args:
            model_dict (dict): json dict de la réponse HTTP
            extra_dict (dict, optional): permet d'injecter des variables ou valeurs supplémentaires en mettant à jour model_dict. Les clés dupliquées seront écrasées.
            **kwargs: for subclassing

        Returns:
            ModelT: Instance du modèle cls.model_type
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
            msg = f"Erreur lors de la contruction du modèle {model_type}\nreçu: {d=}"
            raise CalendarAPIStructError(msg)

    def endpoint_by_operation(self, method: str) -> str:
        try:
            return self.endpoints[self._endpoint_key(method)]
        except KeyError as err:
            msg = f"{method} ne correspond à aucun endpoint de key={err}.\n{self.endpoints=}"
            raise CalendarAPIParamError(msg)

    def host_url(self) -> str:
        """Extrait l'URL de l'instance depuis self.client.base_url. Similaire à ApiConfig.host_url()"""
        base, path = str(self.client.base_url), self.client.base_url.path
        return base.removesuffix(path)

    @staticmethod
    def json_from_response_or_raise(response: Response, *, error_key: str = "detail") -> dict:
        """Fonction utilitaire d'extraction du json depuis la réponse.
        Si le code de la réponse est >= 400, raises CalendarAPIClientError

        Args:
            response (Response): Reponse HTTPX
            error_key (str, 'detail'): Champs du message d'erreur

        Returns:
            dict: Json extracted from the response

        Raises:
            CalendarAPIClientError: Si la réponse est une erreur status_code >= 400
        """
        if response.status_code >= 400:
            raise CalendarAPIClientError(response.json().get(error_key, default_message(response, error_key)))

        return response.json()
