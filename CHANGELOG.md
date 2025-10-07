# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog; versions follow SemVer.


## [0.2.4] - 2025-10-07
### Changed
- CargosAPI.send_contracts now returns the server JSON as-is (list of results) and no longer inspects `errore` to raise `InvalidResponse`. Callers should handle any error semantics present in the response payload.
- Removed internal info log on successful send; behavior is now side-effect free.


## [0.2.3] - 2025-10-07
### Added
- CargosRecordMapper: `location_name_from_code(code)` to convert a Ca.R.G.O.S. luogo code (e.g., 412058091) to its city/country name using the packaged `luoghi.csv` catalog.


## [0.2.2] - 2025-10-07
### Changed
- Version bump to 0.2.2 for public release and tagging.

### Added
- Mapper: `build_record(..., with_map=True)` to return the record plus a JSON-like mapping of fields to padded slices.
- Mapper: `collect_errors=True` to collect validation issues instead of raising, returning `(record, errors)` or `(record, mapping, errors)`.
- CI: Verify all packaged CSV catalogs (luoghi, tipo_documento, tipo_pagamento, tipo_veicolo) are present in the wheel.



## [0.2.1] - 2025-10-07
### Added
- Mapper: `build_record(..., collect_errors=True)` to collect validation issues instead of raising exceptions. The return shape becomes `(record, errors)` or `(record, mapping, errors)` when `with_map=True`.
  Captured errors include:
  - Residence pairing (code + street)
  - Second driver all-or-nothing requirement
  - Overall record length mismatch
  - Missing required minima (`_validate_required_minima`)


## [0.2.0] - 2025-10-06
### Added
- CargosRecordMapper.build_record now supports an optional flag `with_map=True` to also return a JSON-like mapping of field names to their exact padded slices. Useful for validating input data prior to submission.
- Packaged additional catalogs under `cargos_api/data/`:
  - `tipo_documento.csv` (document types)
  - `tipo_pagamento.csv` (payment types)
  - `tipo_veicolo.csv` (vehicle types)
- CatalogLoader class (in `locations_loader.py`) documented for resolving labels to Ca.R.G.O.S. codes using packaged CSVs.

### Changed
- Renamed mapper class `DataToCargosMapper` to `CargosRecordMapper`.
- Renamed `map_booking_to_cargos(...)` to `build_record(...)`.
- Updated README with new API, with_map usage, and lookup table notes.
- CI now verifies that all four CSVs are packaged in the wheel.

### Fixed
- Ensured all CSVs (luoghi, tipo_documento, tipo_pagamento, tipo_veicolo) are included in the wheel via package data configuration.

## [0.1.0] - 2025-xx-xx
### Added
- Initial package structure with src layout, pyproject metadata, and first public release.
- Mapping to 1505-char fixed-width record and basic CSV-based location lookups.

