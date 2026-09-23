from __future__ import annotations

import os
from typing import Any


class AzureOpenAIProvider:
    """Reference Azure OpenAI / Azure AI Foundry model adapter.

    This file intentionally avoids making a live network call in the public demo.
    Replace `invoke` with the approved Azure SDK/client for your environment.
    """

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

    def invoke(self, messages: list[dict[str, Any]]) -> str:
        if not self.endpoint or not self.deployment:
            raise RuntimeError("Azure OpenAI provider is not configured.")
        return "Azure OpenAI provider placeholder response."
