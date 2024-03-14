"""Constants for ARSO_weather."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "ARSO Weather"
DOMAIN = "ARSO_weather"
VERSION = "0.1.1"
ATTRIBUTION = "Data provided by ARSO (https://meteo.arso.gov.si/)."

CONF_LOCATION = "meteo_location"
CONF_REGION = "meteo_region"
