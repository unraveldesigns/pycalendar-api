from pathlib import Path


def build_urls_from_openapi_schema(openapi_path: Path|str, fpath: Path|str, *, strip_base_api: bool=True) -> Path:
    """Extrait les route_paths depuis le schema openapi.json téléchargé et les exporte vers un fichier Texte

    Args:
        openapi_path (Path | str): Chemin du schema openapi
        fpath (Path | str): Chemin du fichier des URLS en texte
        strip_base_api (bool, True): Strip les urls de Base Api (/api/v1)

    Returns:
        Path: Chemin absolu du fichier exporté
    """
    import json

    from pycalendar_api.config import CONSTANTS

    openapi_path = Path(openapi_path).absolute()
    fpath = Path(fpath).absolute()
    with open(openapi_path, encoding=CONSTANTS.ENCODING) as oa_fd:
        schema = json.load(oa_fd)
        with open(fpath, 'w', encoding=CONSTANTS.ENCODING) as url_fd:
            # Endpoints is in schema['paths'].keys()
            if strip_base_api:
                # strip api base_url
                stripped_paths = (x.lstrip(CONSTANTS.API_ENDPOINT) for x in schema['paths'])
                url_fd.writelines("\n".join(stripped_paths))
            else:
                url_fd.writelines("\n".join(schema['paths'].keys()))

    print(f"URLS extraits depuis openapi schema {openapi_path} vers -> {fpath}")
    return fpath
