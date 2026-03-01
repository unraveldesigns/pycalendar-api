from pathlib import Path

from .config import Settings, load_settings
from .domains.bdays import BDaysResource
from .domains.health import ApiHealth, HealthsResource
from .domains.holidays import HolidaysResource


class CalendarApi:

    def __init__(self, apikey: str=None, config: Settings=None, **kwargs):
        self.config = config or Settings()
        if apikey:
            self.config.api.api_key = apikey

        self.client = self.config.create_http_client()
        # ------ Domains APIs ------
        self.bdays = BDaysResource(self.client)
        self.holidays = HolidaysResource(self.client)
        self.h = HealthsResource(self.client)

    def __repr__(self):
        rv = f"CalendarApi(instance={self.config.api.api_base_url})"
        return rv

    @classmethod
    def from_env(cls) -> "CalendarApi":
        """Instancie la configuration depuis les variables d'environnement.
        S'assurer qu'elles sont définies au niveau de /etc/default/flint sous Ubuntu ou autre

        Returns:
            CalendarApi: Configuration du client
        """
        conf = load_settings(from_env=True)
        return cls(config=conf)

    @classmethod
    def from_config_file(cls, fpath: str) -> "CalendarApi":
        """Charge la configuration depuis un fichier toml respectant la structure attendue.

        Args:
            fpath (str): Chemin du fichier de configuration `.toml`

        Returns:
            CalendarApi: Instance configurée selon le fichier renseigné.

        Raises:
            CalendarAPIClientError: Si `strict=True` et que le fichier de configuration n'existe pas!
        """
        conf = Settings.from_config_file(fpath)
        return cls(config=conf)

    def openapi_schema(self, fpath: Path|str) -> Path:
        """Télécharge le schéma OpenAPI actuel depuis le serveur.

        Args:
            fpath (Path | str): Chemin du fichier
        """
        return self.config.openapi_schema(fpath)

    def health(self) -> ApiHealth:
        return self.h.api()
