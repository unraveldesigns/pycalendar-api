from dataclasses import MISSING, Field
from pathlib import Path
from secrets import token_urlsafe
from typing import Any

from sortedcontainers import SortedDict, SortedListWithKey, SortedSet

from .constants import CONSTANTS


def random_secret_key(n: int=48) -> str:
    return token_urlsafe(n)


def dict_to_toml(dico: dict) -> dict:
    """Adapte un dict pour etre exporté vers TOML"""
    rv = {}
    for k, v in dico.items():
        if v in (None, MISSING):
            rv[k] = CONSTANTS.NONE_VALUE
        elif isinstance(v, (dict, SortedDict)):
            rv[k] = dict_to_toml(v)
        elif isinstance(v, (set, SortedSet, SortedListWithKey)):
            rv[k] = list(v)
        elif isinstance(v, Path):
            rv[k] = str(v)
        else:
            rv[k] = v

    return rv


def toml_doc_to_dict(toml_doc: dict) -> dict:
    rv = {}
    for k, v in toml_doc.items():
        if isinstance(v, dict):
            rv[k] = toml_doc_to_dict(v)
        else:
            rv[k] = _read_none_val(v)
    return rv


def _read_none_val(val: Any):
    """Not used just a reminder when the value is None and exported"""
    if not isinstance(val, (dict, list, tuple)) and val and val in {CONSTANTS.NONE_VALUE, 'None', 'null', 'NULL', 'nil', 'NIL'}:
        return None
    return val


def replace_none_with_none_val(val):
    if val in (None, MISSING):
        return CONSTANTS.NONE_VALUE
    return val


def default_value_or_factory(field: Field):
    """Retourne et adapte la valeur par défaut définie au niveau du Field d'un dataclass
    Le besoin est un fichier ENV par défaut, transforme None en "UNDEFINED"

    Args:
        field (Field): dataclasses field

    Returns:
        Any: La valeur par défaut ou "UNDEFINED" si cette dernière est None
    """
    if field.default is not MISSING:
        return replace_none_with_none_val(field.default)
    elif field.default_factory is not MISSING:
        return field.default_factory()
