import datetime
from dataclasses import dataclass, field

from pycalendar_api.config import CONSTANTS


@dataclass
class ApiHealth:
    api_status: str = None
    appname: str = CONSTANTS.APPLICATION_NAME
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now, init=False)

    @classmethod
    def from_json(cls, data: dict, **kwargs) -> "ApiHealth":
        return cls(
            api_status=data.get('api_status', 'NOT RESPONSDING - Check your connection'),
            appname=data.get('appname', CONSTANTS.APPLICATION_NAME)
        )
