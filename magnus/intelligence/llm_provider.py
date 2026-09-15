from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Provider abstraction; core logic must not depend on a single vendor."""

    @abstractmethod
    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        """Free-form text generation."""

    @abstractmethod
    async def extract_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        *,
        system: str | None = None,
    ) -> dict[str, Any]:
        """Structured extraction against a JSON schema description."""

    @abstractmethod
    async def reason(
        self,
        prompt: str,
        context: dict[str, Any],
        *,
        system: str | None = None,
    ) -> str:
        """Higher-level reasoning over supplied context."""
