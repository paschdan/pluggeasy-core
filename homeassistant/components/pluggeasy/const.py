"""Constants for the Pluggeasy integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "pluggeasy"

CONF_CONNECTION: Final = "connection_entry_id"
CONF_UNIT_ID: Final = "unit_id"

DEFAULT_UNIT_ID: Final = 1  # the ventilation unit's default Modbus station address

# A ventilation unit changes slowly, but we poll on a fixed schedule.
SCAN_INTERVAL: Final = timedelta(seconds=30)
