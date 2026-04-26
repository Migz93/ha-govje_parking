"""Config flow for govje_parking."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.govje_parking.api import GOVJEParkingApiClientCommunicationError, GOVJEParkingApiClientError
from custom_components.govje_parking.const import DOMAIN, LOGGER
from homeassistant import config_entries

from .schemas import get_user_schema
from .validators import validate_connection

if TYPE_CHECKING:
    from .options_flow import GOVJEParkingOptionsFlow

_ERROR_MAP = {
    GOVJEParkingApiClientCommunicationError: "connection",
}


class GOVJEParkingConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for govje_parking."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GOVJEParkingOptionsFlow:
        """Return the options flow."""
        from .options_flow import GOVJEParkingOptionsFlow  # noqa: PLC0415

        return GOVJEParkingOptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_connection(self.hass)
            except GOVJEParkingApiClientCommunicationError:
                errors["base"] = "connection"
            except GOVJEParkingApiClientError:
                LOGGER.exception("Unexpected error during config flow")
                errors["base"] = "unknown"
            else:
                self._async_abort_entries_match({})
                return self.async_create_entry(
                    title=user_input.get("name", "GOVJE Parking"),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=get_user_schema(user_input),
            errors=errors,
        )


__all__ = ["GOVJEParkingConfigFlowHandler"]
