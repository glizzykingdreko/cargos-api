from cargos_api.locations_loader import CatalogLoader
from cargos_api.models import Address, Car, Customer, Operator, BookingData
from cargos_api.mapper import CargosRecordMapper

# Optional: a fallback that returns a sentinel code for *any* missing key
def my_fallback(key: str, kind: str) -> str:
    # You can log or route certain kinds differently, return a default, etc.
    # Returning a string means "accept and proceed"; raise to fail hard.
    if kind == "location":
        return "000000000"
    if kind == "document":
        return "UNK00"
    if kind in ("payment", "vehicle"):
        return "0"
    return "0"

# 1) Create the loader pointing to your installed package
#    If your package on PyPI is named "takion_cargos", and docs live in takion_cargos/docs/*.csv:
loader = CatalogLoader(
    package="takion_cargos",
    docs_subpackage="docs",
    fallback=my_fallback,  # or None to hard-fail on misses, or a constant like "000000000"
)

# 2) Resolve codes from human labels in your CSVs
milano_code = int(loader.location_code("MILANO"))               # 9-digit string -> int
roma_code = int(loader.location_code("ROMA"))

doc_code = loader.document_type_code("CARTA DI IDENTITA'")      # 5 chars
veh_code = loader.vehicle_type_code("Autovetture")              # 1 char
pay_code = loader.payment_type_code("Carta di Credito")         # 1 char

# 3) Build your objects
operator = Operator(
    id="OP-ACME-01",
    agency_id="AG-MI-01",
    agency_name="ACME RENT MILANO DUOMO",
    agency_place_code=milano_code,
    agency_address="PIAZZA DUOMO 3, MILANO",
    agency_phone="+39021234567",
)

car = Car(
    type_code=veh_code,
    brand="FIAT",
    model="PANDA 1.0",
    plate="AB123CD",
    color="NERO",
    has_gps=True,
    has_immobilizer=False,
)

customer = Customer(
    surname="ROSSI",
    name="MARCO",
    birth_date="1990-03-12",                 # mapper formats -> dd/mm/YYYY
    birth_place_code=roma_code,
    citizenship_code=roma_code,
    residence=Address(location_code=milano_code, street="VIA GARIBALDI 10, MILANO"),
    id_doc_type_code=doc_code,
    id_doc_number="AX1234567",
    id_doc_issuing_place_code=roma_code,
    driver_licence_number="B1234567890",
    driver_licence_issuing_place_code=milano_code,
    contact="+393331234567",
)

booking = BookingData(
    contract_id="ACME-2025-000001",
    contract_datetime="2025-10-06T10:30:00",  # -> 06/10/2025 10:30
    payment_type_code=pay_code,               # 1 char from table
    checkout_datetime="2025-10-06T11:00:00",
    checkout_place=Address(location_code=milano_code, street="VIA ROMA 1, MILANO"),
    checkin_datetime="2025-10-10T09:00:00",
    checkin_place=Address(location_code=milano_code, street="VIA TORINO 5, MILANO"),
    operator=operator,
    car=car,
    customer=customer,
    second_driver=None,                       # or provide a fully-filled SecondDriver(...)
)

# 4) Build the fixed-width record
mapper = CargosRecordMapper()
record = mapper.build_record(booking)
assert len(record) == CargosRecordMapper.RECORD_LENGTH
print(record)  # 1505 characters, ready for Check/Send