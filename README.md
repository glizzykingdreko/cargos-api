# cargos-api


[![PyPI](https://img.shields.io/pypi/v/cargos-api.svg)](https://pypi.org/project/cargos-api/) [![Python Versions](https://img.shields.io/pypi/pyversions/cargos-api.svg)](https://pypi.org/project/cargos-api/) [![License](https://img.shields.io/pypi/l/cargos-api.svg)](#license)


A small Python library to build and submit rental booking records to the Italian Police Ca.R.G.O.S. API.

## Table of Contents
- [cargos-api](#cargos-api)
- [Table of Contents](#table-of-contents)
- [Install](#install)
- [Quick start](#quick-start)
- [Formatting the data](#formatting-the-data)
  - [Required fields](#required-fields)
  - [Optional fields](#optional-fields)
  - [Location and country codes](#location-and-country-codes)
- [API usage notes](#api-usage-notes)

---

This repository was created to interact with the Ca.R.G.O.S. APIs for a client who needed to automate the submission of rental booking details to the Italian Police.

The official documentation (see [docs.pdf](./docs/docs.pdf)) is difficult to follow and sparse on examples. The goal of this project is to provide a clean, documented Python module that makes the integration straightforward and consistent.

This module handles all the location -> id conversions, data formatting and submission to the Ca.R.G.O.S. API.

---

## Install

```
pip install cargos-api
```

## Quick start

```python
from cargos_api import CargosAPI, DataToCargosMapper, models as m

# Provide your credentials
api = CargosAPI(username="...", password="...", api_key="...")

# Prepare data
booking = m.BookingData(
    id="1",
    creation_date="2025-01-01T10:00:00",
    from_date="2025-01-01T11:00:00",
    to_date="2025-01-02T11:00:00",
    customer=m.Customer(
        firstname="Mario",
        lastname="Rossi",
        birth_date="1990-01-01",
        birth_place="Genova",
        citizenship="Italia",
        document_id="XYZ123",
        cellphone="0000000000",
    ),
    car=m.Car(
        brand="Fiat",
        model="Panda",
        plate="AB123CD",
        color="Bianco"
    ),
    delivery_place=m.Address(
        address="Via X 1",
        address_city="Genova"
    ),
    return_place=m.Address(
        address="Via Y 2",
        address_city="Verona"
    ),
)
operator = m.Operator(
    id="SYSTEM",
    agency_id="1",
    agency_name="ACME",
    city="Roma",
    address="Via Z",
    phone="0000"
)

# Map to Ca.R.G.O.S. fixed-width record (1505 chars)
record = DataToCargosMapper().map_booking_to_cargos(booking, operator)

# Validate or send
api.check_contracts([record])
# api.send_contracts([record])
```

## Formatting the data

This library exposes typed dataclasses in `cargos_api.models` that you fill with your normalized data and pass to the mapper.

- `BookingData`: `id`, `creation_date`, `from_date`, `to_date`, `car`, `customer`, `delivery_place`, `return_place`
- `Customer`: `firstname`, `lastname`, `birth_date`, `birth_place`, `citizenship`, `document_id` or `driver_licence_number`, `cellphone` or `email`, `address` (optional)
- `Car`: `brand`, `model`, `plate`, `color`
- `Address`: `address_city` and `address` are consumed by the mapper (country optional)
- `Operator`: `id`, `agency_id`, `agency_name`, `city`, `address`, `phone`

### Required fields
The mapper validates inputs and raises `InvalidInput` if anything is missing:
- booking: `id`, `creation_date`, `from_date`, `to_date`
- customer: `birth_date`, `firstname`, `lastname`, `birth_place`, `citizenship`, and one of (`document_id`, `driver_licence_number`) and one of (`cellphone`, `email`)
- car: `brand`, `model`, `plate`, `color`
- delivery_place: `address_city`, `address`
- return_place: `address_city`, `address`
- operator: `id`, `agency_id`, `agency_name`, `city`, `address`, `phone`

### Optional fields
- `Customer.address` is emitted as free-text in the record when provided
- `Address.address_country` is currently not mapped to a dedicated field

### Location and country codes
- Location names (cities/countries) are resolved to Ca.R.G.O.S. codes using a packaged CSV dataset
- Lookup is case-insensitive; expired entries (with `DataFineVal`) are ignored
- If a name is not found, the mapper raises a `ValueError`

## API usage notes
- `CargosAPI.get_token()` fetches the token using HTTP Basic auth
- The `api_key` must be exactly 48 characters: first 32 chars are the AES key and the last 16 chars are the IV used to encrypt the bearer token
- Use `check_contracts(records)` to validate records before submission; use `send_contracts(records)` to submit them

## Example: minimal end-to-end flow
```python
from cargos_api import CargosAPI, DataToCargosMapper, models as m

api = CargosAPI(username="ORG", password="PASS", api_key="...48-chars...")
booking = m.BookingData(
    id="123",
    creation_date="2025-01-05T09:00:00",
    from_date="2025-01-06T10:00:00",
    to_date="2025-01-07T10:00:00",
    customer=m.Customer(
        firstname="Anna", lastname="Bianchi", birth_date="1985-05-20",
        birth_place="Roma", citizenship="Italia", document_id="DOC1", cellphone="333..."
    ),
    car=m.Car(brand="VW", model="Golf", plate="ZZ999ZZ", color="Nero"),
    delivery_place=m.Address(address="Via A 10", address_city="Roma"),
    return_place=m.Address(address="Via B 20", address_city="Roma"),
)
operator = m.Operator(id="SYS", agency_id="AG1", agency_name="ACME", city="Roma", address="Via C 30", phone="06...")
record = DataToCargosMapper().map_booking_to_cargos(booking, operator)
api.check_contracts([record])
```

## Troubleshooting
- `ValueError`: location not found → check the spelling of city/country names
- `InvalidInput`: missing fields → read the error message for which fields are missing
- `InvalidResponse`: HTTP errors → network issues or server response with `errore` field

## Building something with it?
If you nee dhelp implementing this in your project, please reach out.


## Author

If you found this project helpful or interesting, consider starring the repo and following me for more security research and tools, or buy me a coffee to keep me up

<p align="center">
  <a href="https://github.com/GlizzyKingDreko"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://twitter.com/GlizzyKingDreko"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://medium.com/@GlizzyKingDreko"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
  <a href="https://discord.com/users/GlizzyKingDreko"><img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="mailto:glizzykingdreko@protonmail.com"><img src="https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white" alt="Email"></a>
  <a href="https://buymeacoffee.com/glizzykingdreko"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white" alt="Buy Me a Coffee"></a>
</p>

---
