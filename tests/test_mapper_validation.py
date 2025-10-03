import sys
from pathlib import Path

# Ensure package import in test env without install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import pytest
from cargos_api.mapper import DataToCargosMapper
from cargos_api import models as m
from cargos_api.exceptions import InvalidInput


def test_missing_required_fields_raises_invalid_input():
    b = m.BookingData(
        id='1',
        creation_date='2025-01-01T10:00:00',
        from_date='2025-01-01T11:00:00',
        to_date='2025-01-02T11:00:00',
        # car missing
        customer=m.Customer(firstname='A', lastname='B', birth_date='1990-01-01', birth_place='Genova', citizenship='Italia'),
        delivery_place=m.Address(address='Via', address_city='Genova'),
        return_place=m.Address(address='Via', address_city='Verona'),
    )
    op = m.Operator(id='SYSTEM', agency_id='1', agency_name='ACME', city='Roma', address='addr', phone='0')
    with pytest.raises(InvalidInput) as e:
        DataToCargosMapper().map_booking_to_cargos(b, op)
    # Ensure the message points to the missing car
    assert 'car' in str(e.value)


def test_format_datetime_invalid():
    with pytest.raises(ValueError):
        DataToCargosMapper.format_datetime('not-a-datetime')


def test_record_length_is_1505():
    b = m.BookingData(
        id='1',
        creation_date='2025-01-01T10:00:00',
        from_date='2025-01-01T11:00:00',
        to_date='2025-01-02T11:00:00',
        customer=m.Customer(firstname='A', lastname='B', birth_date='1990-01-01', birth_place='Genova', citizenship='Italia', document_id='X', cellphone='0'),
        car=m.Car(brand='X', model='Y', plate='Z', color='K'),
        delivery_place=m.Address(address='Via', address_city='Genova'),
        return_place=m.Address(address='Via', address_city='Verona'),
    )
    op = m.Operator(id='SYSTEM', agency_id='1', agency_name='ACME', city='Roma', address='addr', phone='0')
    rec = DataToCargosMapper().map_booking_to_cargos(b, op)
    assert len(rec) == 1505

