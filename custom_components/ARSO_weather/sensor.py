"""Sensor platform for ARSO_weather."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.helpers.entity import generate_entity_id


from .const import DOMAIN, CONF_LOCATION, LOGGER
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
    SensorEntityDescription(
        key="ARSO_weather_rh",
        name="ARSO Sensor rh",
        icon="mdi:thermometer",
        device_class= SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
    ),
)

async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = []
    for entity_description in ENTITY_DESCRIPTIONS:
        entity_description.name = "ARSO" + str(entity_description.device_class) + "Sensor for " + entry.data[CONF_LOCATION]
        if entity_description.device_class == SensorDeviceClass.TEMPERATURE:
            _data_type = 't'
        elif entity_description.device_class == SensorDeviceClass.HUMIDITY:
            _data_type = 'rh'
        else:
            _data_type = ''

        devices.append(
            ARSOSensor(
                coordinator=coordinator,
                entity_description=entity_description,
                location=entry.data[CONF_LOCATION],
                data_type=_data_type,
                sensor_entity_id = generate_entity_id("sensor.{}", "ARSO_"+_data_type+"_for_"+entry.data[CONF_LOCATION], hass=hass),
                unique_id=entry.entry_id,
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
        #self.entity_id = generate_entity_id("sensor.{}", "ARSO"+str(data_type)+"for"+str(location), hass=hass)
        self.entity_id = sensor_entity_id
        self._attr_unique_id = unique_id+self._location+self._data_type
        LOGGER.debug("Unique_ID="+str(self._attr_unique_id))
        LOGGER.debug("Entity_ID="+str(self.entity_id))


    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        #return self.coordinator.data.get("body")
        #meteo_data_location = next((item for item in self.coordinator.data if item["domain_title"] == "VOGEL"), False)
        meteo_data_location = next((item for item in self.coordinator.data if item["domain_title"] == self._location), False)
        return meteo_data_location[self._data_type]
