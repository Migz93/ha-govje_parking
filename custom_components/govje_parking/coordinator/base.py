"""Core DataUpdateCoordinator implementation for govje_parking."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from custom_components.govje_parking.api import GOVJEParkingApiClientCommunicationError, GOVJEParkingApiClientError
from custom_components.govje_parking.const import LOGGER
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

if TYPE_CHECKING:
    from custom_components.govje_parking.data import GOVJEParkingConfigEntry


class GOVJEParkingDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator that fetches and distributes car park availability data.

    Polls the Government of Jersey parking API on a configurable interval
    and makes the data available to all entities via coordinator.data.

    Data shape stored in coordinator.data:
        {
            "car_parks": {
                "Sand Street": {"free_spaces": 120, "carparkOpen": True, ...},
                ...
            },
            "timestamp": "2024-01-15T10:30:00",  # from API, may be None
        }

    Attributes:
        config_entry: The config entry for this integration instance.
        last_scrape_time: ISO-formatted local time of the last successful fetch.
    """

    config_entry: GOVJEParkingConfigEntry

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialise the coordinator."""
        super().__init__(*args, **kwargs)
        self.last_scrape_time: str | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the parking API.

        Returns:
            Parsed data dict with "car_parks" and "timestamp" keys.

        Raises:
            UpdateFailed: If the API call fails for any reason.
        """
        try:
            data = await self.config_entry.runtime_data.client.async_get_data()
        except GOVJEParkingApiClientCommunicationError as exception:
            LOGGER.exception("Communication error fetching parking data")
            raise UpdateFailed(
                translation_domain="govje_parking",
                translation_key="update_failed",
            ) from exception
        except GOVJEParkingApiClientError as exception:
            LOGGER.exception("Error fetching parking data")
            raise UpdateFailed(
                translation_domain="govje_parking",
                translation_key="update_failed",
            ) from exception

        self.last_scrape_time = datetime.now().isoformat(timespec="seconds")
        return data
