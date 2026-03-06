from pathlib import Path

# --- Time Units
ONE_HOUR_IN_SECONDS = 3600
ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24
ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7

# --- Paths
HERE = Path(__file__).absolute().parent
BASE_DIR = HERE.parent


class CONSTANTS:
    # --- config
    NONE_VALUE = "UNDEFINED"
    PREFIX_ENV_VARS = "PYCAL_"
    BASE_DIR = BASE_DIR
    # --- loader
    APP_MODULE_NAME = "pycalendar_api"
    APPLICATION_NAME = "pycalendar-api"
    API_TITLE = "Calendar API"
    API_VERSION = "v1"
    APPLICATION_HOME_KEY = 'PYCALENDAR_API_HOME'
    APPLICATION_APIKEY = 'PYCALENDAR_APIKEY'
    APPLICATION_ENV_KEY = 'PYCALENDAR_API_ENV'
    CONFIG_EXTENSION = ".toml"
    ENCODING = 'utf-8'

    # --- endpoints
    HEALTH_ENDPOINT = "/health"
    OPENAPI_SCHEMA_ENDPOINT = "/schema"
    API_ENDPOINT = "/api/v1"
    AUTH_API_HEADER_KEY = "X-API-KEY"
    # --- Time Units
    ONE_HOUR_IN_SECONDS = ONE_HOUR_IN_SECONDS
    ONE_DAY_IN_SECONDS = ONE_DAY_IN_SECONDS
    ONE_WEEK_IN_SECONDS = ONE_WEEK_IN_SECONDS
