"""Config flow for External Conversation Agent."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

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
