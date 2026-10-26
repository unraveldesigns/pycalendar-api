from pycalendar_api.models import ApiHealth

from .base import ApiCall, AsyncResourceMixin, BaseMixin, SyncResourceMixin
from .urls import ENDPOINTS


class HealthsCalls(BaseMixin):
    """Builds the `ApiCall` of the Health domain. Shared by the sync and async resources."""

    resource_name = "health"
    endpoints = ENDPOINTS

    def _api_call(self) -> ApiCall:
        # The health endpoint is served at the host root, outside of the `/api/v1` base url
        url = self.host_url() + self.endpoint_by_operation('api')
        return ApiCall(url, model_type=ApiHealth)


class HealthsResource(SyncResourceMixin, HealthsCalls):

    def api(self) -> ApiHealth:
        """Check the health of the API. Serves as a heartbeat for integrations.

        Returns:
            ApiHealth: Health Status of the API
        """
        return self._fetch(self._api_call())


class AsyncHealthsResource(AsyncResourceMixin, HealthsCalls):
    """Async version of `HealthsResource`"""

    async def api(self) -> ApiHealth:
        """Check the health of the API. See `HealthsResource.api`"""
        return await self._fetch(self._api_call())
