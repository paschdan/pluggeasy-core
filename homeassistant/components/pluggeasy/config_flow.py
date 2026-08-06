"""Config flow for Pluggeasy."""

from typing import Any

import voluptuous as vol
from homeassistant.components.modbus_connection import (
    ConnectionNotReady,
    async_get_unit,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    ConfigEntrySelector,
    ConfigEntrySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)
from modbus_connection import ModbusError
from pluggeasy_modbus import Pluggeasy

from .const import CONF_CONNECTION, CONF_UNIT_ID, DEFAULT_UNIT_ID, DOMAIN

STEP_USER = vol.Schema(
    {
        vol.Required(CONF_CONNECTION): ConfigEntrySelector(
            ConfigEntrySelectorConfig(integration="modbus_connection")
        ),
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): NumberSelector(
            NumberSelectorConfig(min=1, max=247, step=1, mode=NumberSelectorMode.BOX)
        ),
    }
)


class PluggeasyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pluggeasy."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick a Modbus connection and unit ID, then verify connectivity."""
        errors: dict[str, str] = {}
        if user_input is not None:
            conn = user_input[CONF_CONNECTION]
            unit_id = int(user_input[CONF_UNIT_ID])
            await self.async_set_unique_id(f"{conn}_{unit_id}")
            self._abort_if_unique_id_configured()
            if not await self._async_test_connection(user_input):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Pluggeasy", data=user_input)
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER, errors=errors
        )

    async def _async_test_connection(self, data: dict[str, Any]) -> bool:
        """Borrow a unit and do one device update to verify connectivity."""
        try:
            unit = async_get_unit(
                self.hass, data[CONF_CONNECTION], int(data[CONF_UNIT_ID])
            )
            device = Pluggeasy(unit)
            await device.async_update()
        except (ConnectionNotReady, ModbusError, OSError):
            return False
        return True
