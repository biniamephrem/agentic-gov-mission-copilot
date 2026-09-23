from __future__ import annotations

from app.models.schemas import ToolProposal


class LocalMissionModel:
    """Deterministic model adapter for a public portfolio demo.

    Swap this class with an adapter for Amazon Bedrock, Azure OpenAI, OpenAI,
    or another approved provider while preserving the same interface.
    """

    def summarize(self, request: str, evidence: list[dict]) -> str:
        if not evidence:
            return "No supporting mission evidence was retrieved. I cannot make a grounded operational assessment."
        joined = " ".join(item["text"].strip().replace("\n", " ") for item in evidence[:2])
        return f"Grounded mission assessment: {joined[:650]}"

    def propose_action(self, request: str, evidence: list[dict]) -> ToolProposal | None:
        combined = " ".join(item["text"].lower() for item in evidence)
        request_l = request.lower()
        if "communications" in combined and any(k in request_l for k in ["resource", "prepare", "action", "allocate"]):
            return ToolProposal(
                tool="request_resource_allocation",
                arguments={"resource": "mobile communications unit", "quantity": 1},
                rationale="Retrieved evidence indicates a sustained communications outage affecting response operations.",
                risk_score=0.85,
            )
        return None
