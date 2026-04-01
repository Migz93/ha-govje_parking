"""Sensor platform for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.const import PARALLEL_UPDATES as PARALLEL_UPDATES

from .diagnostic import ENTITY_DESCRIPTIONS, GOVJEParkingDiagnosticSensor
from .parking import GOVJEParkingAvailabilitySensor

if TYPE_CHECKING:
    from custom_components.govje_parking.data import GOVJEParkingConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GOVJEParkingConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator

    entities = [
        GOVJEParkingAvailabilitySensor(coordinator=coordinator, car_park_name=name)
        for name in coordinator.data.get("car_parks", {})
    ]
    entities += [
        GOVJEParkingDiagnosticSensor(coordinator=coordinator, entity_description=desc) for desc in ENTITY_DESCRIPTIONS
    ]

    async_add_entities(entities)
