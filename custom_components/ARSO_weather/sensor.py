"""Sensor platform for ARSO_weather."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass
from homeassistant.const import UnitOfTemperature


from .const import DOMAIN, CONF_LOCATION
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ARSO_weather",
        name="ARSO Sensor",
        icon="mdi:thermometer",
        device_class= SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
)

async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = []
    for entity_description in ENTITY_DESCRIPTIONS:
        entity_description.name = "ARSO Sensor for " + entry.data[CONF_LOCATION]
        devices.append(
            ARSOSensor(
                coordinator=coordinator,
                entity_description=entity_description,
            )
        )
    async_add_devices(devices)

#async def async_setup_entry(hass, entry, async_add_devices):
#    """Set up the sensor platform."""
#    coordinator = hass.data[DOMAIN][entry.entry_id]
#    async_add_devices(
#        ARSOSensor(
#            coordinator=coordinator,
#            entity_description=entity_description,
#        )
#        for entity_description in ENTITY_DESCRIPTIONS
#    )

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
        meteo_data_location = next((item for item in self.coordinator.data if item["domain_title"] == "VOGEL"), False)
        return meteo_data_location["t"]
