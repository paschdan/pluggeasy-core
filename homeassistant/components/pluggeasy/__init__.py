"""The Pluggeasy integration.

Pluggeasy is a Modbus ventilation device. This integration does not own its
connection: it borrows a ``ModbusUnit`` from a ``modbus_connection`` config entry
(chosen in the config flow) and hands it to the ``pluggeasy_modbus`` library. The
``modbus_connection`` entry owns the connection lifecycle; this integration
reloads when the connection drops so it re-borrows on the rebuilt connection.
"""

from homeassistant.components.modbus_connection import async_get_unit
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from pluggeasy_modbus import Pluggeasy

from .const import CONF_CONNECTION, CONF_UNIT_ID
from .coordinator import PluggeasyConfigEntry, PluggeasyCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: PluggeasyConfigEntry) -> bool:
    """Set up Pluggeasy from a config entry.

    ``async_get_unit`` raises ``ConnectionNotReady`` (a ``ConfigEntryNotReady``)
    if the shared connection is missing or not loaded; letting it propagate gives
    Home Assistant's setup retry.
    """
    unit = async_get_unit(
        hass, entry.data[CONF_CONNECTION], int(entry.data[CONF_UNIT_ID])
    )
    device = Pluggeasy(unit)
    coordinator = PluggeasyCoordinator(hass, entry, device)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    # The borrowed unit is bound to modbus_connection's current connection. When
    # that connection drops, modbus_connection rebuilds it; reload so we re-borrow
    # a unit on the fresh connection instead of holding a dead one.
    entry.async_on_unload(
        unit.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PluggeasyConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
