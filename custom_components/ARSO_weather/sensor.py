"""Sensor platform for ARSO_weather."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, UnitOfPressure, PERCENTAGE
from homeassistant.helpers.entity import generate_entity_id


from .const import DOMAIN, CONF_LOCATION, LOGGER
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ARSO_weather_t",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ARSO_weather_rh",
        icon="mdi:water-percent",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ARSO_weather_msl",
        icon="mdi:thermometer-lines",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = []
    for entity_description in ENTITY_DESCRIPTIONS:
        entity_description.name = (
            entry.data[CONF_LOCATION] + " " + str(entity_description.device_class)
        )
        if entity_description.device_class == SensorDeviceClass.TEMPERATURE:
            _data_type = "t"
        elif entity_description.device_class == SensorDeviceClass.HUMIDITY:
            _data_type = "rh"
        elif entity_description.device_class == SensorDeviceClass.ATMOSPHERIC_PRESSURE:
            _data_type = "msl"
        else:
            _data_type = ""

        devices.append(
            ARSOSensor(
                coordinator=coordinator,
                entity_description=entity_description,
                location=entry.data[CONF_LOCATION],
                data_type=_data_type,
                sensor_entity_id=generate_entity_id(
                    "sensor.{}",
                    "ARSO_" + entry.data[CONF_LOCATION] + "_" + _data_type,
                    hass=hass,
                ),
                unique_id=entry.entry_id,
            )
        )
    async_add_devices(devices)


class ARSOSensor(ARSOEntity, SensorEntity):
    """ARSO_weather Sensor class."""

    def __init__(
        self,
        coordinator: ARSODataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        location: str,
        data_type: str,
        sensor_entity_id: str | None = None,
        unique_id: str | None = None,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._location = location
        self._data_type = data_type
        self.entity_id = sensor_entity_id
        self._attr_unique_id = unique_id + self._location + self._data_type

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        LOGGER.debug(
            self.coordinator.data.current_meteo_data(self._location, self._data_type)
        )
        return self.coordinator.data.current_meteo_data(self._location, self._data_type)
