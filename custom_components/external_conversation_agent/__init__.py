"""External Conversation Agent - forwards conversation to an external HTTP service.

The external service must implement a POST endpoint at /api/conversation that
accepts JSON:

    {
        "text": "user's message",
        "conversation_id": "session-id",
        "language": "en",
        "device_id": "optional-device-id"
    }

And returns JSON:

    {
        "response": "agent's response text",
        "conversation_id": "session-id"
    }
"""

from __future__ import annotations

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_API_URL, CONF_TIMEOUT, DEFAULT_TIMEOUT


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up External Conversation Agent from a config entry."""
    agent = ExternalConversationAgent(hass, entry)
    conversation.async_set_agent(hass, entry, agent)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update — reload the integration."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload External Conversation Agent."""
    conversation.async_unset_agent(hass, entry)
    return True


class ExternalConversationAgent(conversation.AbstractConversationAgent):
    """Conversation agent that forwards to an external HTTP service."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.api_url = entry.data[CONF_API_URL].rstrip("/")
        self.timeout = entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    @property
    def supported_languages(self) -> list[str]:
        """Return supported languages."""
        return ["en"]

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Forward conversation to external service and return result."""
        client = get_async_client(self.hass)
        try:
            resp = await client.post(
                f"{self.api_url}/api/conversation",
                json={
                    "text": user_input.text,
                    "conversation_id": user_input.conversation_id or "",
                    "language": user_input.language,
                    "device_id": user_input.device_id or "",
                },
                timeout=float(self.timeout),
            )
            resp.raise_for_status()
            data = resp.json()
            response_text = data["response"]
            conversation_id = data.get("conversation_id", user_input.conversation_id)
        except Exception as err:
            response_text = f"Sorry, I couldn't reach the conversation agent: {err}"
            conversation_id = user_input.conversation_id

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response_text)

        return conversation.ConversationResult(
            response=intent_response,
            conversation_id=conversation_id,
        )
