import datetime as dt
import re

from dateutil import parser


class UtilsError(Exception):
    """Exception de base des fonctions du module Utils"""


def to_date(value: str|None) -> dt.date:
    """Retourne une date depuis un string, format dd/mm/yyyy ou dd-mm-yyyy ou dd.mm.yyyy"""
    if isinstance(value, dt.datetime):
        return value.date()

    if isinstance(value, dt.date):
        return value

    if value in (None, '', 'None', '-'):
        return None

    try:
        if isinstance(value, str):
            sep = ' '
            dayfirst = True

            if '-' in value:
                sep = '-'
            elif '/' in value:
                sep = '/'
            elif '.' in value:
                sep = '.'

            first, *sp_value = value.split(sep)
            # Test pour éviter que les cdc ne soient interprétées MM/DD/YYYY
            if int(first) > 31:
                dayfirst = False

            return parser.parse(value, dayfirst=dayfirst).date()

        else:
            return value

    except (ValueError, parser.ParserError) as err:
        msg = f"to_date: La date passée est mal formatée: {value}"
        raise UtilsError(msg) from err


def to_datetime(value: str) -> dt.datetime:
    """
    Retourne un datetime depuis un string, format dd/mm/yyyy ou dd-mm-yyy
    """
    if value in (None, '', 'None'):
        return None

    if isinstance(value, dt.datetime):
        return value

    if isinstance(value, dt.date):
        rv = dt.datetime.fromisoformat(str(value))
        return rv

    try:
        if isinstance(value, str):
            sep = ' '
            dayfirst = True

            if '-' in value:
                sep = '-'
            elif '/' in value:
                sep = '/'
            elif '.' in value:
                sep = '.'

            first, *sp_value = value.split(sep)
            if int(first) > 31:
                dayfirst = False

            return parser.parse(value, dayfirst=dayfirst)

        else:
            return value

    except (ValueError, parser.ParserError) as err:
        msg = f"to_datetime: La date passée est mal formatée: {value}"
        raise UtilsError(msg) from err


def to_bool(value: str|int) -> bool:
    """Convertit une cdc en booléen selon un mapping simple

    Args:
        value (`str`): Une valeur décrivant un état booléan

    Returns:
        `bool`: True ou False
    """
    svalue = str(value)

    dico = {
        1: True, '1': True,
        'o': True, 'oui': True,
        'vrai': True, 'true': True,
        'y': True, 'yes': True,

        0: False, '0': False,
        'n': False, 'non': False,
        'faux': False,
        'false': False, 'no': False,
        'none': False, 'null': False,
    }

    try:
        return dico[svalue.lower()]

    except KeyError:
        msg = f"to_bool: La valeur passée ne peut être convertie en bool. reçu : {value}"
        raise UtilsError(msg)


def to_float(float_value: str) -> float:
    """Valide et convertit un texte qui représente un nombre rationnel.

    Args:
        float_value (`str`): Valeur en texte

    Returns:
        `float`: Le nombre en unité de base
    """
    if float_value is None:
        return None

    try:
        return float(float_value)

    except (TypeError, ValueError):
        if isinstance(float_value, str):
            stripped = float_value.strip()
            zero_str = ('NC', '-', '', 'ND')
            if stripped in zero_str:
                return 0
            if ',' in float_value:
                return float(float_value.replace(',', '.').replace(' ', ''))

        msg = f"to_float: La valeur passée ne peut être convertie en float. reçu : {float_value}"
        raise UtilsError(msg)


def to_int(int_value: str) -> int:
    """Valide un texte qui représente un nombre entier.

    Args:
        int_value (`str`): nombre entier en texte

    Returns:
        `int`: Le nombre entier en unité de base
    """
    if int_value is None:
        return None

    try:
        ivalue = int(int_value)
        return ivalue

    except (TypeError, ValueError):
        msg = f"to_int: La valeur passée ne peut être convertie en int. reçu : {int_value}"
        raise UtilsError(msg)
