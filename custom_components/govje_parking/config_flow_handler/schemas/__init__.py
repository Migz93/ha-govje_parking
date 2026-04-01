"""Data schemas for config flow forms."""

from __future__ import annotations

from custom_components.govje_parking.config_flow_handler.schemas.config import get_user_schema
from custom_components.govje_parking.config_flow_handler.schemas.options import get_options_schema

__all__ = [
    "get_options_schema",
    "get_user_schema",
]
