from __future__ import annotations

"""Dataclasses used by the strict Ca.R.G.O.S. mapper.

These classes provide a clear, typed representation of the data needed to build
Ca.R.G.O.S. fixed-width records. Optional fields default to None. Use together
with DataToCargosMapper for validation and record generation.
"""

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Address:
    """Address information for delivery, return, or customer residence.

    Attributes
    ----------
    address : Optional[str]
        Street name.
    address_number : Optional[str]
        Street number or civic number.
    address_city : Optional[str]
        City/town name (used for Ca.R.G.O.S. location code lookup).
    address_country : Optional[str]
        Country name (not used in the current mapping).
    """

    address: Optional[str] = None
    address_number: Optional[str] = None
    address_city: Optional[str] = None
    address_country: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Operator:
    """Rental operator and agency information.

    Attributes
    ----------
    id : Optional[str]
        Operator identifier.
    agency_id : Optional[str]
        Agency identifier.
    agency_name : Optional[str]
        Agency display name.
    city : Optional[str]
        Agency city (used for Ca.R.G.O.S. location code lookup).
    address : Optional[str]
        Agency street address.
    phone : Optional[str]
        Agency contact phone.
    """

    id: Optional[str] = None
    agency_id: Optional[str] = None
    agency_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Customer:
    """Primary driver/customer identity and contact details.

    Attributes
    ----------
    birth_date : Optional[str]
        Date of birth in ISO-like format (YYYY-MM-DD or full ISO).
    birth_place : Optional[str]
        Birth city/town (used for Ca.R.G.O.S. location code lookup).
    citizenship : Optional[str]
        Citizenship/country (used for Ca.R.G.O.S. location code lookup).
    driver_licence_number : Optional[str]
        Driver's licence number (alternative to document_id).
    firstname : Optional[str]
        Given name.
    lastname : Optional[str]
        Family name.
    address : Optional[Address]
        Residence address (only free-text is currently emitted in the record).
    document_id : Optional[str]
        Identity document number (alternative to driver_licence_number).
    cellphone : Optional[str]
        Primary phone number.
    email : Optional[str]
        Email address.
    """

    birth_date: Optional[str] = None
    birth_place: Optional[str] = None
    citizenship: Optional[str] = None
    driver_licence_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    address: Optional[Address] = None
    document_id: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Car:
    """Vehicle details used in the contract record.

    Attributes
    ----------
    model : Optional[str]
        Vehicle model.
    brand : Optional[str]
        Vehicle brand/manufacturer.
    name : Optional[str]
        Optional marketing name/trim.
    plate : Optional[str]
        Vehicle license plate.
    color : Optional[str]
        Vehicle color.
    """

    model: Optional[str] = None
    brand: Optional[str] = None
    name: Optional[str] = None
    plate: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BookingData:
    """Normalized booking data used for Ca.R.G.O.S. mapping.

    Attributes
    ----------
    id : Optional[str]
        Contract identifier.
    creation_date : Optional[str]
        Contract creation timestamp (ISO-like string).
    from_date : Optional[str]
        Vehicle checkout datetime (ISO-like string).
    to_date : Optional[str]
        Vehicle checkin datetime (ISO-like string).
    car : Optional[Car]
        Vehicle information.
    customer : Optional[Customer]
        Primary driver/customer details.
    delivery_place : Optional[Address]
        Checkout address (city used for location code).
    return_place : Optional[Address]
        Checkin address (city used for location code).
    """

    id: Optional[str] = None
    creation_date: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    car: Optional[Car] = None
    customer: Optional[Customer] = None
    delivery_place: Optional[Address] = None
    return_place: Optional[Address] = None

    def to_dict(self) -> dict:
        return asdict(self)

