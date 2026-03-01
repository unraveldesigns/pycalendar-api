import os
from functools import lru_cache
from pathlib import Path

from .constants import CONSTANTS
from .exceptions import ConfigurationError
from .settings import Settings


def select_confdir_path() -> Path:
    """Retourne APPLICATION_HOME_KEY EnvVar si présent ou $HOME de l'utilisateur

    Returns:
        Path: Path object
    """
    config_dir = os.environ.get(CONSTANTS.APPLICATION_HOME_KEY)
    if config_dir:
        print(f'Load Settings: Using {CONSTANTS.APPLICATION_HOME_KEY=}')
        return Path(config_dir)
    else:
        config_dir = Path.home() / CONSTANTS.APPLICATION_NAME
        print(f'Config directory path = {config_dir}')
        return config_dir


def get_config_path() -> Path:
    """La priorité est donnée à la variable d'environnement `CONSTANTS.APPLICATION_ENV_KEY`

    Par défaut pour ce projet (calendar-api): `CALENDAR_API_ENV`

    Returns:
        Path: Chemin du fichier de configuration

    Raises:
        ConfigurationError:
            - Si la valeur de `APPLICATION_ENV_KEY` n'est pas reconnue
            - Si fichier de configuration incorrecte
    """
    fname = f"{CONSTANTS.APPLICATION_NAME}{CONSTANTS.CONFIG_EXTENSION}"
    confdir = select_confdir_path()
    if not confdir.exists():
        confdir.mkdir(exist_ok=True, parents=True)

    fpath = confdir / fname

    if not fpath.exists():
        msg = f"Fichier de configuration introuvable dans le dossier {confdir} sous le nom {fname}"
        raise ConfigurationError(msg)

    return fpath


@lru_cache(maxsize=1)
def load_settings(*, cache_key: str=None, from_env: bool=False) -> Settings:
    if from_env:
        envkey = os.environ.get(CONSTANTS.APPLICATION_APIKEY)
        if not envkey:
            msg = f"Environment variable `{CONSTANTS.APPLICATION_APIKEY}` not found."
            raise ConfigurationError(msg)

        conf = Settings()
        conf.api.api_key = envkey
        return conf

    fpath = get_config_path()
    # print(f'Load Settings: Using {fpath=}')
    return Settings.from_config_file(fpath)
