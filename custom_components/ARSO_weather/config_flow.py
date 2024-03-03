"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    ARSOApiClient,
    ARSOApiClientAuthenticationError,
    ARSOApiClientCommunicationError,
    ARSOApiClientError,
)
from .const import DOMAIN, LOGGER, CONF_LOCATION
from .coordinator import ARSODataUpdateCoordinator



class ARSOFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        """Get list of locations to choose from."""
        list_of_locations = await self._return_locations(location='')

        """Present settings UI."""
        if user_input is not None:
            try:
                await self._test_connecton(
                    location=user_input[CONF_LOCATION],
                )
            except ARSOApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except ARSOApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except ARSOApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_LOCATION],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LOCATION): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=list_of_locations,
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_connecton(self, location: str) -> None:
        """Validate connection."""
        client = ARSOApiClient(
            location=location,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

    async def _return_locations(self, location: str) -> list:
        """Get all possible locations."""
        client = ARSOApiClient(
            location=location,
            session=async_create_clientsession(self.hass),
        )
        meteo_data_all = await client.async_get_data()
        list_of_locations = []
        for meteo_data_location in meteo_data_all:
            list_of_locations.append(meteo_data_location["domain_title"])
        return list_of_locations

