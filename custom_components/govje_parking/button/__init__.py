"""Button platform for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.const import PARALLEL_UPDATES as PARALLEL_UPDATES

from .refresh import ENTITY_DESCRIPTIONS, GOVJEParkingRefreshButton

if TYPE_CHECKING:
    from custom_components.govje_parking.data import GOVJEParkingConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GOVJEParkingConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    async_add_entities(
        GOVJEParkingRefreshButton(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )
