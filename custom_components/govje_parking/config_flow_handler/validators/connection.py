"""Connection validator for govje_parking config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.api import GOVJEParkingApiClient
from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_connection(hass: HomeAssistant) -> None:
    """Test that the Government of Jersey parking API is reachable.

    Args:
        hass: The Home Assistant instance.

    Raises:
        GOVJEParkingApiClientCommunicationError: If the API cannot be reached.
        GOVJEParkingApiClientError: For unexpected errors.
    """
    session = async_get_clientsession(hass)
    client = GOVJEParkingApiClient(session=session)
    await client.async_get_data()
