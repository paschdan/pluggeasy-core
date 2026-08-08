"""Fan platform — ventilation speed control via preset modes."""

from typing import Any, ClassVar

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import PluggeasyConfigEntry, PluggeasyCoordinator
from .entity import PluggeasyEntity

_DEFAULT_PRESET = "nominal"

LABEL_TO_MODE: dict[str, str] = {
    "low": "low",
    "medium": "medium",
    "nominal": "high",
    "auto": "auto",
    "snooze": "off",
}

MODE_TO_LABEL: dict[str, str] = {
    "off": "snooze",
    "high": "nominal",
    "low": "low",
    "medium": "medium",
    "auto": "auto",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PluggeasyConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Pluggeasy fan."""
    coordinator = entry.runtime_data
    async_add_entities([PluggeasyFan(coordinator)])


class PluggeasyFan(PluggeasyEntity, FanEntity):
    """Primary fan entity — controls ventilation speed via airflow mode preset."""

    _attr_name = None
    _attr_supported_features = (
        FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
    )
    _attr_preset_modes: ClassVar[list[str]] = [
        "low",
        "medium",
        "nominal",
        "auto",
        "snooze",
    ]

    def __init__(self, coordinator: PluggeasyCoordinator) -> None:
        """Initialize the fan."""
        super().__init__(coordinator, "parameters_selected_airflow", "parameters")

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        eff = self.coordinator.device.effective_airflow_mode()
        return MODE_TO_LABEL.get(eff) if eff is not None else None

    @property
    def is_on(self) -> bool | None:
        """Return True when the fan is running (not in snooze)."""
        mode = self.preset_mode
        if mode is None:
            return None
        return mode != "snooze"

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the ventilation speed preset."""
        lib_mode = LABEL_TO_MODE[preset_mode]
        await self.coordinator.device.async_set_airflow_mode(lib_mode)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn the fan on, optionally to a specific preset (default: nominal)."""
        await self.async_set_preset_mode(preset_mode or _DEFAULT_PRESET)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off by setting snooze mode."""
        await self.async_set_preset_mode("snooze")
