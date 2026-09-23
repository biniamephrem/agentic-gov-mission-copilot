from __future__ import annotations

import os
from typing import Any


HIGH_IMPACT_TOOLS = {
    "request_resource_allocation",
    "dispatch_field_team",
    "change_operational_priority",
}


def assess_tool_risk(tool_name: str, arguments: dict[str, Any]) -> float:
    if tool_name in HIGH_IMPACT_TOOLS:
        return 0.85
    if tool_name.startswith("read_") or tool_name.startswith("search_"):
        return 0.10
    return 0.50


def requires_human_approval(tool_name: str, arguments: dict[str, Any]) -> bool:
    threshold = float(os.getenv("HITL_RISK_THRESHOLD", "0.60"))
    return assess_tool_risk(tool_name, arguments) >= threshold
