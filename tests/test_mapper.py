import sys
from pathlib import Path

# Ensure package import works when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cargos_api import DataToCargosMapper, models as m


def test_format_helpers():
    assert DataToCargosMapper.format_date("2025-01-02") == "02/01/2025"
    assert DataToCargosMapper.format_datetime("2025-01-02T03:04:05").startswith("02/01/2025 03:04")
    assert DataToCargosMapper.pad_field("ab", 4) == "AB  "


def test_map_record_length():
    booking = m.BookingData(
        id="1",
        creation_date="2025-01-01T10:00:00",
        from_date="2025-01-01T11:00:00",
        to_date="2025-01-02T11:00:00",
        customer=m.Customer(
            firstname="Manuel",
            lastname="Ferraro",
            birth_date="1990-01-01",
            birth_place="Genova",
            citizenship="Italia",
            document_id="CV2WD23A",
            cellphone="0771000000",
        ),
        car=m.Car(brand="Mercedes", model="Classe A", plate="ABC123", color="Bianco"),
        delivery_place=m.Address(address="Via annibale mastrantonio", address_city="Genova"),
        return_place=m.Address(address="Via dei medici", address_city="Verona"),
    )
    operator = m.Operator(id="SYSTEM", agency_id="1", agency_name="VIVARENT", city="Roma", address="Via libetta 42", phone="0771000000")
    rec = DataToCargosMapper().map_booking_to_cargos(booking, operator)
    assert isinstance(rec, str) and len(rec) == 1505

