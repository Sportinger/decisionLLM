from fastapi import APIRouter

from app.providers import provider_registry
from app.config import settings

router = APIRouter()


@router.get("/")
async def list_providers():
    """List all available providers and their status."""
    providers = []

    for provider_name in provider_registry.list_providers():
        provider_class = provider_registry.get(provider_name)
        if provider_class:
            # Check if API key is configured
            configured = False
            if provider_name == "openai" and settings.openai_api_key:
                configured = True
            elif provider_name == "anthropic" and settings.anthropic_api_key:
                configured = True
            elif provider_name == "google" and settings.google_api_key:
                configured = True
            elif provider_name == "mistral" and settings.mistral_api_key:
                configured = True
            elif provider_name == "local":
                configured = True  # Local doesn't need API key

            providers.append({
                "name": provider_name,
                "configured": configured,
                "models": provider_class.get_available_models(),
            })

    return {"providers": providers}


@router.get("/{provider_name}/models")
async def get_provider_models(provider_name: str):
    """Get available models for a specific provider."""
    provider_class = provider_registry.get(provider_name)
    if not provider_class:
        return {"error": f"Provider '{provider_name}' not found", "models": []}

    return {"provider": provider_name, "models": provider_class.get_available_models()}
