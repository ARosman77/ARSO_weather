"""Weather platform for ARSO_weather."""

from __future__ import annotations

import dataclasses

from homeassistant.helpers.entity import generate_entity_id

from homeassistant.components.weather import (
    # Weather data
    # ATTR_WEATHER_HUMIDITY,
    # ATTR_WEATHER_OZONE,
    # ATTR_WEATHER_DEW_POINT,
    # ATTR_WEATHER_PRESSURE,
    # ATTR_WEATHER_PRESSURE_UNIT,
    # ATTR_WEATHER_APPARENT_TEMPERATURE,
    # ATTR_WEATHER_TEMPERATURE,
    # ATTR_WEATHER_TEMPERATURE_UNIT,
    # ATTR_WEATHER_VISIBILITY,
    # ATTR_WEATHER_VISIBILITY_UNIT,
    # ATTR_WEATHER_WIND_BEARING,
    # ATTR_WEATHER_WIND_GUST_SPEED,
    # ATTR_WEATHER_WIND_SPEED,
    # ATTR_WEATHER_WIND_SPEED_UNIT,
    # ATTR_WEATHER_PRECIPITATION_UNIT,
    # ATTR_WEATHER_CLOUD_COVERAGE,
    # ATTR_WEATHER_UV_INDEX,
    # Forecast data
    # ATTR_FORECAST_IS_DAYTIME,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_HUMIDITY,
    # ATTR_FORECAST_NATIVE_PRECIPITATION,
    # ATTR_FORECAST_PRECIPITATION,
    # ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_NATIVE_PRESSURE,
    # ATTR_FORECAST_PRESSURE,
    ATTR_FORECAST_NATIVE_APPARENT_TEMP,
    # ATTR_FORECAST_APPARENT_TEMP,
    ATTR_FORECAST_NATIVE_TEMP,
    # ATTR_FORECAST_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    # ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_NATIVE_WIND_GUST_SPEED,
    # ATTR_FORECAST_WIND_GUST_SPEED,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    # ATTR_FORECAST_WIND_SPEED,
    ATTR_FORECAST_NATIVE_DEW_POINT,
    # ATTR_FORECAST_DEW_POINT,
    # ATTR_FORECAST_CLOUD_COVERAGE,
    # ATTR_FORECAST_UV_INDEX,
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

from .const import DOMAIN, CONF_LOCATION, CONF_REGION, ATTRIBUTION, LOGGER
from .coordinator import ARSODataUpdateCoordinator
from .entity import ARSOEntity

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
        # entity_description.name = entry.data[CONF_LOCATION]
        new_entity_description = dataclasses.replace(
            entity_description, name=entry.data[CONF_LOCATION]
        )
        devices.append(
            ARSOWeather(
                coordinator=coordinator,
                entity_description=new_entity_description,
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
        # return None
        return WeatherEntityFeature.FORECAST_DAILY

    # @property
    # def state(self):
    #    """Return the condition at specified location."""
    #    return self.coordinator.data.current_condition(self._location)

    @property
    def condition(self):
        """Return the condition at specified location."""
        return self.coordinator.data.current_condition(self._location)

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
            "native_temperature: %s",
            str(self.coordinator.data.current_temperature(self._location)),
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
            "native_pressure: %s",
            str(self.coordinator.data.current_air_pressure(self._location)),
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
            "native_humidity: %s",
            str(self.coordinator.data.current_humidity(self._location)),
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
        LOGGER.debug(
            "native_wind_speed: %s",
            str(self.coordinator.data.current_wind_speed(self._location)),
        )
        return self.coordinator.data.current_wind_speed(self._location)

    @property
    def native_wind_speed_unit(self):
        """Return the unit of measurement."""
        LOGGER.debug("native_wind_speed_unit")
        return UnitOfSpeed.METERS_PER_SECOND

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        LOGGER.debug(
            "wind_bearing: %s",
            str(self.coordinator.data.current_wind_direction(self._location)),
        )
        return self.coordinator.data.current_wind_direction(self._location)

    def _get_forecast(self) -> list[Forecast]:
        """Return forecast."""
        _forecasts = []
        _list_of_meteo_data = []
        # Putting together all data from API, using dates to create a list of dictionaries
        for (
            fc_date,
            fc_min_temp,
            fc_max_temp,
            fc_condition,
            fc_humidity,
            fc_pressure,
            fc_temp,
            fc_dew_point,
            fc_wind_speed,
            fc_wind_gust,
            fc_wind_bearing,
        ) in zip(
            self.coordinator.data.fc_list_of_dates(self._region),
            self.coordinator.data.fc_list_of_min_temps(self._region),
            self.coordinator.data.fc_list_of_max_temps(self._region),
            self.coordinator.data.fc_list_of_condtions(self._region),
            self.coordinator.data.fc_list_of_humidities(self._region),
            self.coordinator.data.fc_list_of_presures(self._region),
            self.coordinator.data.fc_list_of_temps(self._region),
            self.coordinator.data.fc_list_of_dew_points(self._region),
            self.coordinator.data.fc_list_of_wind_speeds(self._region),
            self.coordinator.data.fc_list_of_wind_gusts(self._region),
            self.coordinator.data.fc_list_of_wind_bearing(self._region),
        ):
            _list_of_meteo_data.append(
                {
                    ATTR_FORECAST_TIME: fc_date,
                    ATTR_FORECAST_NATIVE_TEMP_LOW: fc_min_temp,
                    ATTR_FORECAST_NATIVE_TEMP: fc_max_temp,
                    ATTR_FORECAST_CONDITION: fc_condition,
                    ATTR_FORECAST_HUMIDITY: fc_humidity,
                    ATTR_FORECAST_NATIVE_PRESSURE: fc_pressure,
                    ATTR_FORECAST_NATIVE_APPARENT_TEMP: fc_temp,
                    ATTR_FORECAST_NATIVE_DEW_POINT: fc_dew_point,
                    ATTR_FORECAST_NATIVE_WIND_SPEED: fc_wind_speed,
                    ATTR_FORECAST_NATIVE_WIND_GUST_SPEED: fc_wind_gust,
                    ATTR_FORECAST_WIND_BEARING: fc_wind_bearing,
                }
            )

        for _forcast in _list_of_meteo_data:
            _forecasts.append(_forcast)

        return _forecasts

    async def async_forecast_hourly(self) -> list[Forecast]:
        """Return hourly forecast."""
        # return self._get_forecast()

    async def async_forecast_twice_daily(self) -> list[Forecast]:
        """Return twice_daily forecast."""
        # return self._get_forecast()

    async def async_forecast_daily(self) -> list[Forecast]:
        """Return daily forecast."""
        LOGGER.debug("_get_forecast: %s", str(self._get_forecast()))
        return self._get_forecast()
