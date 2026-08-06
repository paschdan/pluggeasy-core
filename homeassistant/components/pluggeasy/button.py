"""Button platform — momentary controls for the ventilation unit."""

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import PluggeasyConfigEntry, PluggeasyCoordinator
from .entity import PluggeasyEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PluggeasyConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Pluggeasy buttons."""
    coordinator = entry.runtime_data
    async_add_entities([PluggeasyButton(coordinator)])


class PluggeasyButton(PluggeasyEntity, ButtonEntity):
    """Button to reset the filter alarm."""

    _attr_name = "Reset Filter Alarm"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = None

    def __init__(self, coordinator: PluggeasyCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator, "controls_reset_filter_alarm", "controls")

    async def async_press(self) -> None:
        """Press the button — write True to reset_filter_alarm coil."""
        await self.coordinator.device.controls.write("reset_filter_alarm", True)
        await self.coordinator.async_request_refresh()
