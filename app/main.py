from fastapi import FastAPI, HTTPException

from app.agents.orchestrator import decide_approval, run_mission
from app.models.schemas import ApprovalRequest, MissionRequest, MissionResponse

app = FastAPI(
    title="Agentic Government Mission Copilot",
    version="1.0.0",
    description="Synthetic portfolio demo with RAG, agent orchestration, tools, and human approval gates.",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/mission/run", response_model=MissionResponse)
def mission_run(req: MissionRequest) -> MissionResponse:
    state = run_mission(req.request, req.user_id, req.role)
    return MissionResponse(**state)


@app.post("/mission/approve", response_model=MissionResponse)
def mission_approve(req: ApprovalRequest) -> MissionResponse:
    try:
        state = decide_approval(req.approval_id, req.approver_id, req.decision, req.comment)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return MissionResponse(**state)
