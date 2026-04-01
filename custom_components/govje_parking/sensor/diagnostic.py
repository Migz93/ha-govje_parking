"""Diagnostic sensors for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.entity import GOVJEParkingEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.govje_parking.coordinator import GOVJEParkingDataUpdateCoordinator

ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="last_scrape",
        translation_key="last_scrape",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        has_entity_name=True,
    ),
    SensorEntityDescription(
        key="last_api_update",
        translation_key="last_api_update",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        has_entity_name=True,
    ),
)


class GOVJEParkingDiagnosticSensor(SensorEntity, GOVJEParkingEntity):
    """Diagnostic sensor showing last scrape time or last API data timestamp."""

    def __init__(
        self,
        coordinator: GOVJEParkingDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialise the diagnostic sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def native_value(self) -> str | None:
        """Return the timestamp value."""
        if self.entity_description.key == "last_scrape":
            return self.coordinator.last_scrape_time
        if self.entity_description.key == "last_api_update":
            return self.coordinator.data.get("timestamp") if self.coordinator.data else None
        return None

    @property
    def available(self) -> bool:
        """Return availability based on coordinator status."""
        return self.coordinator.last_update_success
