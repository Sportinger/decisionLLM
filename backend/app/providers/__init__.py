from typing import Dict, Type, Optional, List
from app.providers.base import BaseProvider


class ProviderRegistry:
    """Registry for LLM providers."""

    def __init__(self):
        self._providers: Dict[str, Type[BaseProvider]] = {}

    def register(self, name: str, provider_class: Type[BaseProvider]):
        """Register a provider class."""
        self._providers[name] = provider_class

    def get(self, name: str) -> Optional[Type[BaseProvider]]:
        """Get a provider class by name."""
        return self._providers.get(name)

    def list_providers(self) -> List[str]:
        """List all registered provider names."""
        return list(self._providers.keys())


# Global registry
provider_registry = ProviderRegistry()

# Import and register providers
from app.providers.openai import OpenAIProvider
from app.providers.anthropic import AnthropicProvider
from app.providers.google import GoogleProvider
from app.providers.mistral import MistralProvider
from app.providers.local import LocalProvider

provider_registry.register("openai", OpenAIProvider)
provider_registry.register("anthropic", AnthropicProvider)
provider_registry.register("google", GoogleProvider)
provider_registry.register("mistral", MistralProvider)
provider_registry.register("local", LocalProvider)
