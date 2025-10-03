from __future__ import annotations

"""Strict mapper from dataclass models to Ca.R.G.O.S. fixed-width records."""

import logging
from datetime import datetime
from typing import Any

from .exceptions import InvalidInput
from .models import Address, BookingData, Car, Customer, Operator

# The locations dataset is large; we include it as a separate top-level module
# (py_module) in the distribution and import here.
from .locations_loader import location_to_code as _loc_code

logger = logging.getLogger(__name__)


class DataToCargosMapper:
    """Strict mapper from models to Ca.R.G.O.S. 1505-char record.

    The mapper enforces the presence of required fields and raises InvalidInput
    if any are missing or invalid. It does not apply fallback values; validation
    should happen upstream.
    """

    @staticmethod
    def location_to_code(location: str) -> str:
        """Convert location name to Ca.R.G.O.S. code.

        Parameters
        ----------
        location : str
            Location name to look up.

        Returns
        -------
        str
            Ca.R.G.O.S. code.

        Raises
        ------
        ValueError
            If the location is not found.
        """
        return _loc_code(location)

    @staticmethod
    def format_datetime(dt_string: str) -> str:
        """Format ISO-like datetime to 'dd/mm/YYYY HH:MM'."""
        try:
            dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        except Exception as e:
            raise ValueError(f"Invalid datetime format: {dt_string}") from e
        return dt.strftime("%d/%m/%Y %H:%M")

    @staticmethod
    def format_date(dt_string: str) -> str:
        """Format ISO-like date to 'dd/mm/YYYY'."""
        try:
            dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        except Exception as e:
            raise ValueError(f"Invalid date format: {dt_string}") from e
        return dt.strftime("%d/%m/%Y")

    @staticmethod
    def pad_field(value: Any, length: int, align: str = "left") -> str:
        """Pad a value to fixed width with spaces.

        Converts to uppercase string and crops/pads to the requested length.
        """
        s = str(value) if value is not None else ""
        s = s.upper()
        return s.ljust(length)[:length] if align == "left" else s.rjust(length)[:length]

    @staticmethod
    def map_booking_to_cargos(booking_data: BookingData, operator: Operator) -> str:
        """Map a normalized booking into a 1505-character Ca.R.G.O.S. record.

        Required fields (must be present and non-empty):
        - booking_data: id, creation_date, from_date, to_date
        - customer: birth_date, firstname, lastname, birth_place, citizenship
          plus at least one of document_id or driver_licence_number, and one of
          cellphone or email
        - car: brand, model, plate, color
        - delivery_place and return_place: address_city and address
        - operator: id, agency_id, agency_name, city, address, phone
        """
        missing: list[str] = []

        # Direct BookingData fields
        for field in ["id", "creation_date", "from_date", "to_date"]:
            if not getattr(booking_data, field, None):
                missing.append(field)

        # Customer validation
        customer = booking_data.customer
        if not customer:
            missing.append("customer")
        else:
            for field in ["birth_date", "firstname", "lastname", "birth_place", "citizenship"]:
                if not getattr(customer, field, None):
                    missing.append(f"customer.{field}")
            if not (customer.document_id or customer.driver_licence_number):
                missing.append("customer.document_id_or_driver_licence")
            if not (customer.cellphone or customer.email):
                missing.append("customer.cellphone_or_email")

        # Car validation
        car = booking_data.car
        if not car:
            missing.append("car")
        else:
            for field in ["brand", "model", "plate", "color"]:
                if not getattr(car, field, None):
                    missing.append(f"car.{field}")

        # Delivery/Return places validation
        delivery_place = booking_data.delivery_place
        if not delivery_place:
            missing.append("delivery_place")
        else:
            if not delivery_place.address_city:
                missing.append("delivery_place.address_city")
            if not delivery_place.address:
                missing.append("delivery_place.address")

        return_place = booking_data.return_place
        if not return_place:
            missing.append("return_place")
        else:
            if not return_place.address_city:
                missing.append("return_place.address_city")
            if not return_place.address:
                missing.append("return_place.address")

        # Operator validation
        for field in ["id", "agency_id", "agency_name", "city", "address", "phone"]:
            if not getattr(operator, field, None):
                missing.append(f"operator.{field}")

        if missing:
            raise InvalidInput(f"Missing required fields: {', '.join(missing)}")

        pad = DataToCargosMapper.pad_field
        record = ""
        record += pad(str(booking_data.id), 50)  # 1-50 CONTRATTO_ID
        record += pad(DataToCargosMapper.format_datetime(booking_data.creation_date), 16)  # 51-66 CONTRATTO_DATA
        record += pad("1", 1)  # 67 CONTRATTO_TIPOP
        record += pad(DataToCargosMapper.format_datetime(booking_data.from_date), 16)  # 68-83 CHECKOUT_DATA
        record += pad(DataToCargosMapper.location_to_code(delivery_place.address_city), 9, "right")  # 84-92 CHECKOUT_LUOGO_COD
        record += pad(delivery_place.address, 150)  # 93-242 CHECKOUT_INDIRIZZO
        record += pad(DataToCargosMapper.format_datetime(booking_data.to_date), 16)  # 243-258 CHECKIN_DATA
        record += pad(DataToCargosMapper.location_to_code(return_place.address_city), 9, "right")  # 259-267 CHECKIN_LUOGO_COD
        record += pad(return_place.address, 150)  # 268-417 CHECKIN_INDIRIZZO
        record += pad(operator.id, 50)  # 418-467 OPERATORE_ID
        record += pad(operator.agency_id, 30)  # 468-497 AGENZIA_ID
        record += pad(operator.agency_name, 70)  # 498-567 AGENZIA_NOME
        record += pad(DataToCargosMapper.location_to_code(operator.city), 9, "right")  # 568-576 AGENZIA_LUOGO_COD
        record += pad(operator.address, 150)  # 577-726 AGENZIA_INDIRIZZO
        record += pad(operator.phone, 20)  # 727-746 AGENZIA_RECAPITO_TEL
        record += pad("0", 1)  # 747 VEICOLO_TIPO
        record += pad(booking_data.car.brand, 50)  # 748-797
        record += pad(booking_data.car.model, 100)  # 798-897
        record += pad(booking_data.car.plate, 15)  # 898-912 VEICOLO_TARGA
        record += pad(booking_data.car.color, 50)  # 913-962
        record += pad("0", 1)  # 963 VEICOLO_GPS
        record += pad("0", 1)  # 964 VEICOLO_BLOCCOM
        record += pad(booking_data.customer.lastname, 50)  # 965-1014 COGNOME
        record += pad(booking_data.customer.firstname, 30)  # 1015-1044 NOME
        record += pad(DataToCargosMapper.format_date(booking_data.customer.birth_date), 10)  # 1045-1054 NASCITA_DATA
        record += pad(DataToCargosMapper.location_to_code(booking_data.customer.birth_place), 9, "right")  # 1055-1063 NASCITA_LUOGO_COD
        record += pad(DataToCargosMapper.location_to_code(booking_data.customer.citizenship), 9, "right")  # 1064-1072 CITTADINANZA_COD
        record += pad("", 9, "right")  # 1073-1081 RESIDENZA_LUOGO_COD
        addr = ""
        if booking_data.customer.address:
            a = booking_data.customer.address
            addr = f"{a.address or ''} {a.address_number or ''}, {a.address_city or ''}".strip()
        record += pad(addr, 150)  # 1082-1231 RESIDENZA_INDIRIZZO
        record += pad("PATEN", 5)  # 1232-1236 DOCIDE_TIPO_COD
        docno = booking_data.customer.document_id or booking_data.customer.driver_licence_number
        record += pad(docno, 20)  # 1237-1256 DOCIDE_NUMERO
        record += pad(DataToCargosMapper.location_to_code(booking_data.customer.citizenship), 9, "right")  # 1257-1265 DOCIDE_LUOGORIL_COD
        record += pad(docno, 20)  # 1266-1285 PATENTE_NUMERO
        record += pad(DataToCargosMapper.location_to_code(booking_data.customer.citizenship), 9, "right")  # 1286-1294 PATENTE_LUOGORIL_COD
        record += pad(booking_data.customer.cellphone or booking_data.customer.email, 20)  # 1295-1314 RECAPITO
        record += " " * 191  # 1315-1505 SECOND DRIVER

        if len(record) != 1505:
            raise ValueError(f"Generated record has invalid length: {len(record)}")
        return record

