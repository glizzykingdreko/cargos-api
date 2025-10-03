from __future__ import annotations

"""CSV-based loader for Ca.R.G.O.S. locations and countries.

The CSV is expected to have columns: Codice, Descrizione, Provincia, DataFineVal
Only rows without DataFineVal (active) are considered. Keys are normalized to
lowercase for lookup.

Data source defaults to a packaged resource (cargos_api/data/luoghi.csv). When
that resource is not available (e.g., in repo development), it falls back to
`docs/luoghi.csv` at the repository root.
"""

from functools import lru_cache
from typing import Dict
import csv
from pathlib import Path

try:  # Python 3.9+
    from importlib.resources import files as _res_files  # type: ignore
except Exception:  # pragma: no cover
    _res_files = None  # type: ignore


@lru_cache(maxsize=1)
def get_locations() -> Dict[str, Dict[str, str]]:
    """Load locations mapping from CSV.

    Returns
    -------
    dict[str, dict[str, str]]
        Mapping of lowercase name -> {"code": str, "prov": str}
    """
    # 1) Try packaged resource cargos_api/data/luoghi.csv
    csv_path: Path | None = None
    if _res_files is not None:
        try:
            candidate = _res_files("cargos_api").joinpath("data", "luoghi.csv")
            if candidate.is_file():  # type: ignore[attr-defined]
                csv_path = Path(str(candidate))
        except Exception:
            pass

    # 2) Fallback to repo docs/luoghi.csv
    if csv_path is None:
        repo_root = Path(__file__).resolve().parents[2]
        candidate = repo_root / "docs" / "luoghi.csv"
        if candidate.is_file():
            csv_path = candidate

    if csv_path is None:
        raise FileNotFoundError("luoghi.csv not found in package resources or docs/")

    mapping: Dict[str, Dict[str, str]] = {}
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            # Skip expired rows if DataFineVal present
            data_fine = (row.get("DataFineVal") or "").strip()
            if data_fine:
                continue
            name = (row.get("Descrizione") or "").strip().lower()
            code = (row.get("Codice") or "").strip()
            prov = (row.get("Provincia") or "").strip()
            if not name or not code:
                continue
            # Prefer first active entry for a name
            mapping.setdefault(name, {"code": code, "prov": prov})
    return mapping


def location_to_code(name: str) -> str:
    """Return Ca.R.G.O.S. code for a given location/country name.

    Parameters
    ----------
    name : str
        Human-readable name (case-insensitive).

    Returns
    -------
    str
        Code corresponding to the name.

    Raises
    ------
    ValueError
        If the name is not found in the dataset.
    """
    m = get_locations()
    key = (name or "").lower().strip()
    try:
        return m[key]["code"]
    except KeyError as e:
        raise ValueError(f"Location not found: {name}") from e

