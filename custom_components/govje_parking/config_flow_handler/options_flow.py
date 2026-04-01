"""Options flow for govje_parking."""

from __future__ import annotations

from typing import Any

from custom_components.govje_parking.config_flow_handler.schemas import get_options_schema
from homeassistant import config_entries


class GOVJEParkingOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for govje_parking."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage integration options (scan interval)."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=get_options_schema(self.config_entry.options),
        )


__all__ = ["GOVJEParkingOptionsFlow"]
