from __future__ import annotations

"""Top-level package for the Ca.R.G.O.S. API client and strict mapper.

This library provides:
- CargosAPI: Thin HTTP client for the Italian Police Ca.R.G.O.S. endpoints
- DataToCargosMapper: Builder for the fixed-width contract records (1505 chars)
- Dataclasses-based models used by the mapper

The public surface avoids side effects (e.g., no logging handlers added) so it can
be embedded in larger applications.
"""

from .api import CargosAPI
from .mapper import DataToCargosMapper
from . import models

__all__ = ["CargosAPI", "DataToCargosMapper", "models"]
__version__ = "0.1.0"

