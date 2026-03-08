# External Conversation Agent for Home Assistant

A Home Assistant custom integration that forwards conversation requests to an external HTTP service. Use it to connect any custom AI agent to Home Assistant's voice assistant pipeline.

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu → Custom repositories
3. Add `https://github.com/BikesAndBBQ/ha-external-conversation-agent` as an Integration
4. Install "External Conversation Agent"
5. Restart Home Assistant

### Manual

Copy `custom_components/external_conversation_agent/` to your Home Assistant `config/custom_components/` directory and restart.

## Configuration

1. Go to Settings → Devices & Services → Add Integration
2. Search for "External Conversation Agent"
3. Enter the URL of your conversation agent service
4. Set the request timeout (default: 30 seconds)

## API Contract

Your external service must implement:

### `POST /api/conversation`

**Request:**
```json
{
  "text": "What's on my schedule today?",
  "conversation_id": "session-123",
  "language": "en",
  "device_id": "optional-device-id"
}
```

**Response:**
```json
{
  "response": "You have three meetings this afternoon.",
  "conversation_id": "session-123"
}
```

## Voice Pipeline

To use with a voice assistant (e.g., Home Assistant Voice PE):

1. Go to Settings → Voice Assistants
2. Edit your voice pipeline (or create a new one)
3. Set the **Conversation agent** to your External Conversation Agent instance
