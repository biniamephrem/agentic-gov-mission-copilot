from __future__ import annotations

import os


class AzureAISearchRetriever:
    """Reference Azure AI Search retriever adapter."""

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.endpoint or not self.index_name:
            raise RuntimeError("Azure AI Search is not configured.")
        return []
