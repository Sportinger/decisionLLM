from typing import List, Dict, Any, AsyncIterator
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

from app.providers.base import BaseProvider
from app.config import settings


class MistralProvider(BaseProvider):
    """Mistral AI provider."""

    def __init__(self):
        self.client = MistralAsyncClient(api_key=settings.mistral_api_key)

    async def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        # Convert to Mistral message format
        mistral_messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]

        response = await self.client.chat(
            model=model,
            messages=mistral_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    async def stream_generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        # Convert to Mistral message format
        mistral_messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]

        async for chunk in self.client.chat_stream(
            model=model,
            messages=mistral_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    @classmethod
    def get_available_models(cls) -> List[Dict[str, str]]:
        return [
            {"id": "mistral-large-latest", "name": "Mistral Large"},
            {"id": "mistral-medium-latest", "name": "Mistral Medium"},
            {"id": "mistral-small-latest", "name": "Mistral Small"},
            {"id": "open-mixtral-8x22b", "name": "Mixtral 8x22B"},
            {"id": "open-mixtral-8x7b", "name": "Mixtral 8x7B"},
        ]
