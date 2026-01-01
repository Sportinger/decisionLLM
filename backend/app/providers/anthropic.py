from typing import List, Dict, Any, AsyncIterator
import anthropic

from app.providers.base import BaseProvider
from app.config import settings


class AnthropicProvider(BaseProvider):
    """Anthropic Claude API provider."""

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        # Extract system message if present
        system = None
        api_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                api_messages.append(msg)

        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system or "",
            messages=api_messages,
            temperature=temperature,
        )

        # Extract text from response
        text_content = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_content += block.text

        return text_content

    async def stream_generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        # Extract system message if present
        system = None
        api_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                api_messages.append(msg)

        async with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system or "",
            messages=api_messages,
            temperature=temperature,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    @classmethod
    def get_available_models(cls) -> List[Dict[str, str]]:
        return [
            {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4"},
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet"},
            {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku"},
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
        ]
