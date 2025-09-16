"""Sensor platform for GOVJE Parking integration."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    GOVJE_COORDINATOR,
    GOVJE_NAME,
    ATTR_LAST_UPDATED,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class JerseyParkingSensorEntityDescription(SensorEntityDescription):
    """Class describing GOVJE Parking sensor entities."""

    value_fn: Callable[[dict[str, Any], str], StateType] = None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up GOVJE Parking sensor platform."""
    hass_data = hass.data[DOMAIN][entry.entry_id]
    coordinator = hass_data[GOVJE_COORDINATOR]
    name = hass_data[GOVJE_NAME]

    entities = []
    
    # Get car parks dynamically from coordinator data
    car_parks = []
    if coordinator.data:
        car_parks = list(coordinator.data.keys())
        _LOGGER.info("Dynamically loaded car parks: %s", car_parks)
    else:
        _LOGGER.warning("No car park data available yet, will be added when data is fetched")
    
    # Create a sensor entity for each car park
    for car_park_name in car_parks:
        entities.append(
            JerseyParkingSensor(
                coordinator=coordinator,
                name=name,
                car_park_name=car_park_name,
            )
        )
        
    # Add diagnostic sensors for last scrape and last update
    entities.append(
        LastScrapeSensor(
            coordinator=coordinator,
            name=name,
        )
    )
    
    entities.append(
        LastUpdateSensor(
            coordinator=coordinator,
            name=name,
        )
    )

    async_add_entities(entities)


class JerseyParkingSensor(
    CoordinatorEntity, SensorEntity
):
    """Implementation of a GOVJE Parking sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
        car_park_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._car_park_name = car_park_name
        self._attr_unique_id = f"govje_parking_{car_park_name.lower().replace(' ', '_')}"
        self._attr_name = f"{car_park_name} Parking"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, name)},
            "name": name,
            "manufacturer": "Government of Jersey",
            "model": "Parking Information",
        }
        self._attr_native_unit_of_measurement = "spaces"
        self._attr_device_class = None  # No specific device class for parking spaces
        self._attr_state_class = None  # Disable statistics (min/max/mean)
        self._attr_icon = "mdi:parking"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or self._car_park_name not in self.coordinator.data:
            return None
            
        return self.coordinator.data[self._car_park_name]["free_spaces"]
        
    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return entity specific state attributes."""
        attributes = {}
        
        # Add all extra fields from the car park data as attributes
        if self.coordinator.data and self._car_park_name in self.coordinator.data:
            car_park_data = self.coordinator.data[self._car_park_name]
            for field, value in car_park_data.items():
                # Skip free_spaces, last_updated, and name fields
                if field not in ["free_spaces", "last_updated", "name"]:
                    # Map field names to human-readable names
                    if field == "carparkOpen":
                        attr_name = "Car Park Open"
                    elif field == "carparkInformation":
                        attr_name = "Car Park Information"
                    elif field == "numberOfUnusableSpaces":
                        attr_name = "Number Of Unusable Spaces"
                    elif field == "numberOfSpacesConsideredLow":
                        attr_name = "Number Of Spaces Considered Low"
                    elif field == "code":
                        attr_name = "Code"
                    elif field == "type":
                        attr_name = "Type"
                    elif field == "status":
                        attr_name = "Status"
                    else:
                        # For any other fields, convert to title case with spaces
                        attr_name = field.replace('_', ' ').title()
                    
                    attributes[attr_name] = value
        
        return attributes


class LastScrapeSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a Last Scrape sensor."""

    _attr_entity_registry_enabled_default = False
    _attr_entity_registry_visible_default = False

    def __init__(self, coordinator: DataUpdateCoordinator, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "govje_parking_last_scrape"
        self._attr_name = "GOVJE Parking Last Scrape"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, name)},
            "name": name,
            "manufacturer": "Government of Jersey",
            "model": "Parking Information",
        }
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if hasattr(self.coordinator, 'last_scrape_time') and self.coordinator.last_scrape_time:
            return self.coordinator.last_scrape_time
        return None


class LastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a Last Update sensor."""

    _attr_entity_registry_enabled_default = False
    _attr_entity_registry_visible_default = False

    def __init__(self, coordinator: DataUpdateCoordinator, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "govje_parking_last_update"
        self._attr_name = "GOVJE Parking Last Update"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, name)},
            "name": name,
            "manufacturer": "Government of Jersey",
            "model": "Parking Information",
        }
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if hasattr(self.coordinator, 'latest_timestamp') and self.coordinator.latest_timestamp:
            return self.coordinator.latest_timestamp
        return None
