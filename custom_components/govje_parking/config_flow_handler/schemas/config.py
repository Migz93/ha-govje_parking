"""Config flow schemas for govje_parking."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.helpers import selector


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """Get schema for the user step (initial setup).

    Args:
        defaults: Optional dict of default values.

    Returns:
        Voluptuous schema with an optional name field.
    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Optional(
                "name",
                default=defaults.get("name", "GOVJE Parking"),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
        },
    )


__all__ = ["get_user_schema"]
