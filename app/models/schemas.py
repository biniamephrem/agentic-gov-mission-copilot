from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class MissionRequest(BaseModel):
    request: str = Field(min_length=5, max_length=4000)
    user_id: str
    role: str


class EvidenceItem(BaseModel):
    source: str
    text: str
    score: float


class ToolProposal(BaseModel):
    tool: str
    arguments: dict[str, Any]
    rationale: str
    risk_score: float = Field(ge=0.0, le=1.0)


class MissionResponse(BaseModel):
    mission_id: str
    status: str
    summary: str
    evidence: list[EvidenceItem] = []
    proposed_action: ToolProposal | None = None
    approval_id: str | None = None
    tool_result: dict[str, Any] | None = None


class ApprovalRequest(BaseModel):
    approval_id: str
    approver_id: str
    decision: Literal["approved", "rejected"]
    comment: str = ""
