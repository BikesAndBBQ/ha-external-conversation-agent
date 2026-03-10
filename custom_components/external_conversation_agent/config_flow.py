"""Config flow for External Conversation Agent."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import callback

from .const import CONF_API_URL, CONF_TIMEOUT, DEFAULT_TIMEOUT, DOMAIN


class ExternalConversationAgentConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for External Conversation Agent."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle initial setup."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_API_URL],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_URL): str,
                    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow."""
        return ExternalConversationAgentOptionsFlow(config_entry)


class ExternalConversationAgentOptionsFlow(OptionsFlow):
    """Options flow for External Conversation Agent."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options."""
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self.config_entry, data={**self.config_entry.data, **user_input}
            )
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_URL,
                        default=self.config_entry.data.get(CONF_API_URL, ""),
                    ): str,
                    vol.Optional(
                        CONF_TIMEOUT,
                        default=self.config_entry.data.get(
                            CONF_TIMEOUT, DEFAULT_TIMEOUT
                        ),
                    ): int,
                }
            ),
        )
