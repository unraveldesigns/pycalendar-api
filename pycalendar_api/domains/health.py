import httpx

from pycalendar_api.models import ApiHealth

from .base import BaseMixin
from .urls import ENDPOINTS


class HealthsResource(BaseMixin):

    resource_name = "health"

    def __init__(self, client: httpx.Client):
        super().__init__(client, endpoints=ENDPOINTS)

    def api(self) -> ApiHealth:
        """Check the health of the API. Serves as a heartbeat for integrations.

        Returns:
            ApiHealth: Health Status of the API
        """
        key = 'api'
        endpoint = self.endpoint_by_operation(key)
        url = self.host_url() + endpoint
        resp = self.client.get(url)
        data = self.json_from_response_or_raise(resp)
        return self._struct_model(data, model_type=ApiHealth)
