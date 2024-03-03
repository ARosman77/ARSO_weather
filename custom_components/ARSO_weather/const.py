"""Constants for ARSO_weather."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "ARSO Weather"
DOMAIN = "ARSO_weather"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by ARSO."

CONF_LOCATION = "meteo_location"
