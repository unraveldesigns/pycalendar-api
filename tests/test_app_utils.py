from datetime import date, datetime

import pytest

# --- N.B: On ne teste que les fonctions qui actent en tant que convertisseurs, validateurs ou
# --- operations qui pourront être qualifiées de critiques en commençant par Les plus utilisées.
from pycalendar_api.utils import (
    UtilsError,
    to_bool,
    # ----- Critical Converters Tests -----
    to_date,
    to_datetime,
    to_float,
    to_int,
)

pytestmark = pytest.mark.utils


def test_to_int():
    arg_to_int = ('4', 4.0, '-4', -4.0, None)
    int_output = {4, -4, None}
    test_int = tuple(to_int(i) in int_output for i in arg_to_int)
    assert all(test_int)

    raise_arg = 'ABC'
    with pytest.raises(UtilsError):
        to_int(raise_arg)


def test_to_float():
    arg_to_float = ('4', '-4', '4.2', '-4.2', 4.0, -4.2, None, '0.01', 0.01)
    float_output = {float(4), float(-4), float(4.2), float(-4.2), None, float(0.01)}
    test_float = tuple(to_float(i) in float_output for i in arg_to_float)
    assert all(test_float)

    raise_arg = 'ABC'
    with pytest.raises(UtilsError):
        to_float(raise_arg)


def test_to_bool():
    # --- to_bool: True -----  TRUE  --------
    true_bool_output = {True}
    arg_to_bool_true = ('Y', 'O', 'VRAI', 'TRUE', 'YES', 'OUI', True)
    test_bool_true = tuple(to_bool(i) in true_bool_output for i in arg_to_bool_true)
    assert all(test_bool_true)

    # --- to_bool: False -----  FALSE  --------
    false_bool_output = {False}
    arg_to_bool_false = ('N', 'NO', 'NON', 'FAUX', 'FALSE', False)
    test_bool_false = tuple(to_bool(i) in false_bool_output for i in arg_to_bool_false)
    assert all(test_bool_false)

    raise_arg = 'ABC'
    with pytest.raises(UtilsError):
        to_bool(raise_arg)    


def test_to_date():
    date_output = {date(2023, 7, 22), None}
    arg_to_date = ('22/07/2023', '2023/07/22', '2023-07-22', '22-07-2023', None)
    test_date = tuple(to_date(i) in date_output for i in arg_to_date)
    assert all(test_date)

    raise_arg = 'ABC'
    with pytest.raises(UtilsError):
        to_date(raise_arg)


def test_to_datetime():
    test_output = {datetime(2023, 7, 22, 7, 4), None}
    args_to_test = ('22/07/2023 07:04', '2023-07-22 07:04', '22-07-2023 07:04', '2023/07/22 07:04', None)
    test_datetime = tuple(to_datetime(i) in test_output for i in args_to_test)
    assert all(test_datetime)

    raise_arg = 'ABC'
    with pytest.raises(UtilsError):
        to_datetime(raise_arg)
