"""Weather platform for ARSO_weather."""

from __future__ import annotations

from homeassistant.helpers.entity import generate_entity_id

from .const import DOMAIN, CONF_REGION, ATTRIBUTION, LOGGER
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

from homeassistant.components.weather import (
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_WIND_SPEED,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_PRECIPITATION,
    PLATFORM_SCHEMA,
    WeatherEntity,
    WeatherEntityDescription,
    Forecast,
    WeatherEntityFeature,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfPrecipitationDepth,
)

WIND_MAPPING = {
    0: ("-", 0),
    1: ("N", 10),
    2: ("NE", 10),
    3: ("E", 10),
    4: ("SE", 10),
    5: ("S", 10),
    6: ("SW", 10),
    7: ("W", 10),
    8: ("NW", 10),
    9: ("N", 25),
    10: ("NE", 25),
    11: ("E", 25),
    12: ("SE", 25),
    13: ("S", 25),
    14: ("SW", 25),
    15: ("W", 25),
    16: ("NW", 25),
    17: ("N", 50),
    18: ("NE", 50),
    19: ("E", 50),
    20: ("SE", 50),
    21: ("S", 50),
    22: ("SW", 50),
    23: ("W", 50),
    24: ("NW", 50),
}

WIND_SPEED_MAPPING = {
    0: 0,
    1: 10,
    2: 25,
    3: 50,
}

ENTITY_DESCRIPTIONS = (
    WeatherEntityDescription(
        key="ARSO_weather_forecast",
        name="ARSO Weather",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up ARSO weather platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = []
    for entity_description in ENTITY_DESCRIPTIONS:
        devices.append(
            ARSOWeather(
                coordinator=coordinator,
                entity_description=entity_description,
                region=entry.data[CONF_REGION],
                weather_entity_id=generate_entity_id(
                    "sensor.{}",
                    "ARSO_" + entry.data[CONF_REGION],
                    hass=hass,
                ),
                unique_id=entry.entry_id,
            )
        )
        async_add_devices(devices)


class ARSOWeather(WeatherEntity):
    """Representation of a weather condition."""

    def __init__(
        self,
        coordinator: ARSODataUpdateCoordinator,
        entity_description: WeatherEntityDescription,
        region: str,
        weather_entity_id: str | None = None,
        unique_id: str | None = None,
    ):
        """Initialise the platform with a data instance and station name."""
        LOGGER.debug("Initialized.")
        self.coordinator = coordinator
        self._entity_description=entity_description

    def update(self):
        """Update current conditions."""
        LOGGER.debug("Update - called.")

    @property
    def supported_features(self) -> WeatherEntityFeature:
        """Return supported features."""
        return (
            WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._entity_description.name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def condition(self):
        """Return the current condition."""
        return "cloudy"

    @property
    def entity_picture(self):
        """Weather symbol if type is condition."""
        return None

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return "attr"

    @property
    def native_temperature(self):
        """Return the platform temperature."""
        return 3.0

    @property
    def native_temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def native_pressure(self):
        """Return platform air pressure."""
        return 1000.0

    @property
    def native_pressure_unit(self):
        """Return the unit of measurement."""
        return UnitOfPressure.HPA

    @property
    def humidity(self):
        """Return the humidity."""
        return 30

    @property
    def native_precipitation(self):
        """Return the precipitation."""
        return 10.0

    @property
    def native_precipitation_unit(self):
        """Return the precipitation unit."""
        return UnitOfPrecipitationDepth.MILLIMETERS

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        return 10

    @property
    def native_wind_speed_unit(self):
        """Return the unit of measurement."""
        return UnitOfSpeed.METERS_PER_SECOND

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return 50

    async def async_forecast_hourly(self) -> list[Forecast]:
        """Return hourly forecast."""
        return self._get_forecast()

    async def async_forecast_daily(self) -> list[Forecast]:
        """Return daily forecast."""
        return self._get_forecast()

    @property
    def forecast(self):
        """Return forecast."""
        return self._get_forecast()
