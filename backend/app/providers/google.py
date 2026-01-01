from typing import List, Dict, Any, AsyncIterator
import google.generativeai as genai

from app.providers.base import BaseProvider
from app.config import settings


class GoogleProvider(BaseProvider):
    """Google AI (Gemini) provider."""

    def __init__(self):
        genai.configure(api_key=settings.google_api_key)

    async def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        # Convert messages to Gemini format
        gemini_model = genai.GenerativeModel(model)

        # Build conversation history
        history = []
        system_prompt = ""
        current_message = ""

        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                current_message = msg["content"]
                if system_prompt:
                    current_message = f"{system_prompt}\n\n{current_message}"
                    system_prompt = ""
            elif msg["role"] == "assistant":
                history.append({"role": "user", "parts": [current_message]})
                history.append({"role": "model", "parts": [msg["content"]]})
                current_message = ""

        chat = gemini_model.start_chat(history=history)

        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        response = await chat.send_message_async(
            current_message or messages[-1]["content"],
            generation_config=generation_config,
        )

        return response.text

    async def stream_generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        gemini_model = genai.GenerativeModel(model)

        # Build the prompt from messages
        prompt_parts = []
        for msg in messages:
            if msg["role"] == "system":
                prompt_parts.append(f"System: {msg['content']}")
            elif msg["role"] == "user":
                prompt_parts.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                prompt_parts.append(f"Assistant: {msg['content']}")

        prompt = "\n\n".join(prompt_parts)

        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        response = await gemini_model.generate_content_async(
            prompt,
            generation_config=generation_config,
            stream=True,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

    @classmethod
    def get_available_models(cls) -> List[Dict[str, str]]:
        return [
            {"id": "gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro"},
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash"},
            {"id": "gemini-1.0-pro", "name": "Gemini 1.0 Pro"},
        ]
