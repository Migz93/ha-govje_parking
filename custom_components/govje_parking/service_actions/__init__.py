"""Service actions package for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.govje_parking.const import DOMAIN, LOGGER
from homeassistant.core import ServiceCall

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

SERVICE_RELOAD_DATA = "reload_data"


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register service actions at component level (Silver Quality Scale requirement)."""

    async def handle_reload_data(_call: ServiceCall) -> None:
        """Trigger an immediate data refresh for all config entries."""
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            LOGGER.warning("No config entries found for %s", DOMAIN)
            return
        for entry in entries:
            await entry.runtime_data.coordinator.async_request_refresh()

    if not hass.services.has_service(DOMAIN, SERVICE_RELOAD_DATA):
        hass.services.async_register(
            DOMAIN,
            SERVICE_RELOAD_DATA,
            handle_reload_data,
        )
