"""Device info utilities for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


def create_device_info(config_entry: ConfigEntry) -> DeviceInfo:
    """Create the shared DeviceInfo for all entities in this config entry."""
    return DeviceInfo(
        identifiers={(config_entry.domain, config_entry.entry_id)},
        name=config_entry.title,
        manufacturer="Government of Jersey",
        model="Parking API",
    )
