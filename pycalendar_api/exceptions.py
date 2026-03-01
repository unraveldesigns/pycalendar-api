# noqa: N818
# ------ Client HTTP -----
class CalendarAPIError(Exception):
    """Classe de base pour les exceptions client de Calendar API Client"""

class CalendarAPIClientError(CalendarAPIError):
    """Exceptions liées au client HTTPX de Calendar API Client"""

class CalendarAPIAuthError(CalendarAPIClientError):
    """Exceptions liées à l'authetification du client Calendar API Client"""

class CalendarAPIStructError(CalendarAPIError):
    """Exceptions liées à la construction du modèle depuis la réponse Json"""

class CalendarAPIParamError(CalendarAPIError):
    """Exceptions liées aux paramètres mal renseignés"""

class CalendarAPIConfigError(CalendarAPIError):
    """Exceptions liées à la configuration du client"""

ERROR_MESSAGE = "La reponse n'a pas de message d'erreur sous la clé {error_key}.\nstatus_code={status_code}\ntext_body={text_body}\nurl={url}"

def default_message(response, error_key: str='detail') -> str:
    return ERROR_MESSAGE.format(
        error_key=error_key, status_code=response.status_code,
        text_body=response.text, url=response.url
    )
