"""Diagnostics support for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.redact import async_redact_data

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import GOVJEParkingConfigEntry

# No sensitive fields for this unauthenticated integration, but include for future-proofing
TO_REDACT: set[str] = set()


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: GOVJEParkingConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.coordinator
    integration = entry.runtime_data.integration

    data = coordinator.data or {}
    car_parks = data.get("car_parks", {})

    return {
        "entry": {
            "entry_id": entry.entry_id,
            "version": entry.version,
            "domain": entry.domain,
            "title": entry.title,
            "state": str(entry.state),
            "data": async_redact_data(dict(entry.data), TO_REDACT),
            "options": async_redact_data(dict(entry.options), TO_REDACT),
        },
        "integration": {
            "name": integration.name,
            "version": integration.version,
            "domain": integration.domain,
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "update_interval": str(coordinator.update_interval),
            "last_scrape_time": coordinator.last_scrape_time,
            "api_timestamp": data.get("timestamp"),
            "car_park_count": len(car_parks),
            "car_park_names": sorted(car_parks.keys()),
        },
        "error": {
            "last_exception": str(coordinator.last_exception) if coordinator.last_exception else None,
            "last_exception_type": (type(coordinator.last_exception).__name__ if coordinator.last_exception else None),
        },
    }
