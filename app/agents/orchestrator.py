from __future__ import annotations

import uuid
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.services.audit import audit
from app.services.llm import LocalMissionModel
from app.services.policy import requires_human_approval
from app.services.rag import MissionRAG
from app.tools.mission_tools import execute_tool


class MissionState(TypedDict, total=False):
    mission_id: str
    request: str
    user_id: str
    role: str
    evidence: list[dict[str, Any]]
    summary: str
    proposed_action: dict[str, Any] | None
    approval_id: str | None
    status: str
    tool_result: dict[str, Any] | None


RAG = MissionRAG()
MODEL = LocalMissionModel()
PENDING_APPROVALS: dict[str, MissionState] = {}


def retrieve(state: MissionState) -> MissionState:
    docs = RAG.retrieve(state["request"], top_k=3)
    evidence = [{"source": d.source, "text": d.text, "score": d.score} for d in docs]
    audit("retrieval.completed", state["mission_id"], {"sources": [d["source"] for d in evidence]})
    return {**state, "evidence": evidence}


def analyze(state: MissionState) -> MissionState:
    summary = MODEL.summarize(state["request"], state.get("evidence", []))
    proposal = MODEL.propose_action(state["request"], state.get("evidence", []))
    proposal_dict = proposal.model_dump() if proposal else None
    audit("analysis.completed", state["mission_id"], {"action_proposed": bool(proposal_dict)})
    return {**state, "summary": summary, "proposed_action": proposal_dict}


def policy_gate(state: MissionState) -> MissionState:
    proposal = state.get("proposed_action")
    if not proposal:
        return {**state, "status": "completed"}

    if requires_human_approval(proposal["tool"], proposal["arguments"]):
        approval_id = str(uuid.uuid4())
        pending = {**state, "approval_id": approval_id, "status": "awaiting_human_approval"}
        PENDING_APPROVALS[approval_id] = pending
        audit("approval.required", state["mission_id"], {"approval_id": approval_id, "tool": proposal["tool"]})
        return pending

    return {**state, "status": "approved_for_execution"}


def execute_low_risk(state: MissionState) -> MissionState:
    proposal = state.get("proposed_action")
    if not proposal:
        return state
    result = execute_tool(proposal["tool"], proposal["arguments"])
    audit("tool.executed", state["mission_id"], {"tool": proposal["tool"], "result": result})
    return {**state, "tool_result": result, "status": "completed"}


def route_after_policy(state: MissionState) -> str:
    if state.get("status") == "approved_for_execution":
        return "execute"
    return "end"


workflow = StateGraph(MissionState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("analyze", analyze)
workflow.add_node("policy", policy_gate)
workflow.add_node("execute", execute_low_risk)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", "policy")
workflow.add_conditional_edges("policy", route_after_policy, {"execute": "execute", "end": END})
workflow.add_edge("execute", END)
GRAPH = workflow.compile()


def run_mission(request: str, user_id: str, role: str) -> MissionState:
    mission_id = str(uuid.uuid4())
    audit("mission.started", mission_id, {"user_id": user_id, "role": role, "request": request})
    return GRAPH.invoke({
        "mission_id": mission_id,
        "request": request,
        "user_id": user_id,
        "role": role,
    })


def decide_approval(approval_id: str, approver_id: str, decision: str, comment: str) -> MissionState:
    state = PENDING_APPROVALS.pop(approval_id, None)
    if state is None:
        raise KeyError("Unknown or already-processed approval_id")

    audit("approval.decided", state["mission_id"], {
        "approval_id": approval_id,
        "approver_id": approver_id,
        "decision": decision,
        "comment": comment,
    })

    if decision != "approved":
        return {**state, "status": "rejected_by_human"}

    proposal = state["proposed_action"]
    result = execute_tool(proposal["tool"], proposal["arguments"])
    audit("tool.executed_after_approval", state["mission_id"], {"tool": proposal["tool"], "result": result})
    return {**state, "status": "completed", "tool_result": result}
