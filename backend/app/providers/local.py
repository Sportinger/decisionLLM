from typing import List, Dict, Any, AsyncIterator
import httpx

from app.providers.base import BaseProvider
from app.config import settings


class LocalProvider(BaseProvider):
    """Local LLM provider using Ollama API."""

    def __init__(self):
        self.base_url = settings.ollama_base_url

    async def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")

    async def stream_generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                    "stream": True,
                },
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        import json
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue

    @classmethod
    def get_available_models(cls) -> List[Dict[str, str]]:
        # These are common Ollama models - actual available models
        # depend on what's installed locally
        return [
            {"id": "llama3.1:latest", "name": "Llama 3.1"},
            {"id": "llama3:latest", "name": "Llama 3"},
            {"id": "mistral:latest", "name": "Mistral"},
            {"id": "codellama:latest", "name": "Code Llama"},
            {"id": "phi3:latest", "name": "Phi 3"},
            {"id": "gemma2:latest", "name": "Gemma 2"},
            {"id": "qwen2:latest", "name": "Qwen 2"},
        ]
