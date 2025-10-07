from models import Address, Car, Customer, Operator, BookingData, SecondDriver
from mapper import CargosRecordMapper

mapper = CargosRecordMapper()

booking = BookingData(
    contract_id="ABC-2025-0001",
    contract_datetime="2025-10-06T10:30:00",   # will become 06/10/2025 10:30
    payment_type_code="0",                      # example, from Tabella Tipo Pagamenti
    checkout_datetime="2025-10-06T11:00:00",
    checkout_place=Address(location_code=123456789, street="VIA ROMA 1, MILANO"),
    checkin_datetime="2025-10-10T09:00:00",
    checkin_place=Address(location_code=987654321, street="VIA TORINO 5, MILANO"),
    operator=Operator(
        id="OP-001",
        agency_id="AG-77",
        agency_name="FAST RENT MILANO",
        agency_place_code=200000001,
        agency_address="PIAZZA DUOMO 3, MILANO",
        agency_phone="+39020123456",
    ),
    car=Car(
        type_code="A",
        brand="FIAT",
        model="PANDA",
        plate="AB123CD",
        color="NERO",
        has_gps=True,
        has_immobilizer=False
    ),
    customer=Customer(
        surname="ROSSI",
        name="MARCO",
        birth_date="1990-03-12",
        birth_place_code=201000001,
        citizenship_code=201000001,
        residence=Address(location_code=201000001, street="VIA GARIBALDI 10, MILANO"),
        id_doc_type_code="CIE",
        id_doc_number="AX1234567",
        id_doc_issuing_place_code=201000001,
        driver_licence_number="B1234567890",
        driver_licence_issuing_place_code=201000001,
        contact="+393331234567"
    ),
    second_driver=None  # or a SecondDriver(...) with all fields populated
)

record_line = mapper.build_record(booking)
assert len(record_line) == CargosRecordMapper.RECORD_LENGTH