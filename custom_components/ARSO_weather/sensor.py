"""Sensor platform for ARSO_weather."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ARSO_weather",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        ARSOSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class ARSOSensor(ARSOEntity, SensorEntity):
    """ARSO_weather Sensor class."""

    def __init__(
        self,
        coordinator: ARSODataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        #return self.coordinator.data.get("body")
        return self.coordinator.data
