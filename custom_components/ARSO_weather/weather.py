"""Weather platform for ARSO_weather."""

from __future__ import annotations

from homeassistant.helpers.entity import generate_entity_id

from .const import DOMAIN, CONF_LOCATION, CONF_REGION, ATTRIBUTION, LOGGER
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

from homeassistant.components.weather import (
    # ATTR_WEATHER_HUMIDITY,
    # ATTR_WEATHER_PRESSURE,
    # ATTR_WEATHER_TEMPERATURE,
    # ATTR_WEATHER_WIND_BEARING,
    # ATTR_WEATHER_WIND_SPEED,
    # ATTR_FORECAST_TIME,
    # ATTR_FORECAST_TEMP,
    # ATTR_FORECAST_TEMP_LOW,
    # ATTR_FORECAST_CONDITION,
    # ATTR_FORECAST_WIND_SPEED,
    # ATTR_FORECAST_WIND_BEARING,
    # ATTR_FORECAST_PRECIPITATION,
    # PLATFORM_SCHEMA,
    WeatherEntity,
    WeatherEntityDescription,
    # Forecast,
    WeatherEntityFeature,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfPrecipitationDepth,
)

# condition mapping for tag <nn_icon-wwsyn_icon> in observations xml
CONDITION_MAPPING = {
    "clear": "sunny",
    "mostClear": "sunny",
    "slightCloudy": "sunny",
    "partCloudy": "partlycloudy",
    "modCloudy": "partlycloudy",
    "prevCloudy": "cloudy",
    "overcast": "cloudy",
    "FG": "fog",
}

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
        entity_description.name = entry.data[CONF_LOCATION]
        devices.append(
            ARSOWeather(
                coordinator=coordinator,
                entity_description=entity_description,
                location=entry.data[CONF_LOCATION],
                region=entry.data[CONF_REGION],
                weather_entity_id=generate_entity_id(
                    "weather.{}",
                    "ARSO_" + entry.data[CONF_REGION],
                    hass=hass,
                ),
                unique_id=entry.entry_id,
            )
        )
        async_add_devices(devices)


class ARSOWeather(ARSOEntity, WeatherEntity):
    """Representation of a weather condition."""

    def __init__(
        self,
        coordinator: ARSODataUpdateCoordinator,
        entity_description: WeatherEntityDescription,
        location: str,
        region: str,
        weather_entity_id: str | None = None,
        unique_id: str | None = None,
    ):
        """Initialise the platform with a data instance and station name."""
        LOGGER.debug("Initialized.")
        super().__init__(coordinator)
        self.entity_id = weather_entity_id

        self._location = location
        self._region = region

        self._attr_unique_id = unique_id + self._region
        self._attr_name = entity_description.name
        self._attr_attribution = ATTRIBUTION

    @property
    def supported_features(self) -> WeatherEntityFeature:
        """Return supported features."""
        LOGGER.debug("supported_features")
        # return (
        #    WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY
        # )
        return None

    @property
    def state(self):
        """Return the condition at specified location."""
        LOGGER.debug(
            "condition:"
            + CONDITION_MAPPING[self.coordinator.data.current_condition(self._location)]
        )
        return CONDITION_MAPPING[
            self.coordinator.data.current_condition(self._location)
        ]

    # @property
    # def entity_picture(self):
    #    """Weather symbol if type is condition."""
    #    LOGGER.debug("entity_picture")
    #    return None

    # @property
    # def extra_state_attributes(self):
    #    """Return the state attributes."""
    #    LOGGER.debug("extra_state_attributes")
    #    return "attr"

    @property
    def native_temperature(self):
        """Return the platform temperature."""
        LOGGER.debug(
            "native_temperature:"
            + self.coordinator.data.current_temperature(self._location)
        )
        return self.coordinator.data.current_temperature(self._location)

    @property
    def native_temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def native_pressure(self):
        """Return platform air pressure."""
        LOGGER.debug(
            "native_pressure:"
            + self.coordinator.data.current_air_pressure(self._location)
        )
        return self.coordinator.data.current_air_pressure(self._location)

    @property
    def native_pressure_unit(self):
        """Return the unit of measurement."""
        LOGGER.debug("native_pressure_unit")
        return UnitOfPressure.HPA

    @property
    def humidity(self):
        """Return the humidity."""
        LOGGER.debug(
            "native_humidity:"
            + str(self.coordinator.data.current_humidity(self._location))
        )
        return self.coordinator.data.current_humidity(self._location)

    @property
    def native_precipitation(self):
        """Return the precipitation."""
        LOGGER.debug("native_precipitation")
        return 10.0

    @property
    def native_precipitation_unit(self):
        """Return the precipitation unit."""
        LOGGER.debug("native_precipitation_unit")
        return UnitOfPrecipitationDepth.MILLIMETERS

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        LOGGER.debug("native_wind_speed")
        return 10

    @property
    def native_wind_speed_unit(self):
        """Return the unit of measurement."""
        LOGGER.debug("native_wind_speed_unit")
        return UnitOfSpeed.METERS_PER_SECOND

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        LOGGER.debug("wind_bearing")
        return 50

    # async def async_forecast_hourly(self) -> list[Forecast]:
    #    """Return hourly forecast."""
    #    #return self._get_forecast()
    #    return None

    # async def async_forecast_daily(self) -> list[Forecast]:
    #    """Return daily forecast."""
    #    #return self._get_forecast()
    #    return None

    # @property
    # def forecast(self):
    #    """Return forecast."""
    #    #return self._get_forecast()
    #    return None
