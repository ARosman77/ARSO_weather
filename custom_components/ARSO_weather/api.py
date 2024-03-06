"""Sample API Client."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import asyncio
import socket
import aiohttp
import async_timeout

# from .const import LOGGER


class ARSOApiClientError(Exception):
    """Exception to indicate a general API error."""


class ARSOApiClientCommunicationError(ARSOApiClientError):
    """Exception to indicate a communication error."""


class ARSOApiClientAuthenticationError(ARSOApiClientError):
    """Exception to indicate an authentication error."""


class ARSOMeteoData:
    """Meteo data class."""

    def __init__(
        self,
        current_data: str,
        forecast_data: str,
    ) -> None:
        """Initialize Meteo data class."""
        self._current_data = current_data
        self._forecast_data = forecast_data
        self._meteo_data_all = []
        self._meteo_fc_data_all = []

        data_selection = [
            "domain_title",
            "domain_longTitle",
            "domain_lat",
            "domain_lon",
            "domain_altitude",
            "t",
            "rh",
            "msl",
        ]

        data_fc_selection = [
            "domain_shortTitle",
            "domain_lat",
            "domain_lon",
            "domain_altitude",
            "valid",
            "nn_decodeText",
            "wwsyn_decodeText",
            "rr_decodeText",
            "td",  # dev point
            "dd_decodeText",  # wind direction
            "ff_val",  # wind m/s
            "t",
            "tnsyn",  # min temp
            "txsyn",  # max temp
            "msl",
        ]

        root = ET.fromstring(current_data)
        for meteo_parent in root.findall("metData"):
            meteo_data_location = {}
            for data in data_selection:
                meteo_data_location[data] = meteo_parent.find(data).text
            self._meteo_data_all.append(meteo_data_location)

        root = ET.fromstring(forecast_data)
        for meteo_parent in root.findall("metData"):
            meteo_data_region = {}
            for data in data_fc_selection:
                meteo_data_region[data] = meteo_parent.find(data).text
            self._meteo_fc_data_all.append(meteo_data_region)

    def current_temperature(self, location: str) -> str:
        """Return temperature of the location."""
        return self.current_meteo_data(location, "t")

    def current_humidity(self, location: str) -> str:
        """Return humidity of the location."""
        return self.current_meteo_data(location, "rh")

    def current_air_pressure(self, location: str) -> str:
        """Return air pressure of the location."""
        return self.current_meteo_data(location, "msl")

    def current_meteo_data(self, location: str, data_type: str) -> str:
        """Return temperature of the location."""
        meteo_data_location = next(
            (
                item
                for item in self._meteo_data_all
                if item["domain_longTitle"] == location
            ),
            False,
        )
        return meteo_data_location[data_type]

    def list_of_locations(self) -> list:
        """Return list of possible locations."""
        list_of_locations = []
        for meteo_data_location in self._meteo_data_all:
            list_of_locations.append(meteo_data_location["domain_longTitle"])
        return list_of_locations

    def list_of_forecast_regions(self) -> list:
        """Return list of possible forecast regions."""
        list_of_regions = []
        for meteo_data_region in self._meteo_fc_data_all:
            list_of_regions.append(meteo_data_region["domain_shortTitle"])
        return list(set(list_of_regions)) # Using set to remove duplicate entries


class ARSOApiClient:
    """Sample API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        # pylint: disable=line-too-long
        meteo_data_xml = await self._api_wrapper(
            method="get",
            url="https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml",
        )
        meteo_forecast_xml = await self._api_wrapper(
            method="get",
            url="https://meteo.arso.gov.si/uploads/probase/www/fproduct/text/sl/forecast_si_latest.xml",
        )
        return ARSOMeteoData(meteo_data_xml, meteo_forecast_xml)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise ARSOApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.text()

        except asyncio.TimeoutError as exception:
            raise ARSOApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ARSOApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ARSOApiClientError("Something really wrong happened!") from exception
