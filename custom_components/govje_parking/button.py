"""Button platform for GOVJE Parking integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    GOVJE_COORDINATOR,
    GOVJE_NAME,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up GOVJE Parking button platform."""
    hass_data = hass.data[DOMAIN][entry.entry_id]
    coordinator = hass_data[GOVJE_COORDINATOR]
    name = hass_data[GOVJE_NAME]

    async_add_entities([JerseyParkingRefreshButton(coordinator, name)])


class JerseyParkingRefreshButton(CoordinatorEntity, ButtonEntity):
    """Button to refresh GOVJE Parking data."""

    def __init__(self, coordinator, name):
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_name = f"{name} Refresh Data"
        self._attr_unique_id = f"{DOMAIN}_refresh_button"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:refresh"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, name)},
            "name": name,
            "manufacturer": "Government of Jersey",
            "model": "Parking Information",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug("Refresh button pressed, updating parking data")
        await self.coordinator.async_refresh()
