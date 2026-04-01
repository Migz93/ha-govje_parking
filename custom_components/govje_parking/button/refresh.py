"""Refresh button for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.entity import GOVJEParkingEntity
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.govje_parking.coordinator import GOVJEParkingDataUpdateCoordinator

ENTITY_DESCRIPTIONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="refresh",
        translation_key="refresh",
        icon="mdi:refresh",
        entity_category=EntityCategory.DIAGNOSTIC,
        has_entity_name=True,
    ),
)


class GOVJEParkingRefreshButton(ButtonEntity, GOVJEParkingEntity):
    """Button that triggers an immediate coordinator refresh."""

    def __init__(
        self,
        coordinator: GOVJEParkingDataUpdateCoordinator,
        entity_description: ButtonEntityDescription,
    ) -> None:
        """Initialise the refresh button."""
        super().__init__(coordinator, entity_description)

    async def async_press(self) -> None:
        """Trigger an immediate data refresh."""
        await self.coordinator.async_request_refresh()
