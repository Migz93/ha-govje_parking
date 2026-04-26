"""Parking availability sensors for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.govje_parking.const import ATTRIBUTION
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.device_registry import DeviceInfo

if TYPE_CHECKING:
    from custom_components.govje_parking.coordinator import GOVJEParkingDataUpdateCoordinator

_FIELD_LABEL: dict[str, str] = {
    "carparkOpen": "Car Park Open",
    "carparkInformation": "Car Park Information",
    "numberOfUnusableSpaces": "Number Of Unusable Spaces",
    "numberOfSpacesConsideredLow": "Number Of Spaces Considered Low",
    "code": "Code",
    "type": "Type",
    "status": "Status",
}


class GOVJEParkingAvailabilitySensor(SensorEntity):
    """Sensor reporting the number of free spaces in a single car park.

    These entities are created dynamically at setup time — one per open
    car park returned by the API.  They subscribe to the coordinator directly
    rather than inheriting GOVJEParkingEntity because they are not created
    from EntityDescriptions.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "spaces"
    _attr_icon = "mdi:parking"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: GOVJEParkingDataUpdateCoordinator,
        car_park_name: str,
    ) -> None:
        """Initialise the parking availability sensor."""
        super().__init__()
        self.coordinator = coordinator
        self._car_park_name = car_park_name

        from custom_components.govje_parking.utils.string_helpers import slugify_name  # noqa: PLC0415

        slug = slugify_name(car_park_name)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{slug}"
        self._attr_name = car_park_name
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.domain, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.title,
            manufacturer="Government of Jersey",
            model="Parking API",
        )

    @property
    def available(self) -> bool:
        """Return True if the car park is in the latest coordinator data."""
        return self.coordinator.last_update_success and self._car_park_name in self.coordinator.data.get(
            "car_parks", {}
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of free spaces."""
        if not self.available:
            return None
        return self.coordinator.data["car_parks"][self._car_park_name].get("free_spaces")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional car park attributes."""
        if not self.available:
            return {}

        car_park: dict[str, Any] = self.coordinator.data["car_parks"][self._car_park_name]
        return {
            _FIELD_LABEL.get(field, field.replace("_", " ").title()): value
            for field, value in car_park.items()
            if field not in ("free_spaces", "name")
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to coordinator updates."""
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))

    async def async_update(self) -> None:
        """No-op: coordinator handles updates."""
