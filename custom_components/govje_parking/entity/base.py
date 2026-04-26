"""Base entity class for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.const import ATTRIBUTION
from custom_components.govje_parking.coordinator import GOVJEParkingDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class GOVJEParkingEntity(CoordinatorEntity[GOVJEParkingDataUpdateCoordinator]):
    """Base entity class for govje_parking.

    All fixed entities (diagnostic sensors, refresh button) inherit from this class.
    It provides coordinator integration, device info, unique ID, and attribution.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GOVJEParkingDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialise the base entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.domain, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.title,
            manufacturer="Government of Jersey",
            model="Parking API",
        )
