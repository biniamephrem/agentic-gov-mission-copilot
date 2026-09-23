from __future__ import annotations

import os


class GCPVectorSearchRetriever:
    """Reference Vertex AI Vector Search retriever adapter."""

    def __init__(self) -> None:
        self.project_id = os.getenv("GCP_PROJECT_ID", "")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.index_endpoint = os.getenv("GCP_VECTOR_INDEX_ENDPOINT", "")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.project_id or not self.index_endpoint:
            raise RuntimeError("GCP Vector Search is not configured.")
        return []
