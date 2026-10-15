"""Config flow for External Conversation Agent."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import CONF_API_TOKEN, CONF_API_URL, CONF_TIMEOUT, DEFAULT_TIMEOUT, DOMAIN

# Masked in the form; sent as "Authorization: Bearer <token>" when set.
TOKEN_SELECTOR = TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))


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
                    vol.Optional(CONF_API_TOKEN, default=""): TOKEN_SELECTOR,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow."""
        return ExternalConversationAgentOptionsFlow()


class ExternalConversationAgentOptionsFlow(OptionsFlow):
    """Options flow for External Conversation Agent."""

    async def async_step_init(self, user_input=None):
        """Handle options."""
        if user_input is not None:
            user_input.setdefault(CONF_API_TOKEN, "")
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
                    # suggested_value, not default: an emptied field then
                    # clears the token instead of falling back to the old one.
                    vol.Optional(
                        CONF_API_TOKEN,
                        description={
                            "suggested_value": self.config_entry.data.get(
                                CONF_API_TOKEN, ""
                            )
                        },
                    ): TOKEN_SELECTOR,
                }
            ),
        )
