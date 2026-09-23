from __future__ import annotations

import os
from typing import Any


class GCPVertexProvider:
    """Reference Vertex AI / Gemini model adapter.

    This public demo keeps the adapter offline by default. Replace `invoke`
    with an approved Vertex AI SDK call in the target project/environment.
    """

    def __init__(self) -> None:
        self.project_id = os.getenv("GCP_PROJECT_ID", "")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.model = os.getenv("GCP_VERTEX_MODEL", "")

    def invoke(self, messages: list[dict[str, Any]]) -> str:
        if not self.project_id or not self.model:
            raise RuntimeError("GCP Vertex provider is not configured.")
        return "Vertex AI provider placeholder response."
