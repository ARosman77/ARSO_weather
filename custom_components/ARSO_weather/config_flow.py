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
    ARSOMeteoData,
)
from .const import DOMAIN, LOGGER, CONF_LOCATION

class ARSOFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ARSO Weather."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        #Get list of locations to choose from.
        list_of_locations = await self._return_locations()

        #Present settings UI.
        if user_input is not None:
            try:
                await self._test_connecton()
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

    async def _test_connecton(self) -> None:
        """Validate connection."""
        client = ARSOApiClient(
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

    async def _return_locations(self) -> list:
        """Get all possible locations."""
        client = ARSOApiClient(
            session=async_create_clientsession(self.hass),
        )
        meteo_data: ARSOMeteoData
        meteo_data = await client.async_get_data()
        return meteo_data.list_of_locations()
