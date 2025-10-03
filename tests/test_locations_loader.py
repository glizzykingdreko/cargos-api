import sys
from pathlib import Path

# Ensure package import in test env without install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import pytest
from cargos_api.locations_loader import location_to_code, get_locations


def test_location_to_code_case_insensitive():
    assert location_to_code('roma') == location_to_code('ROMA')


def test_location_not_found_raises():
    with pytest.raises(ValueError):
        location_to_code('ThisDoesNotExist')


def test_expired_location_not_present():
    # Known expired entry in dataset (has DataFineVal), should not be loadable
    with pytest.raises(ValueError):
        location_to_code('Abbadia Alpina')


def test_get_locations_contains_expected_keys():
    m = get_locations()
    # A few well-known entries
    for k in ['roma', 'genova', 'italia']:
        assert k in m and 'code' in m[k]

