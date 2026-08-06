"""DataUpdateCoordinator that polls the Pluggeasy ventilation unit."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from modbus_connection import ModbusError
from pluggeasy_modbus import Pluggeasy

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

type PluggeasyConfigEntry = ConfigEntry[PluggeasyCoordinator]


class PluggeasyCoordinator(DataUpdateCoordinator[Pluggeasy]):
    """Refreshes every sub-system on a schedule.

    ``async_update`` fans out to each component (each reads only its own
    registers), so adding/removing entities never changes what is polled. The
    ``modbus_connection`` entry owns the connection; this coordinator only reads.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entry: PluggeasyConfigEntry,
        device: Pluggeasy,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device

    async def _async_update_data(self) -> Pluggeasy:
        try:
            await self.device.async_update()
        except ModbusError as err:
            raise UpdateFailed(f"Error communicating with Pluggeasy: {err}") from err
        return self.device
