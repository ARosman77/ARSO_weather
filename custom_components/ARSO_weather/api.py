"""Sample API Client."""
from __future__ import annotations

from .const import LOGGER

import asyncio
import socket

import aiohttp
import async_timeout

import xml.etree.ElementTree as ET

class ARSOApiClientError(Exception):
    """Exception to indicate a general API error."""


class ARSOApiClientCommunicationError(
    ARSOApiClientError
):
    """Exception to indicate a communication error."""


class ARSOApiClientAuthenticationError(
    ARSOApiClientError
):
    """Exception to indicate an authentication error."""


class ARSOApiClient:
    """Sample API Client."""

    def __init__(
        self,
        location: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._location = location
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        LOGGER.debug("API Location:"+str(self._location))
        meteo_data_all = []
        meteo_data_xml = await self._api_wrapper(method="get", url="https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml")
        root = ET.fromstring(meteo_data_xml)
        data_selection = ['domain_title','domain_longTitle','domain_lat','domain_lon','domain_altitude','t','rh','msl']
        for metData in root.findall('metData'):
            meteo_data_location = {}
            for data in data_selection:
                meteo_data_location[data] = metData.find(data).text
            meteo_data_all.append(meteo_data_location)
        return meteo_data_all

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._location

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
            raise ARSOApiClientError(
                "Something really wrong happened!"
            ) from exception
